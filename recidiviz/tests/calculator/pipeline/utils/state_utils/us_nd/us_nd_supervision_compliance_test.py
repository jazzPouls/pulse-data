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
"""Unit tests for us_nd_supervision_compliance."""
# pylint: disable=protected-access

import unittest
from datetime import date

from recidiviz.calculator.pipeline.utils.state_utils.us_nd.us_nd_supervision_compliance import \
    UsNdSupervisionCaseCompliance
from recidiviz.common.constants.state.state_assessment import StateAssessmentType
from recidiviz.common.constants.state.state_case_type import StateSupervisionCaseType
from recidiviz.common.constants.state.state_supervision_contact import StateSupervisionContactType, \
    StateSupervisionContactStatus
from recidiviz.common.constants.state.state_supervision_period import StateSupervisionPeriodTerminationReason, \
    StateSupervisionPeriodSupervisionType, StateSupervisionPeriodAdmissionReason, StateSupervisionLevel
from recidiviz.common.constants.states import StateCode
from recidiviz.persistence.entity.state.entities import StateAssessment, StateSupervisionPeriod, StateSupervisionContact


class TestAssessmentsInComplianceMonth(unittest.TestCase):
    """Tests for assessments_in_compliance_month."""
    def test_assessments_in_compliance_month(self):
        evaluation_date = date(2018, 4, 30)
        assessment_out_of_range = StateAssessment.new_with_defaults(
            state_code=StateCode.US_ND.value,
            assessment_type=StateAssessmentType.LSIR,
            assessment_date=date(2018, 3, 10)
        )
        assessment_out_of_range_2 = StateAssessment.new_with_defaults(
            state_code=StateCode.US_ND.value,
            assessment_type=StateAssessmentType.LSIR,
            assessment_date=date(2018, 5, 10)
        )
        assessment_1 = StateAssessment.new_with_defaults(
            state_code=StateCode.US_ND.value,
            assessment_type=StateAssessmentType.LSIR,
            assessment_date=date(2018, 4, 2)
        )
        assessment_2 = StateAssessment.new_with_defaults(
            state_code=StateCode.US_ND.value,
            assessment_type=StateAssessmentType.LSIR,
            assessment_date=date(2018, 4, 10)
        )
        assessment_3 = StateAssessment.new_with_defaults(
            state_code=StateCode.US_ND.value,
            assessment_type=StateAssessmentType.LSIR,
            assessment_date=date(2018, 4, 28)
        )

        supervision_period = StateSupervisionPeriod.new_with_defaults(
            supervision_period_id=111,
            external_id='sp1',
            state_code=StateCode.US_ND.value,
            start_date=date(2018, 3, 5),  # This was a Monday
            termination_date=date(2018, 5, 19),
            admission_reason=StateSupervisionPeriodAdmissionReason.COURT_SENTENCE,
            termination_reason=StateSupervisionPeriodTerminationReason.DISCHARGE,
            supervision_period_supervision_type=StateSupervisionPeriodSupervisionType.PROBATION,
        )

        assessments = [assessment_out_of_range, assessment_out_of_range_2, assessment_1, assessment_2, assessment_3]
        expected_assessments = [assessment_1, assessment_2, assessment_3]

        us_nd_supervision_compliance = UsNdSupervisionCaseCompliance(supervision_period=supervision_period,
                                                                     case_type=StateSupervisionCaseType.GENERAL,
                                                                     start_of_supervision=evaluation_date,
                                                                     assessments=assessments,
                                                                     supervision_contacts=[])

        self.assertEqual(len(expected_assessments), us_nd_supervision_compliance
                         ._assessments_in_compliance_month(evaluation_date))


class TestFaceToFaceContactsInComplianceMonth(unittest.TestCase):
    """Tests for face_to_face_contacts_in_compliance_month."""
    def test_face_to_face_contacts_in_compliance_month(self):
        # TODO(#5199): Update once face to face logic has been implemented.
        evaluation_date = date(2018, 4, 30)

        supervision_period = StateSupervisionPeriod.new_with_defaults(
            supervision_period_id=111,
            external_id='sp1',
            state_code=StateCode.US_ND.value,
            start_date=date(2018, 3, 5),  # This was a Monday
            termination_date=date(2018, 5, 19),
            admission_reason=StateSupervisionPeriodAdmissionReason.COURT_SENTENCE,
            termination_reason=StateSupervisionPeriodTerminationReason.DISCHARGE,
            supervision_period_supervision_type=StateSupervisionPeriodSupervisionType.PROBATION,
        )

        contacts = []
        us_nd_supervision_compliance = UsNdSupervisionCaseCompliance(supervision_period=supervision_period,
                                                                     case_type=StateSupervisionCaseType.GENERAL,
                                                                     start_of_supervision=evaluation_date,
                                                                     assessments=[],
                                                                     supervision_contacts=contacts)
        self.assertEqual(0, us_nd_supervision_compliance._face_to_face_contacts_in_compliance_month(evaluation_date))


