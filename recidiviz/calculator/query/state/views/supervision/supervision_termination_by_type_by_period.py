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
"""Successful and unsuccessful terminations of supervision by metric period month."""
# pylint: disable=trailing-whitespace

from recidiviz.big_query.big_query_view import BigQueryView
from recidiviz.calculator.query import bq_utils
from recidiviz.calculator.query.state import view_config
from recidiviz.utils import metadata

PROJECT_ID = metadata.project_id()
METRICS_DATASET = view_config.DATAFLOW_METRICS_DATASET
REFERENCE_DATASET = view_config.REFERENCE_TABLES_DATASET

SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_VIEW_NAME = 'supervision_termination_by_type_by_period'

SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_DESCRIPTION = """
 Supervision termination by type and by metric period month.
 The counts of supervision that were projected to end in a given month and
 that have ended by now, broken down by whether or not the
 supervision ended because of a revocation or successful completion.
"""

SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_QUERY = \
    """
    /*{description}*/
    SELECT
        state_code, metric_period_months,
        SUM(successful_termination) AS successful_termination,
        SUM(projected_completion_count - successful_termination) AS revocation_termination,
        supervision_type,
        district    
    FROM (
      SELECT 
        state_code, metric_period_months, 
        -- Only count as success if all completed periods were successful per person
        MIN(successful_completion_count) as successful_termination,
        MAX(projected_completion_count) as projected_completion_count,
        supervision_type,
        district
      FROM `{project_id}.{metrics_dataset}.supervision_success_metrics`
      JOIN `{project_id}.{reference_dataset}.most_recent_job_id_by_metric_and_state_code` job
        USING (state_code, job_id, year, month, metric_period_months),
      {district_dimension},
      {supervision_dimension},
      {metric_period_dimension}
      WHERE methodology = 'EVENT'
        AND person_id IS NOT NULL
        AND DATE(year, month, 1) >= DATE_SUB(DATE_TRUNC(CURRENT_DATE('US/Pacific'), MONTH),
                                             INTERVAL metric_period_months - 1 MONTH)
        AND job.metric_type = 'SUPERVISION_SUCCESS'
      GROUP BY state_code, metric_period_months, supervision_type, district, person_id
    )
    WHERE supervision_type in ('ALL', 'PAROLE', 'PROBATION')
    GROUP BY state_code, metric_period_months, supervision_type, district
    ORDER BY state_code, metric_period_months, district, supervision_type
    """.format(
        description=SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_DESCRIPTION,
        project_id=PROJECT_ID,
        reference_dataset=REFERENCE_DATASET,
        metrics_dataset=METRICS_DATASET,
        district_dimension=bq_utils.unnest_district(),
        supervision_dimension=bq_utils.unnest_supervision_type(),
        metric_period_dimension=bq_utils.unnest_metric_period_months(),
    )

SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_VIEW = BigQueryView(
    view_id=SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_VIEW_NAME,
    view_query=SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_QUERY
)

if __name__ == '__main__':
    print(SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_VIEW.view_id)
    print(SUPERVISION_TERMINATION_BY_TYPE_BY_PERIOD_VIEW.view_query)
