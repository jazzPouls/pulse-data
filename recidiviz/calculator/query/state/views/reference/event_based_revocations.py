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
"""Event Based Revocations."""
# pylint: disable=trailing-whitespace

from recidiviz.big_query.big_query_view import SimpleBigQueryViewBuilder
from recidiviz.calculator.query import bq_utils
from recidiviz.calculator.query.state import dataset_config
from recidiviz.utils.environment import GCP_PROJECT_STAGING
from recidiviz.utils.metadata import local_project_id_override

EVENT_BASED_REVOCATIONS_VIEW_NAME = "event_based_revocations"

EVENT_BASED_REVOCATIONS_DESCRIPTION = """
 Revocation data on the person level with revocation violation and admission information

 Expanded Dimensions: district, supervision_type
 """

EVENT_BASED_REVOCATIONS_QUERY_TEMPLATE = """
    /*{description}*/
    SELECT
      person_id, state_code, year, month,
      supervision_type,
      IFNULL(district, 'EXTERNAL_UNKNOWN') as district,
      judicial_district_code,
      supervising_officer_external_id AS officer_external_id,
      source_violation_type,
      revocation_admission_date,
      prioritized_race_or_ethnicity as race_or_ethnicity,
      gender,
      age_bucket
    FROM `{project_id}.{materialized_metrics_dataset}.most_recent_supervision_revocation_metrics_materialized`,
    {district_dimension},
    {supervision_type_dimension}
    WHERE {thirty_six_month_filter}
    """

EVENT_BASED_REVOCATIONS_VIEW_BUILDER = SimpleBigQueryViewBuilder(
    dataset_id=dataset_config.REFERENCE_VIEWS_DATASET,
    view_id=EVENT_BASED_REVOCATIONS_VIEW_NAME,
    view_query_template=EVENT_BASED_REVOCATIONS_QUERY_TEMPLATE,
    description=EVENT_BASED_REVOCATIONS_DESCRIPTION,
    materialized_metrics_dataset=dataset_config.DATAFLOW_METRICS_MATERIALIZED_DATASET,
    reference_views_dataset=dataset_config.REFERENCE_VIEWS_DATASET,
    district_dimension=bq_utils.unnest_district(),
    supervision_type_dimension=bq_utils.unnest_supervision_type(),
    thirty_six_month_filter=bq_utils.thirty_six_month_filter(),
)

if __name__ == "__main__":
    with local_project_id_override(GCP_PROJECT_STAGING):
        EVENT_BASED_REVOCATIONS_VIEW_BUILDER.build_and_print()
