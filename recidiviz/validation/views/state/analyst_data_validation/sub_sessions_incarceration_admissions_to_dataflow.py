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

"""A view which provides an annual comparison between incarceration session starts and dataflow admissions."""

# pylint: disable=trailing-whitespace
from recidiviz.big_query.big_query_view import SimpleBigQueryViewBuilder
from recidiviz.utils.environment import GCP_PROJECT_STAGING
from recidiviz.utils.metadata import local_project_id_override
from recidiviz.validation.views import dataset_config

SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_NAME = (
    "sub_sessions_incarceration_admissions_to_dataflow"
)

SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_DESCRIPTION = """
    A view which provides an annual comparison between incarceration session starts and dataflow admissions. One 
    comparison is session starts vs sessions_with_start_reason (the latter being a subset of the former), which can 
    be used to identify the % of sessions with start reasons. Another comparison is dataflow_admissions vs 
    session_admissions (the latter being a subset of the former), which can be used to identify the % of dataflow 
    admission events represented in sessions.
    """

SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_QUERY_TEMPLATE = """
    /*{description}*/
    SELECT 
        state_code AS region_code,
        DATE_TRUNC(start_date, YEAR) AS start_year,
        SUM(sub_session_start) AS sub_session_starts,
        SUM(session_start) AS session_starts,
        SUM(sub_session_with_start_reason) AS sub_sessions_with_start_reason,
        SUM(session_with_start_reason) AS sessions_with_start_reason,
        SUM(dataflow_admission) AS dataflow_admissions,
        SUM(sub_session_admission) AS sub_session_admissions,
        SUM(session_admission) AS session_admissions
    FROM `{project_id}.{validation_views_dataset}.sub_sessions_incarceration_admissions_to_dataflow_disaggregated`
    GROUP BY 1,2
    ORDER BY 1,2
    """

SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_BUILDER = SimpleBigQueryViewBuilder(
    dataset_id=dataset_config.VIEWS_DATASET,
    view_id=SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_NAME,
    view_query_template=SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_QUERY_TEMPLATE,
    description=SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_DESCRIPTION,
    validation_views_dataset=dataset_config.VIEWS_DATASET,
)

if __name__ == "__main__":
    with local_project_id_override(GCP_PROJECT_STAGING):
        SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_BUILDER.build_and_print()
