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
"""Validation view configuration."""

from typing import Sequence

from recidiviz.big_query.big_query_view import BigQueryViewBuilder
from recidiviz.validation.views.state.active_program_participation_by_region_internal_consistency import (
    ACTIVE_PROGRAM_PARTICIPATION_BY_REGION_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.case_termination_by_type_comparison import (
    CASE_TERMINATIONS_BY_TYPE_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.ftr_referrals_comparison import (
    FTR_REFERRALS_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_admission_after_open_period import (
    INCARCERATION_ADMISSION_AFTER_OPEN_PERIOD_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_admission_nulls import (
    INCARCERATION_ADMISSION_NULLS_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_lengths_by_demographics_internal_consistency import (
    INCARCERATION_LENGTHS_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_by_admission_reason_internal_consistency import (
    INCARCERATION_POPULATION_BY_ADMISSION_REASON_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_by_demographic_internal_comparison import (
    INCARCERATION_POPULATION_BY_DEMOGRAPHIC_INTERNAL_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_by_facility_by_demographics_internal_consistency import (
    INCARCERATION_POPULATION_BY_FACILITY_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_by_facility_external_comparison import (
    INCARCERATION_POPULATION_BY_FACILITY_EXTERNAL_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_by_facility_internal_comparison import (
    INCARCERATION_POPULATION_BY_FACILITY_INTERNAL_COMPARISON_VIEW_BUILDER,
)


from recidiviz.validation.views.state.incarceration_population_by_month_internal_comparison import (
    INCARCERATION_POPULATION_BY_MONTH_INTERNAL_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_by_prioritized_race_and_ethnicity_by_period_internal_consistency import (
    INCARCERATION_POPULATION_BY_PRIORITIZED_RACE_AND_ETHNICITY_BY_PERIOD_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_person_level_external_comparison import (
    INCARCERATION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_population_person_level_external_comparison_matching_people import (
    INCARCERATION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_MATCHING_PEOPLE_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_release_prior_to_admission import (
    INCARCERATION_RELEASE_PRIOR_TO_ADMISSION_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_release_reason_no_date import (
    INCARCERATION_RELEASE_REASON_NO_DATE_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_release_reason_no_release_date import (
    INCARCERATION_RELEASE_REASON_NO_RELEASE_DATE_VIEW_BUILDER,
)
from recidiviz.validation.views.state.incarceration_releases_by_type_by_period_internal_consistency import (
    INCARCERATION_RELEASES_BY_TYPE_BY_PERIOD_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.overlapping_incarceration_periods import (
    OVERLAPPING_INCARCERATION_PERIODS_VIEW_BUILDER,
)
from recidiviz.validation.views.state.overlapping_supervision_periods import (
    OVERLAPPING_SUPERVISION_PERIODS_VIEW_BUILDER,
)
from recidiviz.validation.views.state.po_report_avgs_per_district_state import (
    PO_REPORT_AVGS_PER_DISTRICT_STATE_VIEW_BUILDER,
)
from recidiviz.validation.views.state.po_report_clients import (
    PO_REPORT_CLIENTS_VIEW_BUILDER,
)
from recidiviz.validation.views.state.po_report_distinct_by_officer_month import (
    PO_REPORT_DISTINCT_BY_OFFICER_MONTH_VIEW_BUILDER,
)
from recidiviz.validation.views.state.po_report_missing_fields import (
    PO_REPORT_MISSING_FIELDS_VIEW_BUILDER,
)
from recidiviz.validation.views.state.population_projection_data_validation.population_projection_data_validation_view_config import (
    POPULATION_PROJECTION_DATA_VALIDATION_VIEW_BUILDERS_FOR_VIEWS_TO_UPDATE,
)
from recidiviz.validation.views.state.recidivism_release_cohort_person_level_external_comparison import (
    RECIDIVISM_RELEASE_COHORT_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.recidivism_person_level_external_comparison_matching_people import (
    RECIDIVISM_PERSON_LEVEL_EXTERNAL_COMPARISON_MATCHING_PEOPLE_VIEW_BUILDER,
)
from recidiviz.validation.views.state.revocation_matrix_comparison_revocation_cell_vs_caseload import (
    REVOCATION_MATRIX_COMPARISON_REVOCATION_CELL_VS_CASELOAD_VIEW_BUILDER,
)
from recidiviz.validation.views.state.revocation_matrix_comparison_revocation_cell_vs_month import (
    REVOCATION_MATRIX_COMPARISON_REVOCATION_CELL_VS_MONTH_VIEW_BUILDER,
)
from recidiviz.validation.views.state.revocation_matrix_comparison_revocations_by_officer import (
    REVOCATION_MATRIX_COMPARISON_REVOCATIONS_BY_OFFICER_VIEW_BUILDER,
)
from recidiviz.validation.views.state.revocation_matrix_comparison_supervision_population import (
    REVOCATION_MATRIX_COMPARISON_SUPERVISION_POPULATION_VIEW_BUILDER,
)
from recidiviz.validation.views.state.revocation_matrix_distribution_by_gender_comparison import (
    REVOCATION_MATRIX_DISTRIBUTION_BY_GENDER_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.revocation_matrix_distribution_by_race_comparison import (
    REVOCATION_MATRIX_DISTRIBUTION_BY_RACE_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.revocations_by_period_dashboard_comparison import (
    REVOCATIONS_BY_PERIOD_DASHBOARD_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.sentence_type_by_district_by_demographics_internal_consistency import (
    SENTENCE_TYPE_BY_DISTRICT_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_population_by_district_by_demographics_internal_consistency import (
    SUPERVISION_POPULATION_BY_DISTRICT_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)


from recidiviz.validation.views.state.supervision_population_by_prioritized_race_and_ethnicity_by_period_internal_consistency import (
    SUPERVISION_POPULATION_BY_PRIORITIZED_RACE_AND_ETHNICITY_BY_PERIOD_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_population_person_level_external_comparison import (
    SUPERVISION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_population_person_level_external_comparison_matching_people import (
    SUPERVISION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_MATCHING_PEOPLE_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_revocations_by_period_by_type_by_demographics_internal_consistency import (
    SUPERVISION_REVOCATIONS_BY_PERIOD_BY_TYPE_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_success_by_month_dashboard_comparison import (
    SUPERVISION_SUCCESS_BY_MONTH_DASHBOARD_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_success_by_period_by_demographics_internal_consistency import (
    SUPERVISION_SUCCESS_BY_PERIOD_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_success_by_period_dashboard_comparison import (
    SUPERVISION_SUCCESS_BY_PERIOD_DASHBOARD_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_termination_person_level_external_comparison import (
    SUPERVISION_TERMINATION_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_termination_prior_to_start import (
    SUPERVISION_TERMINATION_PRIOR_TO_START_VIEW_BUILDER,
)
from recidiviz.validation.views.state.supervision_termination_reason_no_date import (
    SUPERVISION_TERMINATION_REASON_NO_DATE_VIEW_BUILDER,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_incarceration_population_to_dataflow import (
    SUB_SESSIONS_INCARCERATION_POPULATION_TO_DATAFLOW_VIEW_BUILDER,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_incarceration_population_to_dataflow_disaggregated import (
    SUB_SESSIONS_INCARCERATION_POPULATION_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_supervision_population_to_dataflow import (
    SUB_SESSIONS_SUPERVISION_POPULATION_TO_DATAFLOW_VIEW_BUILDER,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_supervision_population_to_dataflow_disaggregated import (
    SUB_SESSIONS_SUPERVISION_POPULATION_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_incarceration_admissions_to_dataflow import (
    SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_BUILDER,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_incarceration_admissions_to_dataflow_disaggregated import (
    SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_supervision_starts_to_dataflow import (
    SUB_SESSIONS_SUPERVISION_STARTS_TO_DATAFLOW_VIEW_BUILDER,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_supervision_starts_to_dataflow_disaggregated import (
    SUB_SESSIONS_SUPERVISION_STARTS_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_incarceration_releases_to_dataflow import (
    SUB_SESSIONS_INCARCERATION_RELEASES_TO_DATAFLOW_VIEW_BUILDER,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_incarceration_releases_to_dataflow_disaggregated import (
    SUB_SESSIONS_INCARCERATION_RELEASES_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_supervision_terminations_to_dataflow import (
    SUB_SESSIONS_SUPERVISION_TERMINATIONS_TO_DATAFLOW_VIEW_BUILDER,
)
from recidiviz.validation.views.state.analyst_data_validation.sub_sessions_supervision_terminations_to_dataflow_disaggregated import (
    SUB_SESSIONS_SUPERVISION_TERMINATIONS_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
)

VIEW_BUILDERS_FOR_VIEWS_TO_UPDATE: Sequence[BigQueryViewBuilder] = [
    ACTIVE_PROGRAM_PARTICIPATION_BY_REGION_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    CASE_TERMINATIONS_BY_TYPE_COMPARISON_VIEW_BUILDER,
    FTR_REFERRALS_COMPARISON_VIEW_BUILDER,
    INCARCERATION_ADMISSION_AFTER_OPEN_PERIOD_VIEW_BUILDER,
    INCARCERATION_ADMISSION_NULLS_VIEW_BUILDER,
    INCARCERATION_RELEASE_REASON_NO_DATE_VIEW_BUILDER,
    INCARCERATION_LENGTHS_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    INCARCERATION_POPULATION_BY_ADMISSION_REASON_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    INCARCERATION_POPULATION_BY_FACILITY_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    INCARCERATION_POPULATION_BY_FACILITY_EXTERNAL_COMPARISON_VIEW_BUILDER,
    INCARCERATION_POPULATION_BY_FACILITY_INTERNAL_COMPARISON_VIEW_BUILDER,
    INCARCERATION_POPULATION_BY_MONTH_INTERNAL_COMPARISON_VIEW_BUILDER,
    INCARCERATION_POPULATION_BY_PRIORITIZED_RACE_AND_ETHNICITY_BY_PERIOD_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    INCARCERATION_POPULATION_BY_DEMOGRAPHIC_INTERNAL_COMPARISON_VIEW_BUILDER,
    INCARCERATION_RELEASE_PRIOR_TO_ADMISSION_VIEW_BUILDER,
    INCARCERATION_RELEASE_REASON_NO_RELEASE_DATE_VIEW_BUILDER,
    INCARCERATION_RELEASES_BY_TYPE_BY_PERIOD_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    PO_REPORT_AVGS_PER_DISTRICT_STATE_VIEW_BUILDER,
    OVERLAPPING_INCARCERATION_PERIODS_VIEW_BUILDER,
    OVERLAPPING_SUPERVISION_PERIODS_VIEW_BUILDER,
    PO_REPORT_DISTINCT_BY_OFFICER_MONTH_VIEW_BUILDER,
    PO_REPORT_MISSING_FIELDS_VIEW_BUILDER,
    PO_REPORT_CLIENTS_VIEW_BUILDER,
    RECIDIVISM_RELEASE_COHORT_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
    RECIDIVISM_PERSON_LEVEL_EXTERNAL_COMPARISON_MATCHING_PEOPLE_VIEW_BUILDER,
    REVOCATION_MATRIX_COMPARISON_REVOCATION_CELL_VS_CASELOAD_VIEW_BUILDER,
    REVOCATION_MATRIX_COMPARISON_REVOCATION_CELL_VS_MONTH_VIEW_BUILDER,
    REVOCATION_MATRIX_COMPARISON_REVOCATIONS_BY_OFFICER_VIEW_BUILDER,
    REVOCATION_MATRIX_COMPARISON_SUPERVISION_POPULATION_VIEW_BUILDER,
    REVOCATION_MATRIX_DISTRIBUTION_BY_GENDER_COMPARISON_VIEW_BUILDER,
    REVOCATION_MATRIX_DISTRIBUTION_BY_RACE_COMPARISON_VIEW_BUILDER,
    REVOCATIONS_BY_PERIOD_DASHBOARD_COMPARISON_VIEW_BUILDER,
    SENTENCE_TYPE_BY_DISTRICT_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    SUPERVISION_POPULATION_BY_DISTRICT_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    SUPERVISION_POPULATION_BY_PRIORITIZED_RACE_AND_ETHNICITY_BY_PERIOD_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    SUPERVISION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
    SUPERVISION_REVOCATIONS_BY_PERIOD_BY_TYPE_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    SUPERVISION_SUCCESS_BY_MONTH_DASHBOARD_COMPARISON_VIEW_BUILDER,
    SUPERVISION_SUCCESS_BY_PERIOD_DASHBOARD_COMPARISON_VIEW_BUILDER,
    SUPERVISION_SUCCESS_BY_PERIOD_BY_DEMOGRAPHICS_INTERNAL_CONSISTENCY_VIEW_BUILDER,
    SUPERVISION_TERMINATION_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
    SUPERVISION_TERMINATION_PRIOR_TO_START_VIEW_BUILDER,
    SUPERVISION_TERMINATION_REASON_NO_DATE_VIEW_BUILDER,
    INCARCERATION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_VIEW_BUILDER,
    INCARCERATION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_MATCHING_PEOPLE_VIEW_BUILDER,
    SUPERVISION_POPULATION_PERSON_LEVEL_EXTERNAL_COMPARISON_MATCHING_PEOPLE_VIEW_BUILDER,
    SUB_SESSIONS_INCARCERATION_POPULATION_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
    SUB_SESSIONS_INCARCERATION_POPULATION_TO_DATAFLOW_VIEW_BUILDER,
    SUB_SESSIONS_SUPERVISION_POPULATION_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
    SUB_SESSIONS_SUPERVISION_POPULATION_TO_DATAFLOW_VIEW_BUILDER,
    SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
    SUB_SESSIONS_INCARCERATION_ADMISSIONS_TO_DATAFLOW_VIEW_BUILDER,
    SUB_SESSIONS_SUPERVISION_STARTS_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
    SUB_SESSIONS_SUPERVISION_STARTS_TO_DATAFLOW_VIEW_BUILDER,
    SUB_SESSIONS_INCARCERATION_RELEASES_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
    SUB_SESSIONS_INCARCERATION_RELEASES_TO_DATAFLOW_VIEW_BUILDER,
    SUB_SESSIONS_SUPERVISION_TERMINATIONS_TO_DATAFLOW_VIEW_BUILDER_DISAGGREGATED,
    SUB_SESSIONS_SUPERVISION_TERMINATIONS_TO_DATAFLOW_VIEW_BUILDER,
] + POPULATION_PROJECTION_DATA_VALIDATION_VIEW_BUILDERS_FOR_VIEWS_TO_UPDATE
