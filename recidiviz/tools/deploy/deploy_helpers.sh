#!/usr/bin/env bash

BASH_SOURCE_DIR=$(dirname "$BASH_SOURCE")
source ${BASH_SOURCE_DIR}/../script_base.sh

VERSION_REGEX="^v([0-9]+)\.([0-9]+)\.([0-9]+)(-alpha.([0-9]+))?$"

# Parses a version tag and output a space-separated string of the version regex capture groups.
# Example usage:
#    $ VERSION_PARTS=($(parse_version v1.2.0-alpha.0))
#    $ echo "MAJOR VERSION NUMBER: ${VERSION_PARTS[1]}"
function parse_version {
    VERSION=$1
    if [[ ! ${VERSION} =~ ${VERSION_REGEX} ]]
    then
        echo_error "Expected a version tag matching regex $VERSION_REGEX. Instead found [$VERSION]."
        exit 1
    fi

    echo ${BASH_REMATCH[@]}
}

# Returns the last version tag on the given branch. Fails if that tag does not match the acceptable version regex.
function last_version_tag_on_branch {
    BRANCH=$1

    LAST_VERSION_TAG_ON_BRANCH=$(git tag --merged ${BRANCH} | sort_versions | tail -n 1) || exit_on_fail

    # Check that the version parses
    _=$(parse_version ${LAST_VERSION_TAG_ON_BRANCH}) || exit_on_fail

    echo ${LAST_VERSION_TAG_ON_BRANCH}
}

function next_alpha_version {
    PREVIOUS_VERSION=$1
    PREVIOUS_VERSION_PARTS=($(parse_version ${PREVIOUS_VERSION})) || exit_on_fail

    MAJOR=${PREVIOUS_VERSION_PARTS[1]}
    MINOR=${PREVIOUS_VERSION_PARTS[2]}
    PATCH=${PREVIOUS_VERSION_PARTS[3]}
    ALPHA=${PREVIOUS_VERSION_PARTS[4]-}  # Optional
    ALPHA_VERSION=${PREVIOUS_VERSION_PARTS[5]-}  # Optional

    if [[ -z ${ALPHA} ]]; then
        # If the previous version was a release version, bump the minor version and build a fresh alpha version
        NEW_VERSION="v$MAJOR.$(($MINOR + 1)).0-alpha.0"
    else
        # If the previous version was an alpha version, just increment alpha version
        NEW_VERSION="v$MAJOR.$MINOR.$PATCH-alpha.$(($ALPHA_VERSION + 1))"
    fi

    echo ${NEW_VERSION}
}

function verify_deploy_permissions {
    # TODO(3996): Actually check Github for Owner-level repo permissions

    GIT_USER_EMAIL="$(git config user.email)"
    EMAIL_PATTERN=".*\@recidiviz\.org$"

    if [[ ! ${GIT_USER_EMAIL} =~ ${EMAIL_PATTERN} ]]
    then
        echo_error "User [$GIT_USER_EMAIL] does not have sufficient permissions to deploy."
        echo_error "Please reach out to Recidiviz administrators if you need to deploy."
        exit 1
    fi
}

# Prints an error and exits if the provided commit does not have a green build on Travis.
function check_commit_is_green {
    COMMIT=$1

    # This returns an SVG with an element that will have the text "passing" if the build is passing.
    URL="https://api.travis-ci.com/Recidiviz/pulse-data.svg?token=pa7kG645RqXUvoHE2g9n&commit=$COMMIT"
    TRAVIS_BUILD_STATUS_SVG=$(curl ${URL})

    PASSING_PATTERN=">passing<"

    if [[ ! ${TRAVIS_BUILD_STATUS_SVG} =~ ${PASSING_PATTERN} ]]
    then
        echo_error "Commit [$COMMIT] is not passing on Travis. You must wait for a green build to deploy."
        exit 1
    fi

    echo "Build is passing for commit [$COMMIT]."
}

# Helper for deploying any infrastructure changes before we deploy a new version of the application. Requires that we
# have checked out the commit for the version that will be deployed.
function pre_deploy_configure_infrastructure {
    PROJECT=$1

    echo "Deploying cron.yaml"
    run_cmd gcloud -q app deploy cron.yaml --project=${PROJECT}

    echo "Updating the BigQuery Dataflow metric table schemas to match the metric classes"
    run_cmd pipenv run python -m recidiviz.calculator.calculation_data_storage_manager --project_id ${PROJECT} --function_to_execute update_schemas

    if [[ ${PROJECT} == 'recidiviz-staging' ]]; then
        echo "Deploying stage-only calculation pipelines to templates in ${PROJECT}."
        run_cmd pipenv run python -m recidiviz.tools.deploy.deploy_pipeline_templates --project_id ${PROJECT} --templates_to_deploy staging
    fi

    echo "Deploying prod-ready calculation pipelines to templates in ${PROJECT}."
    run_cmd pipenv run python -m recidiviz.tools.deploy.deploy_pipeline_templates --project_id ${PROJECT} --templates_to_deploy production

    echo "Initializing task queues"
    run_cmd pipenv run python -m recidiviz.tools.initialize_google_cloud_task_queues --project_id ${PROJECT} --google_auth_token $(gcloud auth print-access-token)
}