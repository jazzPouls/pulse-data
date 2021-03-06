# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2019 Recidiviz, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================
"""Reference table for Recidiviz users who should only have access to data from a single or limited set of supervision
locations.
"""

# pylint: disable=trailing-whitespace
from recidiviz.big_query.big_query_view import SimpleBigQueryViewBuilder
from recidiviz.calculator.query.state import dataset_config
from recidiviz.utils.environment import GCP_PROJECT_STAGING
from recidiviz.utils.metadata import local_project_id_override

SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_VIEW_NAME = (
    "supervision_location_restricted_access_emails"
)

SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_DESCRIPTION = """Reference table for Recidiviz users
who should only have access to data from a single or limited set of supervision locations"""

SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_QUERY_TEMPLATE = """
    /*{description}*/
    WITH
    mo_level_1_supervision_location_restricted_access AS (
        SELECT
          'US_MO' AS state_code,
          EMAIL AS restricted_user_email,
          STRING_AGG(DISTINCT DISTRICT, ',') AS allowed_level_1_supervision_location_ids
        FROM `{project_id}.us_mo_raw_data_up_to_date_views.LANTERN_DA_RA_LIST_latest`
        WHERE DISTRICT IS NOT NULL
        GROUP BY EMAIL
    )
    SELECT * FROM mo_level_1_supervision_location_restricted_access;
    """

SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_VIEW_BUILDER = SimpleBigQueryViewBuilder(
    dataset_id=dataset_config.REFERENCE_VIEWS_DATASET,
    view_id=SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_VIEW_NAME,
    view_query_template=SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_QUERY_TEMPLATE,
    description=SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_DESCRIPTION,
)

if __name__ == "__main__":
    with local_project_id_override(GCP_PROJECT_STAGING):
        SUPERVISION_LOCATION_RESTRICTED_ACCESS_EMAILS_VIEW_BUILDER.build_and_print()
