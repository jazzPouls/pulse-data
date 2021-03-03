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
"""Revocations by metric month period."""
# pylint: disable=trailing-whitespace

from recidiviz.metrics.metric_big_query_view import MetricBigQueryViewBuilder
from recidiviz.calculator.query import bq_utils
from recidiviz.calculator.query.state import dataset_config
from recidiviz.utils.environment import GCP_PROJECT_STAGING
from recidiviz.utils.metadata import local_project_id_override


REVOCATIONS_BY_PERIOD_VIEW_NAME = "revocations_by_period"

REVOCATIONS_BY_PERIOD_DESCRIPTION = """ Revocations by metric month period """

REVOCATIONS_BY_PERIOD_QUERY_TEMPLATE = """
    /*{description}*/
    SELECT
      state_code,
      metric_period_months,
      IFNULL(revocation_count, 0) as revocation_count,
      total_supervision_count,
      supervision_type,
      district
    FROM (
      SELECT
        state_code, metric_period_months,
        COUNT(DISTINCT person_id) AS total_supervision_count,
        supervision_type,
        district
      FROM `{project_id}.{reference_views_dataset}.event_based_supervision_populations`,
      {metric_period_dimension}
      WHERE {metric_period_condition}
      GROUP BY state_code, metric_period_months, supervision_type, district
    ) pop
    LEFT JOIN (
      SELECT
        state_code, metric_period_months,
        COUNT(DISTINCT person_id) AS revocation_count,
        supervision_type,
        district
      FROM `{project_id}.{reference_views_dataset}.event_based_revocations`,
      {metric_period_dimension}
      WHERE {metric_period_condition}
      GROUP BY state_code, metric_period_months, supervision_type, district
    ) rev
    USING (state_code, metric_period_months, supervision_type, district)
    WHERE supervision_type in ('ALL', 'PAROLE', 'PROBATION')
    ORDER BY state_code, district, supervision_type, metric_period_months
    """

REVOCATIONS_BY_PERIOD_VIEW_BUILDER = MetricBigQueryViewBuilder(
    dataset_id=dataset_config.DASHBOARD_VIEWS_DATASET,
    view_id=REVOCATIONS_BY_PERIOD_VIEW_NAME,
    view_query_template=REVOCATIONS_BY_PERIOD_QUERY_TEMPLATE,
    dimensions=["state_code", "metric_period_months", "supervision_type", "district"],
    description=REVOCATIONS_BY_PERIOD_DESCRIPTION,
    reference_views_dataset=dataset_config.REFERENCE_VIEWS_DATASET,
    metric_period_dimension=bq_utils.unnest_metric_period_months(),
    metric_period_condition=bq_utils.metric_period_condition(),
)

if __name__ == "__main__":
    with local_project_id_override(GCP_PROJECT_STAGING):
        REVOCATIONS_BY_PERIOD_VIEW_BUILDER.build_and_print()
