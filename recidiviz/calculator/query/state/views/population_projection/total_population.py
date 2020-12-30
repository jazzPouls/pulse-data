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
"""Historical population by compartment and month"""
# pylint: disable=trailing-whitespace
from recidiviz.big_query.big_query_view import SimpleBigQueryViewBuilder
from recidiviz.calculator.query.state import dataset_config
from recidiviz.utils.environment import GCP_PROJECT_STAGING
from recidiviz.utils.metadata import local_project_id_override

TOTAL_POPULATION_VIEW_NAME = 'total_population'

TOTAL_POPULATION_VIEW_DESCRIPTION = \
    """"Historical population by compartment and month"""

TOTAL_POPULATION_QUERY_TEMPLATE = \
    """
    WITH cte AS
    (
        SELECT
          state_code,
          session_id,
          CASE WHEN compartment = 'INCARCERATION - GENERAL' AND previously_incarcerated
            THEN 'INCARCERATION - RE-INCARCERATION'
            ELSE compartment
          END AS compartment,
          gender,
          start_date,
          end_date,
          run_date,
          COUNT(1) as total_population,
        FROM `{project_id}.{population_projection_dataset}.population_projection_sessions_materialized`
        JOIN `{project_id}.{population_projection_dataset}.simulation_run_dates`
          ON start_date < run_date
        WHERE
          state_code = 'US_ID'
          AND (compartment LIKE '%INCARCERATION%' OR compartment LIKE '%SUPERVISION%')
        GROUP BY 1,2,3,4,5,6,7
        ORDER BY 1,2,3,4,5,6,7
    )
    SELECT
      cte.compartment,
      cte.state_code,
      cte.gender,
      cte.run_date,
      time_step,
      SUM(cte.total_population) as total_population
    FROM cte,
    UNNEST(GENERATE_DATE_ARRAY('2000-01-01', DATE_TRUNC(CURRENT_DATE, MONTH), INTERVAL 1 MONTH)) AS time_step
    WHERE
      state_code = 'US_ID'
      AND gender IN ('FEMALE', 'MALE')
      AND time_step BETWEEN cte.start_date AND COALESCE(cte.end_date, '9999-01-01')
    GROUP BY 1,2,3,4,5
    ORDER BY 1,2,3,4,5
    """

TOTAL_POPULATION_VIEW_BUILDER = SimpleBigQueryViewBuilder(
    dataset_id=dataset_config.POPULATION_PROJECTION_DATASET,
    view_id=TOTAL_POPULATION_VIEW_NAME,
    view_query_template=TOTAL_POPULATION_QUERY_TEMPLATE,
    description=TOTAL_POPULATION_VIEW_DESCRIPTION,
    analyst_dataset=dataset_config.ANALYST_VIEWS_DATASET,
    population_projection_dataset=dataset_config.POPULATION_PROJECTION_DATASET,
    should_materialize=False
)

if __name__ == '__main__':
    with local_project_id_override(GCP_PROJECT_STAGING):
        TOTAL_POPULATION_VIEW_BUILDER.build_and_print()
