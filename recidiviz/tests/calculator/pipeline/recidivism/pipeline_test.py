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

# pylint: disable=unused-import,wrong-import-order

"""Tests for recidivism/pipeline.py."""
import unittest
from typing import Optional, Set

import apache_beam as beam
import pytest
from apache_beam.pvalue import AsDict
from apache_beam.testing.util import assert_that, equal_to, BeamAssertException
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.options.pipeline_options import PipelineOptions

import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum

from freezegun import freeze_time

from recidiviz.calculator.pipeline.recidivism import pipeline
from recidiviz.calculator.pipeline.recidivism.metrics import \
    ReincarcerationRecidivismMetric, \
    ReincarcerationRecidivismRateMetric, ReincarcerationRecidivismMetricType
from recidiviz.calculator.pipeline.recidivism.metrics import \
    ReincarcerationRecidivismMetricType as MetricType
from recidiviz.calculator.pipeline.utils.beam_utils import RecidivizMetricWritableDict
from recidiviz.calculator.pipeline.recidivism.release_event import \
    ReincarcerationReturnType, RecidivismReleaseEvent, \
    NonRecidivismReleaseEvent
from recidiviz.calculator.pipeline.utils.person_utils import PersonMetadata
from recidiviz.common.constants.person_characteristics import Ethnicity, ResidencyStatus, Gender, Race
from recidiviz.common.constants.state.state_incarceration import StateIncarcerationType
from recidiviz.common.constants.state.state_incarceration_period import \
    StateIncarcerationPeriodStatus, StateIncarcerationPeriodAdmissionReason, \
    StateIncarcerationPeriodReleaseReason, \
    StateIncarcerationFacilitySecurityLevel
from recidiviz.persistence.database.schema.state import schema
from recidiviz.persistence.entity.state import entities
from recidiviz.tests.calculator.calculator_test_utils import \
    normalized_database_base_dict, normalized_database_base_dict_list
from recidiviz.tests.calculator.pipeline.fake_bigquery import FakeReadFromBigQueryFactory, FakeWriteToBigQuery, \
    FakeWriteToBigQueryFactory, DataTablesDict
from recidiviz.tests.calculator.pipeline.utils.run_pipeline_test_utils import run_test_pipeline
from recidiviz.tests.persistence.database import database_test_utils

_COUNTY_OF_RESIDENCE = 'county'

ALL_METRIC_INCLUSIONS_DICT = {
    MetricType.REINCARCERATION_COUNT: True,
    MetricType.REINCARCERATION_RATE: True
}


