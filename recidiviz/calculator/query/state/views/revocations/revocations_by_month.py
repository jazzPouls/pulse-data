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
"""Revocations by month."""
# pylint: disable=trailing-whitespace

from recidiviz.calculator.query import bqview
from recidiviz.calculator.query.state import view_config
from recidiviz.utils import metadata

PROJECT_ID = metadata.project_id()
METRICS_DATASET = view_config.DATAFLOW_METRICS_DATASET
REFERENCE_DATASET = view_config.REFERENCE_TABLES_DATASET

REVOCATIONS_BY_MONTH_VIEW_NAME = 'revocations_by_month'

REVOCATIONS_BY_MONTH_DESCRIPTION = """ Revocations by month """

REVOCATIONS_BY_MONTH_QUERY = \
    """
    /*{description}*/
    SELECT 
      state_code, year, month, 
      IFNULL(rev.count, 0) as revocation_count, 
      pop.count as total_supervision_count,
      supervision_type, 
      supervising_district_external_id as district 
    FROM (
      SELECT 
        state_code, year, month, count, 
        IFNULL(supervision_type, 'ALL') as supervision_type, 
        IFNULL(supervising_district_external_id, 'ALL') as supervising_district_external_id 
      FROM `{project_id}.{metrics_dataset}.supervision_population_metrics`
      INNER JOIN `{project_id}.{reference_dataset}.most_recent_job_id_by_metric_and_state_code` job
        USING (state_code, job_id, year, month, metric_period_months)
      WHERE methodology = 'PERSON'
        AND month IS NOT NULL
        AND metric_period_months = 1
        AND assessment_score_bucket IS NULL
        AND assessment_type IS NULL
        AND supervising_officer_external_id IS NULL
        AND age_bucket IS NULL
        AND race IS NULL
        AND ethnicity IS NULL
        AND gender IS NULL
        AND most_severe_violation_type IS NULL
        AND most_severe_violation_type_subtype IS NULL
        AND response_count IS NULL
        AND case_type IS NULL
        AND person_id IS NULL
        AND person_external_id IS NULL
        AND supervision_level IS NULL
        AND supervision_level_raw_text IS NULL
        AND year >= EXTRACT(YEAR FROM DATE_ADD(CURRENT_DATE(), INTERVAL -3 YEAR))
        AND job.metric_type = 'SUPERVISION_POPULATION'
    ) pop
    LEFT JOIN (
      SELECT 
        state_code, year, month, count, 
        IFNULL(supervision_type, 'ALL') as supervision_type, 
        IFNULL(supervising_district_external_id, 'ALL') as supervising_district_external_id  
      FROM `{project_id}.{metrics_dataset}.supervision_revocation_metrics` rev
      INNER JOIN `{project_id}.{reference_dataset}.most_recent_job_id_by_metric_and_state_code` job
        USING (state_code, job_id, year, month, metric_period_months)
      WHERE methodology = 'PERSON'
        AND month IS NOT NULL
        AND metric_period_months = 1
        AND assessment_score_bucket IS NULL
        AND assessment_type IS NULL
        AND revocation_type IS NULL
        AND source_violation_type IS NULL
        AND supervising_officer_external_id IS NULL
        AND age_bucket IS NULL
        AND race IS NULL
        AND ethnicity IS NULL
        AND gender IS NULL
        AND case_type IS NULL
        AND person_id IS NULL
        AND person_external_id IS NULL
        AND year >= EXTRACT(YEAR FROM DATE_ADD(CURRENT_DATE(), INTERVAL -3 YEAR))
        AND job.metric_type = 'SUPERVISION_REVOCATION'
    ) rev
    USING (state_code, year, month, supervision_type, supervising_district_external_id)
    WHERE supervision_type in ('ALL', 'PAROLE', 'PROBATION')
    ORDER BY state_code, year, month, supervision_type, district
    """.format(
        description=REVOCATIONS_BY_MONTH_DESCRIPTION,
        project_id=PROJECT_ID,
        metrics_dataset=METRICS_DATASET,
        reference_dataset=REFERENCE_DATASET,
        )

REVOCATIONS_BY_MONTH_VIEW = bqview.BigQueryView(
    view_id=REVOCATIONS_BY_MONTH_VIEW_NAME,
    view_query=REVOCATIONS_BY_MONTH_QUERY
)

if __name__ == '__main__':
    print(REVOCATIONS_BY_MONTH_VIEW.view_id)
    print(REVOCATIONS_BY_MONTH_VIEW.view_query)
