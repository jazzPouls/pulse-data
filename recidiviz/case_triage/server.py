# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2020 Recidiviz, Inc.
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
"""Backend entry point for Case Triage API server."""
import json
import os
from http import HTTPStatus
from typing import Dict

from flask import Flask, Response, g, jsonify, send_from_directory, session
from flask_sqlalchemy_session import current_session
from flask_wtf.csrf import CSRFError, CSRFProtect
from sqlalchemy.orm.exc import NoResultFound

from recidiviz.case_triage.api_routes import api
from recidiviz.case_triage.authorization import AuthorizationStore
from recidiviz.case_triage.exceptions import CaseTriageAuthorizationError
from recidiviz.case_triage.impersonate_users import (
    IMPERSONATED_EMAIL_KEY,
    ImpersonateUser,
)
from recidiviz.case_triage.querier.querier import CaseTriageQuerier
from recidiviz.case_triage.scoped_sessions import setup_scoped_sessions
from recidiviz.case_triage.util import get_local_secret, SESSION_ADMIN_KEY
from recidiviz.persistence.database.sqlalchemy_engine_manager import (
    SQLAlchemyEngineManager,
    SchemaType,
)
from recidiviz.tools.postgres import local_postgres_helpers
from recidiviz.utils.auth.auth0 import (
    Auth0Config,
    get_userinfo,
    build_auth0_authorization_decorator,
)
from recidiviz.utils.environment import in_development, in_test
from recidiviz.utils.flask_exception import FlaskException
from recidiviz.utils.timer import RepeatedTimer

# Flask setup
static_folder = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../../frontends/case-triage/build/",
    )
)

app = Flask(__name__, static_folder=static_folder)
app.secret_key = get_local_secret("case_triage_secret_key")
CSRFProtect(app)

if in_development():
    db_url = local_postgres_helpers.postgres_db_url_from_env_vars()
else:
    db_url = SQLAlchemyEngineManager.get_server_postgres_instance_url(
        schema_type=SchemaType.CASE_TRIAGE
    )
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

setup_scoped_sessions(app, db_url)


# Auth setup
def on_successful_authorization(_payload: Dict[str, str], token: str) -> None:
    """
    Memoize the user's info (email_address, picture, etc) into our session
    Expose the user on the flask request global
    """
    if "user_info" not in session:
        session["user_info"] = get_userinfo(authorization_config.domain, token)

    email = session["user_info"]["email"]
    if email not in authorization_store.allowed_users:
        raise CaseTriageAuthorizationError(
            code="unauthorized",
            description="You are not authorized to access this application",
        )

    if email in authorization_store.admin_users:
        session[SESSION_ADMIN_KEY] = True


auth0_configuration = get_local_secret("case_triage_auth0")

if not auth0_configuration:
    raise ValueError("Missing Case Triage Auth0 configuration secret")

authorization_store = AuthorizationStore()
authorization_config = Auth0Config(json.loads(auth0_configuration))
requires_authorization = build_auth0_authorization_decorator(
    authorization_config, on_successful_authorization
)

store_refresh = RepeatedTimer(
    15 * 60, authorization_store.refresh, run_immediately=True
)

if not in_test():
    store_refresh.start()


# Security headers
@app.after_request
def set_headers(response: Response) -> Response:
    if not in_development():
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=63072000"  # max age of 2 years
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# Routes & Blueprints
@api.before_request
@requires_authorization
def fetch_user_info() -> None:
    """This method both fetches the current user and (by virtue of the decorator) enforces authorization
    for all API routes.

    If the user is an admin (i.e. an approved Recidiviz employee), and the `impersonated_email` param is
    set, then they can make requests as if they were the impersonated user.
    """
    try:
        if (
            IMPERSONATED_EMAIL_KEY in session
            and session["user_info"]["email"] in authorization_store.admin_users
        ):
            g.current_user = CaseTriageQuerier.officer_for_email(
                current_session, session[IMPERSONATED_EMAIL_KEY]
            )

        if not getattr(g, "current_user", None):
            g.current_user = CaseTriageQuerier.officer_for_email(
                current_session, session["user_info"]["email"]
            )
    except NoResultFound as e:
        if not session.get(SESSION_ADMIN_KEY):
            raise CaseTriageAuthorizationError(
                code="unauthorized",
                description="You are not authorized to access this application",
            ) from e


app.register_blueprint(api, url_prefix="/api")
app.add_url_rule(
    "/impersonate_user",
    view_func=ImpersonateUser.as_view(
        "impersonate_user",
        redirect_url="/",
        authorization_store=authorization_store,
    ),
)


@app.errorhandler(CSRFError)
def handle_csrf_error(_: CSRFError) -> Response:
    return handle_auth_error(
        FlaskException(
            code="invalid_csrf_token",
            description="The provided X-CSRF-Token header could not be validated",
            status_code=HTTPStatus.BAD_REQUEST,
        )
    )


@app.errorhandler(FlaskException)
def handle_auth_error(ex: FlaskException) -> Response:
    response = jsonify(
        {
            "code": ex.code,
            "description": ex.description,
        }
    )
    response.status_code = ex.status_code
    return response


@app.route("/auth0_public_config.js")
def auth0_public_config() -> str:
    # Expose ONLY the necessary variables to configure our Auth0 frontend
    return f"window.AUTH0_CONFIG = {authorization_config.as_public_config()};"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path: str = "") -> Response:
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)

    return send_from_directory(static_folder, "index.html")