class TestRecidivismPipeline(unittest.TestCase):
    """Tests the entire recidivism pipeline."""
    def setUp(self) -> None:
        self.fake_bq_source_factory = FakeReadFromBigQueryFactory()
        self.fake_bq_sink_factory = FakeWriteToBigQueryFactory(FakeWriteToBigQuery)

    @staticmethod
    def build_data_dict(fake_person_id: int):
        """Builds a data_dict for a basic run of the pipeline."""
        fake_person = schema.StatePerson(
            state_code='US_XX',
            person_id=fake_person_id, gender=Gender.MALE,
            birthdate=date(1970, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        persons_data = [normalized_database_base_dict(fake_person)]

        race_1 = schema.StatePersonRace(
            person_race_id=111,
            state_code='US_XX',
            race=Race.BLACK,
            person_id=fake_person_id
        )

        race_2 = schema.StatePersonRace(
            person_race_id=111,
            state_code='ND',
            race=Race.WHITE,
            person_id=fake_person_id
        )

        races_data = normalized_database_base_dict_list([race_1, race_2])

        ethnicity = schema.StatePersonEthnicity(
            person_ethnicity_id=111,
            state_code='US_XX',
            ethnicity=Ethnicity.HISPANIC,
            person_id=fake_person_id)

        ethnicity_data = normalized_database_base_dict_list([ethnicity])

        initial_incarceration = schema.StateIncarcerationPeriod(
            incarceration_period_id=1111,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            county_code='124',
            facility='San Quentin',
            facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            admission_date=date(2008, 11, 20),
            release_date=date(2010, 12, 4),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
            person_id=fake_person_id
        )

        first_reincarceration = schema.StateIncarcerationPeriod(
            incarceration_period_id=2222,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            county_code='124',
            facility='San Quentin',
            facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            admission_date=date(2011, 4, 5),
            release_date=date(2014, 4, 14),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
            person_id=fake_person_id)

        subsequent_reincarceration = schema.StateIncarcerationPeriod(
            incarceration_period_id=3333,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.IN_CUSTODY,
            state_code='US_XX',
            county_code='124',
            facility='San Quentin',
            facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            admission_date=date(2017, 1, 4),
            person_id=fake_person_id)

        incarceration_periods_data = [
            normalized_database_base_dict(initial_incarceration),
            normalized_database_base_dict(first_reincarceration),
            normalized_database_base_dict(subsequent_reincarceration)
        ]

        supervision_violation_response = \
            database_test_utils.generate_test_supervision_violation_response(
                fake_person_id)

        state_agent = database_test_utils.generate_test_assessment_agent()

        supervision_violation_response.decision_agents = [state_agent]

        supervision_violation = \
            database_test_utils.generate_test_supervision_violation(
                fake_person_id, [supervision_violation_response])

        supervision_violation_response.supervision_violation_id = \
            supervision_violation.supervision_violation_id

        supervision_violation_response_data = [
            normalized_database_base_dict(supervision_violation_response)
        ]

        supervision_violation_data = [
            normalized_database_base_dict(supervision_violation)
        ]

        fake_person_id_to_county_query_result = [
            {'state_code': 'US_XX',
             'person_id': fake_person_id,
             'county_of_residence': _COUNTY_OF_RESIDENCE}]

        state_race_ethnicity_population_count_data = [{
            'state_code': 'US_XX',
            'race_or_ethnicity': 'BLACK',
            'population_count': 1,
            'representation_priority': 1
        }]

        data_dict = {
            schema.StatePerson.__tablename__: persons_data,
            schema.StatePersonRace.__tablename__: races_data,
            schema.StatePersonEthnicity.__tablename__: ethnicity_data,
            schema.StateIncarcerationPeriod.__tablename__: incarceration_periods_data,
            schema.StateSupervisionViolationResponse.__tablename__: supervision_violation_response_data,
            schema.StateSupervisionViolation.__tablename__: supervision_violation_data,
            schema.StateAssessment.__tablename__: [],
            schema.StatePersonExternalId.__tablename__: [],
            schema.StatePersonAlias.__tablename__: [],
            schema.StateSentenceGroup.__tablename__: [],
            schema.StateProgramAssignment.__tablename__: [],
            schema.StateFine.__tablename__: [],
            schema.StateIncarcerationIncident.__tablename__: [],
            schema.StateParoleDecision.__tablename__: [],
            schema.StateSupervisionViolationTypeEntry.__tablename__: [],
            schema.StateSupervisionViolatedConditionEntry.__tablename__: [],
            schema.StateSupervisionViolationResponseDecisionEntry.__tablename__: [],
            schema.state_incarceration_period_program_assignment_association_table.name: [],
            'persons_to_recent_county_of_residence': fake_person_id_to_county_query_result,
            'state_race_ethnicity_population_counts': state_race_ethnicity_population_count_data,
        }

        return data_dict

    def testRecidivismPipeline(self):
        """Tests the entire recidivism pipeline with one person and three
        incarceration periods."""

        fake_person_id = 12345

        data_dict = self.build_data_dict(fake_person_id)

        dataset = 'recidiviz-123.state'

        self.run_test_pipeline(dataset, data_dict)

    def testRecidivismPipelineWithFilterSet(self):
        """Tests the entire recidivism pipeline with one person and three
        incarceration periods."""

        fake_person_id = 12345

        data_dict = self.build_data_dict(fake_person_id)

        dataset = 'recidiviz-123.state'

        self.run_test_pipeline(dataset, data_dict)

    def testRecidivismPipeline_WithConditionalReturns(self):
        """Tests the entire RecidivismPipeline with two person and three
        incarceration periods each. One entities.StatePerson has a return from a
        technical supervision violation.
        """

        fake_person_id_1 = 12345

        fake_person_1 = schema.StatePerson(
            state_code='US_XX',
            person_id=fake_person_id_1, gender=Gender.MALE,
            birthdate=date(1970, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        fake_person_id_2 = 6789

        fake_person_2 = schema.StatePerson(
            state_code='US_XX',
            person_id=fake_person_id_2, gender=Gender.FEMALE,
            birthdate=date(1990, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        persons_data = [normalized_database_base_dict(fake_person_1),
                        normalized_database_base_dict(fake_person_2)]

        initial_incarceration_1 = schema.StateIncarcerationPeriod(
            incarceration_period_id=1111,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            county_code='124',
            facility='San Quentin',
            facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            admission_date=date(2008, 11, 20),
            release_date=date(2010, 12, 4),
            release_reason=StateIncarcerationPeriodReleaseReason.
            SENTENCE_SERVED,
            person_id=fake_person_id_1)

        first_reincarceration_1 = schema.StateIncarcerationPeriod(
            incarceration_period_id=2222,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            county_code='124',
            facility='San Quentin',
            facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            admission_date=date(2011, 4, 5),
            release_date=date(2014, 4, 14),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
            person_id=fake_person_id_1)

        subsequent_reincarceration_1 = \
            schema.StateIncarcerationPeriod(
                incarceration_period_id=3333,
                incarceration_type=StateIncarcerationType.STATE_PRISON,
                status=StateIncarcerationPeriodStatus.IN_CUSTODY,
                state_code='US_XX',
                county_code='124',
                facility='San Quentin',
                facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
                admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
                projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
                admission_date=date(2017, 1, 4),
                person_id=fake_person_id_1)

        initial_incarceration_2 = schema.StateIncarcerationPeriod(
            incarceration_period_id=4444,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            county_code='124',
            facility='San Quentin',
            facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            admission_date=date(2004, 12, 20),
            release_date=date(2010, 6, 3),
            release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            person_id=fake_person_id_2)

        supervision_violation_response = \
            database_test_utils.generate_test_supervision_violation_response(
                fake_person_id_2)

        supervision_violation = \
            database_test_utils.generate_test_supervision_violation(
                fake_person_id_2, [supervision_violation_response])

        supervision_violation_response.supervision_violation_id = \
            supervision_violation.supervision_violation_id

        supervision_violation_response_data = [
            normalized_database_base_dict(supervision_violation_response)
        ]

        supervision_violation_data = [
            normalized_database_base_dict(supervision_violation)
        ]

        first_reincarceration_2 = schema.StateIncarcerationPeriod(
            incarceration_period_id=5555,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            county_code='124',
            facility='San Quentin',
            facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
            admission_reason=StateIncarcerationPeriodAdmissionReason.PAROLE_REVOCATION,
            projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
            admission_date=date(2011, 4, 5),
            release_date=date(2014, 1, 4),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
            source_supervision_violation_response_id=
            supervision_violation_response.supervision_violation_response_id,
            person_id=fake_person_id_2)

        subsequent_reincarceration_2 = \
            schema.StateIncarcerationPeriod(
                incarceration_period_id=6666,
                incarceration_type=StateIncarcerationType.STATE_PRISON,
                status=StateIncarcerationPeriodStatus.IN_CUSTODY,
                state_code='US_XX',
                county_code='124',
                facility='San Quentin',
                facility_security_level=StateIncarcerationFacilitySecurityLevel.MAXIMUM,
                admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
                projected_release_reason=StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
                admission_date=date(2018, 3, 9),
                person_id=fake_person_id_2)

        incarceration_periods_data = [
            normalized_database_base_dict(initial_incarceration_1),
            normalized_database_base_dict(first_reincarceration_1),
            normalized_database_base_dict(subsequent_reincarceration_1),
            normalized_database_base_dict(initial_incarceration_2),
            normalized_database_base_dict(first_reincarceration_2),
            normalized_database_base_dict(subsequent_reincarceration_2)
        ]

        fake_person_id_to_county_query_result = [
            {'state_code': 'US_XX',
             'person_id': fake_person_id_1,
             'county_of_residence': _COUNTY_OF_RESIDENCE}]

        state_race_ethnicity_population_count_data = [{
            'state_code': 'US_XX',
            'race_or_ethnicity': 'BLACK',
            'population_count': 1,
            'representation_priority': 1
        }]

        data_dict = {
            schema.StatePerson.__tablename__: persons_data,
            schema.StateIncarcerationPeriod.__tablename__: incarceration_periods_data,
            schema.StateSupervisionViolationResponse.__tablename__: supervision_violation_response_data,
            schema.StateSupervisionViolation.__tablename__: supervision_violation_data,
            schema.StateAssessment.__tablename__: [],
            schema.StatePersonExternalId.__tablename__: [],
            schema.StatePersonAlias.__tablename__: [],
            schema.StatePersonRace.__tablename__: [],
            schema.StatePersonEthnicity.__tablename__: [],
            schema.StateSentenceGroup.__tablename__: [],
            schema.StateProgramAssignment.__tablename__: [],
            schema.StateFine.__tablename__: [],
            schema.StateIncarcerationIncident.__tablename__: [],
            schema.StateParoleDecision.__tablename__: [],
            schema.StateSupervisionViolationTypeEntry.__tablename__: [],
            schema.StateSupervisionViolatedConditionEntry.__tablename__: [],
            schema.StateSupervisionViolationResponseDecisionEntry.__tablename__: [],
            schema.state_incarceration_period_program_assignment_association_table.name: [],
            'persons_to_recent_county_of_residence': fake_person_id_to_county_query_result,
            'state_race_ethnicity_population_counts': state_race_ethnicity_population_count_data,
        }
        dataset = 'recidiviz-123.state'

        self.run_test_pipeline(dataset, data_dict)

    def run_test_pipeline(self,
                          dataset: str,
                          data_dict: DataTablesDict,
                          unifying_id_field_filter_set: Optional[Set[int]] = None,
                          metric_types_filter: Optional[Set[str]] = None):
        """Runs a test version of the recidivism pipeline."""

        expected_metric_types: Set[MetricType] = {
            ReincarcerationRecidivismMetricType.REINCARCERATION_RATE,
            ReincarcerationRecidivismMetricType.REINCARCERATION_COUNT
        }

        read_from_bq_constructor = self.fake_bq_source_factory.create_fake_bq_source_constructor(dataset, data_dict)
        write_to_bq_constructor = self.fake_bq_sink_factory.create_fake_bq_sink_constructor(
            dataset,
            expected_output_metric_types=expected_metric_types,
        )

        run_test_pipeline(
            pipeline_module=pipeline,
            state_code='US_XX',
            dataset=dataset,
            read_from_bq_constructor=read_from_bq_constructor,
            write_to_bq_constructor=write_to_bq_constructor,
            unifying_id_field_filter_set=unifying_id_field_filter_set,
            metric_types_filter=metric_types_filter,
            include_calculation_limit_args=False
        )


class TestClassifyReleaseEvents(unittest.TestCase):
    """Tests the ClassifyReleaseEvents DoFn in the pipeline."""

    def testClassifyReleaseEvents(self):
        """Tests the ClassifyReleaseEvents DoFn when there are two instances
        of recidivism."""

        fake_person_id = 12345

        fake_person = entities.StatePerson.new_with_defaults(
            state_code='US_XX',
            person_id=fake_person_id, gender=Gender.MALE,
            birthdate=date(1970, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        initial_incarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=1111,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2008, 11, 20),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            release_date=date(2010, 12, 4),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED)

        first_reincarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=2222,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            state_code='US_XX',
            admission_date=date(2011, 4, 5),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            release_date=date(2014, 4, 14),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED)

        subsequent_reincarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=3333,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2017, 1, 4),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION)

        fake_person_id_to_county_query_result = {
            'person_id': fake_person_id,
            'county_of_residence': _COUNTY_OF_RESIDENCE
        }

        person_incarceration_periods = {
            'person': [fake_person],
            'incarceration_periods': [
                initial_incarceration,
                first_reincarceration,
                subsequent_reincarceration
            ],
            'persons_to_recent_county_of_residence': [fake_person_id_to_county_query_result]
        }

        first_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=initial_incarceration.admission_date,
            release_date=initial_incarceration.release_date,
            release_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            reincarceration_date=first_reincarceration.admission_date,
            reincarceration_facility=None,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        second_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=first_reincarceration.admission_date,
            release_date=first_reincarceration.release_date,
            release_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            reincarceration_date=subsequent_reincarceration.admission_date,
            reincarceration_facility=None,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        correct_output = [
            (fake_person.person_id, (
                fake_person, {initial_incarceration.release_date.year: [first_recidivism_release_event],
                              first_reincarceration.release_date.year: [second_recidivism_release_event]}
            )
             )
        ]

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([(fake_person_id,
                                  person_incarceration_periods)])
                  | 'Identify Recidivism Events' >>
                  beam.ParDo(pipeline.ClassifyReleaseEvents()))

        assert_that(output, equal_to(correct_output))

        test_pipeline.run()

    def testClassifyReleaseEvents_NoRecidivism(self):
        """Tests the ClassifyReleaseEvents DoFn in the pipeline when there
        is no instance of recidivism."""

        fake_person_id = 12345

        fake_person = entities.StatePerson.new_with_defaults(
            state_code='US_XX',
            person_id=fake_person_id, gender=Gender.MALE,
            birthdate=date(1970, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        only_incarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=1111,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX', admission_date=date(2008, 11, 20),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            release_date=date(2010, 12, 4),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED)

        fake_person_id_to_county_query_result = {'person_id': fake_person_id,
                                                 'county_of_residence': _COUNTY_OF_RESIDENCE}

        person_incarceration_periods = {
            'person': [fake_person],
            'incarceration_periods': [only_incarceration],
            'persons_to_recent_county_of_residence': [fake_person_id_to_county_query_result],
        }

        non_recidivism_release_event = NonRecidivismReleaseEvent(
            'US_XX', only_incarceration.admission_date,
            only_incarceration.release_date, only_incarceration.facility,
            _COUNTY_OF_RESIDENCE)

        correct_output = [(fake_person.person_id, (fake_person,
                           {only_incarceration.release_date.year:
                            [non_recidivism_release_event]}))]

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([(fake_person_id,
                                  person_incarceration_periods)])
                  | 'Identify Recidivism Events' >>
                  beam.ParDo(pipeline.ClassifyReleaseEvents()))

        assert_that(output, equal_to(correct_output))

        test_pipeline.run()

    def testClassifyReleaseEvents_NoIncarcerationPeriods(self):
        """Tests the ClassifyReleaseEvents DoFn in the pipeline when there
        are no incarceration periods. The person in this case should be
        excluded from the calculations."""

        fake_person_id = 12345

        fake_person = entities.StatePerson.new_with_defaults(
            state_code='US_XX',
            person_id=fake_person_id, gender=Gender.MALE,
            birthdate=date(1970, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        fake_person_id_to_county_query_result = {'person_id': fake_person_id,
                                                 'county_of_residence': _COUNTY_OF_RESIDENCE}

        person_incarceration_periods = {
            'person': [fake_person],
            'incarceration_periods': [],
            'persons_to_recent_county_of_residence': [fake_person_id_to_county_query_result],
        }

        correct_output = []

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([(fake_person_id,
                                  person_incarceration_periods)])
                  | 'Identify Recidivism Events' >>
                  beam.ParDo(pipeline.ClassifyReleaseEvents()))

        assert_that(output, equal_to(correct_output))

        test_pipeline.run()

    def testClassifyReleaseEvents_TwoReleasesSameYear(self):
        """Tests the ClassifyReleaseEvents DoFn in the pipeline when a person
        is released twice in the same calendar year."""

        fake_person_id = 12345

        fake_person = entities.StatePerson.new_with_defaults(
            state_code='US_XX',
            person_id=fake_person_id, gender=Gender.MALE,
            birthdate=date(1970, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        initial_incarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=1111,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2008, 11, 20),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            release_date=date(2010, 1, 4),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED)

        first_reincarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=2222,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2010, 4, 5),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            release_date=date(2010, 10, 14),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED)

        subsequent_reincarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=3333,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2017, 1, 4),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
        )

        fake_person_id_to_county_query_result = {'person_id': fake_person_id,
                                                 'county_of_residence': _COUNTY_OF_RESIDENCE}

        person_incarceration_periods = {
            'person': [fake_person],
            'incarceration_periods': [
                initial_incarceration,
                first_reincarceration,
                subsequent_reincarceration
            ],
            'persons_to_recent_county_of_residence': [fake_person_id_to_county_query_result],
        }

        first_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=initial_incarceration.admission_date,
            release_date=initial_incarceration.release_date,
            release_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            reincarceration_date=first_reincarceration.admission_date,
            reincarceration_facility=None,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        second_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=first_reincarceration.admission_date,
            release_date=first_reincarceration.release_date,
            release_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            reincarceration_date=subsequent_reincarceration.admission_date,
            reincarceration_facility=None,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        correct_output = [
            (fake_person.person_id, (fake_person, {initial_incarceration.release_date.year:
                           [first_recidivism_release_event,
                            second_recidivism_release_event]}))]

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([(fake_person_id,
                                  person_incarceration_periods)])
                  | 'Identify Recidivism Events' >>
                  beam.ParDo(pipeline.ClassifyReleaseEvents()))

        assert_that(output, equal_to(correct_output))

        test_pipeline.run()

    def testClassifyReleaseEvents_WrongOrder(self):
        """Tests the ClassifyReleaseEvents DoFn when there are two instances
        of recidivism."""

        fake_person_id = 12345

        fake_person = entities.StatePerson.new_with_defaults(
            state_code='US_XX',
            person_id=fake_person_id, gender=Gender.MALE,
            birthdate=date(1970, 1, 1),
            residency_status=ResidencyStatus.PERMANENT)

        initial_incarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=1111,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2008, 11, 20),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            release_date=date(2010, 12, 4),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED)

        first_reincarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=2222,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2011, 4, 5),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
            release_date=date(2014, 4, 14),
            release_reason=StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED)

        subsequent_reincarceration = entities.StateIncarcerationPeriod.new_with_defaults(
            incarceration_period_id=3333,
            incarceration_type=StateIncarcerationType.STATE_PRISON,
            status=StateIncarcerationPeriodStatus.IN_CUSTODY,
            state_code='US_XX',
            admission_date=date(2017, 1, 4),
            admission_reason=StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION)

        fake_person_id_to_county_query_result = {'person_id': fake_person_id,
                                                 'county_of_residence': _COUNTY_OF_RESIDENCE}

        person_incarceration_periods = {
            'person': [fake_person],
            'incarceration_periods': [
                subsequent_reincarceration,
                initial_incarceration,
                first_reincarceration
            ],
            'persons_to_recent_county_of_residence': [fake_person_id_to_county_query_result],
        }

        first_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=initial_incarceration.admission_date,
            release_date=initial_incarceration.release_date,
            release_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            reincarceration_date=first_reincarceration.admission_date,
            reincarceration_facility=None,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        second_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=first_reincarceration.admission_date,
            release_date=first_reincarceration.release_date,
            release_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            reincarceration_date=subsequent_reincarceration.admission_date,
            reincarceration_facility=None,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        correct_output = [
            (fake_person.person_id, (fake_person, {
                initial_incarceration.release_date.year: [first_recidivism_release_event],
                first_reincarceration.release_date.year: [second_recidivism_release_event]}))]

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([(fake_person_id,
                                  person_incarceration_periods)])
                  | 'Identify Recidivism Events' >>
                  beam.ParDo(pipeline.ClassifyReleaseEvents()))

        assert_that(output, equal_to(correct_output))

        test_pipeline.run()


