# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2021 Recidiviz, Inc.
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
"""Supervisees due for release by PO by day."""
# pylint: disable=line-too-long

from recidiviz.big_query.big_query_view import SimpleBigQueryViewBuilder
from recidiviz.calculator.query.state import dataset_config
from recidiviz.utils.environment import GCP_PROJECT_STAGING
from recidiviz.utils.metadata import local_project_id_override

SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_VIEW_NAME = 'supervision_population_due_for_release_by_po_by_day'

SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_DESCRIPTION = """
    Supervision population due for release by PO by day
 """

SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_QUERY_TEMPLATE = \
    """
    /*{description}*/
    SELECT
        state_code,
        date_of_supervision,
        supervising_officer_external_id as supervising_officer,
        supervising_district_external_id as district,
        COUNT (DISTINCT(IF(is_past_projected_end_date, person_id, NULL))) as due_for_release_count
    FROM `{project_id}.{materialized_metrics_dataset}.most_recent_supervision_population_metrics_materialized`
    WHERE date_of_supervision > DATE_SUB(CURRENT_DATE('US/Pacific'), INTERVAL 90 DAY)
    GROUP BY state_code, date_of_supervision, supervising_officer, district
    ORDER BY date_of_supervision DESC, supervising_officer DESC, due_for_release_count DESC
    """

SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_VIEW_BUILDER = SimpleBigQueryViewBuilder(
    dataset_id=dataset_config.VITALS_REPORT_DATASET,
    view_id=SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_VIEW_NAME,
    view_query_template=SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_QUERY_TEMPLATE,
    description=SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_DESCRIPTION,
    materialized_metrics_dataset=dataset_config.DATAFLOW_METRICS_MATERIALIZED_DATASET,
)

if __name__ == '__main__':
    with local_project_id_override(GCP_PROJECT_STAGING):
        SUPERVISION_POPULATION_DUE_FOR_RELEASE_BY_PO_BY_DAY_VIEW_BUILDER.build_and_print()