class TestGuidelinesApplicableForCase(unittest.TestCase):
    """Tests the guidelines_applicable_for_case function."""

    def test_guidelines_applicable_for_case(self):
        """The guidelines should be case and supervision level agnostic."""
        supervision_period = StateSupervisionPeriod.new_with_defaults(
            supervision_period_id=111,
            external_id='sp1',
            state_code=StateCode.US_ND.value,
            start_date=date(2018, 3, 5),
            termination_date=date(2018, 5, 19),
            admission_reason=StateSupervisionPeriodAdmissionReason.COURT_SENTENCE,
            termination_reason=StateSupervisionPeriodTerminationReason.DISCHARGE,
            supervision_period_supervision_type=StateSupervisionPeriodSupervisionType.PROBATION,
            supervision_level=StateSupervisionLevel.MEDIUM,
            supervision_level_raw_text='LEVEL 2'
        )

        us_nd_supervision_compliance = UsNdSupervisionCaseCompliance(supervision_period=supervision_period,
                                                                     case_type=StateSupervisionCaseType.GENERAL,
                                                                     start_of_supervision=supervision_period.start_date,
                                                                     assessments=[],
                                                                     supervision_contacts=[])

        applicable = us_nd_supervision_compliance._guidelines_applicable_for_case()

        self.assertTrue(applicable)


class TestContactFrequencySufficient(unittest.TestCase):
    """Tests the contact_frequency_is_sufficient function."""
    def test_face_to_face_frequency_sufficient(self):
        # TODO(#5199): Update once face to face logic is implemented.
        supervision_period = StateSupervisionPeriod.new_with_defaults(
            supervision_period_id=111,
            external_id='sp1',
            state_code=StateCode.US_ND.value,
            start_date=date(2018, 3, 5),  # This was a Monday
            termination_date=date(2018, 5, 19),
            admission_reason=StateSupervisionPeriodAdmissionReason.COURT_SENTENCE,
            termination_reason=StateSupervisionPeriodTerminationReason.DISCHARGE,
            supervision_period_supervision_type=StateSupervisionPeriodSupervisionType.PROBATION,
        )

        supervision_contacts = [StateSupervisionContact.new_with_defaults(
            state_code=StateCode.US_ND.value,
            contact_date=supervision_period.start_date,
            contact_type=StateSupervisionContactType.FACE_TO_FACE,
            status=StateSupervisionContactStatus.COMPLETED
        )]

        start_of_supervision = supervision_period.start_date
        evaluation_date = start_of_supervision

        us_nd_supervision_compliance = UsNdSupervisionCaseCompliance(supervision_period=supervision_period,
                                                                     case_type=StateSupervisionCaseType.GENERAL,
                                                                     start_of_supervision=evaluation_date,
                                                                     assessments=[],
                                                                     supervision_contacts=supervision_contacts)

        face_to_face_frequency_sufficient = us_nd_supervision_compliance.\
            _face_to_face_contact_frequency_is_sufficient(evaluation_date)

        self.assertFalse(face_to_face_frequency_sufficient)


class TestReassessmentRequirementAreMet(unittest.TestCase):
    """Tests the reassessment_requirements_are_met function."""
    def test_reassessment_requirements_are_met(self):
        supervision_period = StateSupervisionPeriod.new_with_defaults(
            supervision_period_id=111,
            external_id='sp1',
            state_code=StateCode.US_ND.value,
            start_date=date(2018, 3, 5),  # This was a Monday
            termination_date=date(2018, 5, 19),
            admission_reason=StateSupervisionPeriodAdmissionReason.COURT_SENTENCE,
            termination_reason=StateSupervisionPeriodTerminationReason.DISCHARGE,
            supervision_period_supervision_type=StateSupervisionPeriodSupervisionType.PROBATION,
        )

        assessment = StateAssessment.new_with_defaults(
            state_code=StateCode.US_ND.value,
            assessment_type=StateAssessmentType.LSIR,
            assessment_date=date(2018, 4, 2)
        )

        start_of_supervision = supervision_period.start_date
        evaluation_date = start_of_supervision

        us_nd_supervision_compliance = UsNdSupervisionCaseCompliance(supervision_period=supervision_period,
                                                                     case_type=StateSupervisionCaseType.GENERAL,
                                                                     start_of_supervision=evaluation_date,
                                                                     assessments=[assessment],
                                                                     supervision_contacts=[])

        reassessment_requirements_are_met = us_nd_supervision_compliance.\
            _reassessment_requirements_are_met(evaluation_date, assessment)

        self.assertTrue(reassessment_requirements_are_met)

    def test_reassessment_requirements_are_not_met(self):
        supervision_period = StateSupervisionPeriod.new_with_defaults(
            supervision_period_id=111,
            external_id='sp1',
            state_code=StateCode.US_ND.value,
            start_date=date(2018, 3, 5),  # This was a Monday
            termination_date=date(2018, 5, 19),
            admission_reason=StateSupervisionPeriodAdmissionReason.COURT_SENTENCE,
            termination_reason=StateSupervisionPeriodTerminationReason.DISCHARGE,
            supervision_period_supervision_type=StateSupervisionPeriodSupervisionType.PROBATION,
        )

        assessment = StateAssessment.new_with_defaults(
            state_code=StateCode.US_ND.value,
            assessment_type=StateAssessmentType.LSIR,
            assessment_date=date(2010, 4, 2)
        )

        start_of_supervision = supervision_period.start_date
        evaluation_date = start_of_supervision

        us_nd_supervision_compliance = UsNdSupervisionCaseCompliance(supervision_period=supervision_period,
                                                                     case_type=StateSupervisionCaseType.GENERAL,
                                                                     start_of_supervision=evaluation_date,
                                                                     assessments=[assessment],
                                                                     supervision_contacts=[])

        reassessment_requirements_are_met = us_nd_supervision_compliance.\
            _reassessment_requirements_are_met(evaluation_date, assessment)

        self.assertFalse(reassessment_requirements_are_met)