class TestCalculateRecidivismMetricCombinations(unittest.TestCase):
    """Tests for the CalculateRecidivismMetricCombinations DoFn in the
    pipeline."""

    def setUp(self) -> None:
        self.fake_person_id = 12345

        self.person_metadata = PersonMetadata(prioritized_race_or_ethnicity='BLACK')

    # TODO(#4813): This fails on dates after 2020-12-03 - is this a bug in the pipeline or in the test code?
    @freeze_time('2020-12-03')
    def testCalculateRecidivismMetricCombinations(self):
        """Tests the CalculateRecidivismMetricCombinations DoFn in the pipeline."""
        fake_person = entities.StatePerson.new_with_defaults(
            state_code='US_XX',
            person_id=self.fake_person_id, gender=Gender.MALE,
            residency_status=ResidencyStatus.PERMANENT)

        first_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=date(2008, 11, 20),
            release_date=date(2010, 12, 4), release_facility=None,
            reincarceration_date=date(2011, 4, 5),
            reincarceration_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        second_recidivism_release_event = RecidivismReleaseEvent(
            state_code='US_XX',
            original_admission_date=date(2011, 4, 5),
            release_date=date(2014, 4, 14), release_facility=None,
            reincarceration_date=date(2017, 1, 4),
            reincarceration_facility=None,
            county_of_residence=_COUNTY_OF_RESIDENCE,
            return_type=ReincarcerationReturnType.NEW_ADMISSION)

        person_release_events = [
            (fake_person, {first_recidivism_release_event.release_date.year:
                           [first_recidivism_release_event],
                           second_recidivism_release_event.release_date.year:
                               [second_recidivism_release_event]})]

        inputs = [(self.fake_person_id, {
            'person_events': person_release_events,
            'person_metadata': [self.person_metadata]
        })]

        # We do not track metrics for periods that start after today, so we need to subtract for some number of periods
        # that go beyond whatever today is.
        periods = relativedelta(date.today(), date(2010, 12, 4)).years + 1
        periods_with_single = 6
        periods_with_double = periods - periods_with_single

        expected_combinations_count_2010 = (periods_with_single + (2 * periods_with_double))

        periods = relativedelta(date.today(), date(2014, 4, 14)).years + 1

        expected_combinations_count_2014 = periods

        # Add count metrics for the 2 events
        expected_count_metric_combinations = 2

        expected_combination_counts = {
            2010: expected_combinations_count_2010,
            2014: expected_combinations_count_2014,
            'counts': expected_count_metric_combinations
        }

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create(inputs)
                  | beam.ParDo(pipeline.ExtractPersonReleaseEventsMetadata())
                  | 'Calculate Metric Combinations' >>
                  beam.ParDo(pipeline.CalculateRecidivismMetricCombinations(), ALL_METRIC_INCLUSIONS_DICT)
                  )

        assert_that(output, AssertMatchers.count_combinations(expected_combination_counts),
                    'Assert number of metrics is expected value')

        test_pipeline.run()

    def testCalculateRecidivismMetricCombinations_NoResults(self):
        """Tests the CalculateRecidivismMetricCombinations DoFn in the pipeline
        when there are no ReleaseEvents associated with the entities.StatePerson."""
        fake_person = entities.StatePerson.new_with_defaults(
            state_code='US_XX',
            person_id=self.fake_person_id, gender=Gender.MALE,
            residency_status=ResidencyStatus.PERMANENT)

        person_release_events = [(fake_person, {})]

        inputs = [(self.fake_person_id, {
            'person_events': person_release_events,
            'person_metadata': [self.person_metadata]
        })]

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create(inputs)
                  | beam.ParDo(pipeline.ExtractPersonReleaseEventsMetadata())
                  | 'Calculate Metric Combinations' >>
                  beam.ParDo(pipeline.CalculateRecidivismMetricCombinations(), ALL_METRIC_INCLUSIONS_DICT)
                  )

        assert_that(output, equal_to([]))

        test_pipeline.run()

    def testCalculateRecidivismMetricCombinations_NoPersonEvents(self):
        """Tests the CalculateRecidivismMetricCombinations DoFn in the pipeline
        when there is no entities.StatePerson and no ReleaseEvents."""

        inputs = []

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create(inputs)
                  | beam.ParDo(pipeline.ExtractPersonReleaseEventsMetadata())
                  | 'Calculate Metric Combinations' >>
                  beam.ParDo(pipeline.CalculateRecidivismMetricCombinations(), ALL_METRIC_INCLUSIONS_DICT)
                  )

        assert_that(output, equal_to([]))

        test_pipeline.run()

    def testProduceReincarcerationRecidivismMetric_EmptyMetric(self):
        """Tests the ProduceReincarcerationRecidivismMetric DoFn in the
        pipeline when the metric dictionary is empty.

        This should not happen in the pipeline, but we test against it
        anyways.
        """

        metric_key_dict = {}

        value = 100

        test_pipeline = TestPipeline()

        all_pipeline_options = PipelineOptions().get_all_options()

        job_timestamp = datetime.datetime.now().strftime(
            '%Y-%m-%d_%H_%M_%S.%f')
        all_pipeline_options['job_timestamp'] = job_timestamp

        # This should never happen, and we want the pipeline to fail loudly if it does.
        with pytest.raises(ValueError):
            _ = (test_pipeline
                 | beam.Create([(metric_key_dict, value)])
                 | 'Produce Recidivism Metric' >>
                 beam.ParDo(
                     pipeline.ProduceReincarcerationRecidivismMetric(),
                     **all_pipeline_options))

            test_pipeline.run()


class TestRecidivismMetricWritableDict(unittest.TestCase):
    """Tests the RecidivismMetricWritableDict DoFn in the pipeline."""

    def testRecidivismMetricWritableDict(self):
        """Tests converting the ReincarcerationRecidivismMetric to a dictionary
        that can be written to BigQuery."""
        metric = MetricGroup.recidivism_metric_with_race

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([metric])
                  | 'Convert to writable dict' >>
                  beam.ParDo(RecidivizMetricWritableDict()))

        assert_that(output, AssertMatchers.validate_metric_writable_dict())

        test_pipeline.run()

    def testRecidivismMetricWritableDict_WithDateField(self):
        """Tests converting the ReincarcerationRecidivismMetric to a dictionary
        that can be written to BigQuery, where the metric contains a date
        attribute."""
        metric = MetricGroup.recidivism_metric_without_dimensions
        metric.created_on = date.today()

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([metric])
                  | 'Convert to writable dict' >>
                  beam.ParDo(RecidivizMetricWritableDict()))

        assert_that(output, AssertMatchers.
                    validate_metric_writable_dict())

        test_pipeline.run()

    def testRecidivismMetricWritableDict_WithEmptyDateField(self):
        """Tests converting the ReincarcerationRecidivismMetric to a dictionary
        that can be written to BigQuery, where the metric contains None on a
        date attribute."""
        metric = MetricGroup.recidivism_metric_without_dimensions
        metric.created_on = None

        test_pipeline = TestPipeline()

        output = (test_pipeline
                  | beam.Create([metric])
                  | 'Convert to writable dict' >>
                  beam.ParDo(RecidivizMetricWritableDict()))

        assert_that(output, AssertMatchers.
                    validate_metric_writable_dict())

        test_pipeline.run()


class MetricGroup:
    """Stores a set of metrics where every dimension is included for testing
    dimension filtering."""
    recidivism_metric_with_age = ReincarcerationRecidivismRateMetric(
        job_id='12345', state_code='US_XX', release_cohort=2015,
        follow_up_period=1, age_bucket='25-29', did_recidivate=True)

    recidivism_metric_with_gender = ReincarcerationRecidivismRateMetric(
        job_id='12345', state_code='US_XX', release_cohort=2015,
        follow_up_period=1, gender=Gender.MALE, did_recidivate=True)

    recidivism_metric_with_race = ReincarcerationRecidivismRateMetric(
        job_id='12345', state_code='US_XX', release_cohort=2015,
        follow_up_period=1, did_recidivate=True)

    recidivism_metric_with_ethnicity = ReincarcerationRecidivismRateMetric(
        job_id='12345', state_code='US_XX', release_cohort=2015,
        follow_up_period=1, did_recidivate=True)

    recidivism_metric_with_release_facility = \
        ReincarcerationRecidivismRateMetric(
            job_id='12345', state_code='US_XX', release_cohort=2015,
            follow_up_period=1, release_facility='Red', did_recidivate=True)

    recidivism_metric_with_stay_length = ReincarcerationRecidivismRateMetric(
        job_id='12345', state_code='US_XX', release_cohort=2015,
        follow_up_period=1, stay_length_bucket='12-24', did_recidivate=True)

    recidivism_metric_without_dimensions = ReincarcerationRecidivismRateMetric(
        job_id='12345', state_code='US_XX', release_cohort=2015,
        follow_up_period=1, did_recidivate=True)

    recidivism_metric_event_based = ReincarcerationRecidivismRateMetric(
        job_id='12345', state_code='US_XX', release_cohort=2015,
        follow_up_period=1, did_recidivate=True)

    @staticmethod
    def get_list():
        return [MetricGroup.recidivism_metric_with_age,
                MetricGroup.recidivism_metric_with_gender,
                MetricGroup.recidivism_metric_with_race,
                MetricGroup.recidivism_metric_with_ethnicity,
                MetricGroup.recidivism_metric_with_release_facility,
                MetricGroup.recidivism_metric_with_stay_length,
                MetricGroup.recidivism_metric_without_dimensions,
                MetricGroup.recidivism_metric_event_based]


class AssertMatchers:
    """Functions to be used by Apache Beam testing `assert_that` functions to
    validate pipeline outputs."""

    @staticmethod
    def validate_pipeline_test():

        def _validate_pipeline_test(output):

            for metric in output:
                if not isinstance(metric, ReincarcerationRecidivismMetric):
                    raise BeamAssertException(
                        'Failed assert. Output is not'
                        'of type'
                        ' ReincarcerationRecidivismMetric.')

        return _validate_pipeline_test

    @staticmethod
    def count_combinations(expected_combination_counts):
        """Asserts that the number of metric combinations matches the expected counts for each release cohort year."""
        def _count_combinations(output):
            actual_combination_counts = {}

            for key in expected_combination_counts.keys():
                actual_combination_counts[key] = 0

            for result in output:
                combination_dict, _ = result

                if combination_dict.get('metric_type') == MetricType.REINCARCERATION_RATE:
                    release_cohort_year = combination_dict['release_cohort']
                    actual_combination_counts[release_cohort_year] = actual_combination_counts[release_cohort_year] + 1
                elif combination_dict.get('metric_type') == MetricType.REINCARCERATION_COUNT:
                    actual_combination_counts['counts'] = actual_combination_counts['counts'] + 1

            for key in expected_combination_counts:
                if expected_combination_counts[key] != actual_combination_counts[key]:
                    raise BeamAssertException(f"Failed assert. Count {actual_combination_counts[key]} does not match"
                                              f" expected value {expected_combination_counts[key]}.")

        return _count_combinations

    @staticmethod
    def validate_job_id_on_metric(expected_job_id):

        def _validate_job_id_on_metric(output):

            for metric in output:

                if metric.job_id != expected_job_id:
                    raise BeamAssertException('Failed assert. Output job_id: '
                                              f"{metric.job_id} does not match"
                                              "expected value: "
                                              f"{expected_job_id}")

        return _validate_job_id_on_metric

    @staticmethod
    def validate_metric_writable_dict():

        def _validate_metric_writable_dict(output):
            for metric_dict in output:
                for _, value in metric_dict.items():
                    if isinstance(value, Enum):
                        raise BeamAssertException('Failed assert. Dictionary'
                                                  'contains invalid Enum '
                                                  f"value: {value}")
                    if isinstance(value, datetime.date):
                        raise BeamAssertException('Failed assert. Dictionary'
                                                  'contains invalid date '
                                                  f"value: {value}")

        return _validate_metric_writable_dict
