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
"""Supervision metrics we calculate."""

from datetime import date
from typing import Any, Dict, Optional, cast, List

import attr

from recidiviz.calculator.pipeline.utils.metric_utils import (
    RecidivizMetric,
    PersonLevelMetric,
    RecidivizMetricType,
    AssessmentMetric,
    SupervisionLocationMetric,
)
from recidiviz.common.attr_mixins import BuildableAttr
from recidiviz.common.constants.state.state_case_type import StateSupervisionCaseType
from recidiviz.common.constants.state.state_supervision_period import (
    StateSupervisionPeriodTerminationReason,
    StateSupervisionPeriodSupervisionType,
    StateSupervisionLevel,
    StateSupervisionPeriodAdmissionReason,
)
from recidiviz.common.constants.state.state_supervision_violation import (
    StateSupervisionViolationType,
)
from recidiviz.common.constants.state.state_supervision_violation_response import (
    StateSupervisionViolationResponseRevocationType,
    StateSupervisionViolationResponseDecision,
)


class SupervisionMetricType(RecidivizMetricType):
    """The type of supervision metrics."""

    SUPERVISION_COMPLIANCE = "SUPERVISION_COMPLIANCE"
    SUPERVISION_POPULATION = "SUPERVISION_POPULATION"
    SUPERVISION_OUT_OF_STATE_POPULATION = "SUPERVISION_OUT_OF_STATE_POPULATION"
    SUPERVISION_REVOCATION = "SUPERVISION_REVOCATION"
    SUPERVISION_REVOCATION_ANALYSIS = "SUPERVISION_REVOCATION_ANALYSIS"
    SUPERVISION_START = "SUPERVISION_START"
    SUPERVISION_SUCCESS = "SUPERVISION_SUCCESS"
    SUPERVISION_SUCCESSFUL_SENTENCE_DAYS_SERVED = (
        "SUPERVISION_SUCCESSFUL_SENTENCE_DAYS_SERVED"
    )
    SUPERVISION_TERMINATION = "SUPERVISION_TERMINATION"
    SUPERVISION_DOWNGRADE = "SUPERVISION_DOWNGRADE"


@attr.s
class SupervisionMetric(RecidivizMetric, SupervisionLocationMetric):
    """Models a single supervision metric.

    Contains all of the identifying characteristics of the metric, including required characteristics for
    normalization as well as optional characteristics for slicing the data.
    """

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(default=None)

    # Year
    year: int = attr.ib(default=None)

    # Month
    month: int = attr.ib(default=None)

    # Optional characteristics

    # TODO(#2891): Consider moving this out of the base class, and making the supervision type specific to each
    #   metric type
    # Supervision Type
    supervision_type: Optional[StateSupervisionPeriodSupervisionType] = attr.ib(
        default=None
    )

    # The type of supervision case
    case_type: Optional[StateSupervisionCaseType] = attr.ib(default=None)

    # Level of supervision
    supervision_level: Optional[StateSupervisionLevel] = attr.ib(default=None)

    # Raw text of the level of supervision
    supervision_level_raw_text: Optional[str] = attr.ib(default=None)

    # TODO(#3885): Add a custodial_authority field to this metric, then update BQ views to pass through to dashboard
    # for new custodial authority dropdown feature.

    # External ID of the officer who was supervising the person described by this metric.
    supervising_officer_external_id: Optional[str] = attr.ib(default=None)

    # Area of jurisdictional coverage of the court that sentenced the person to this supervision
    judicial_district_code: Optional[str] = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionMetric"]:
        """Builds a SupervisionMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionMetric, SupervisionMetric.build_from_dictionary(metric_key)
        )

        return supervision_metric


@attr.s
class ViolationHistoryMetric(BuildableAttr):
    """Base class for including the most severe violation type and subtype features on a metric."""

    # The most severe violation type leading up to the date of the event the metric describes
    most_severe_violation_type: Optional[StateSupervisionViolationType] = attr.ib(
        default=None
    )

    # A string subtype that provides further insight into the most_severe_violation_type above.
    most_severe_violation_type_subtype: Optional[str] = attr.ib(default=None)

    # The number of responses that were included in determining the most severe type/subtype
    response_count: Optional[int] = attr.ib(default=None)

    # The most severe decision on the responses that were included in determining the most severe type/subtype
    most_severe_response_decision: Optional[
        StateSupervisionViolationResponseDecision
    ] = attr.ib(default=None)


@attr.s
class SupervisionPopulationMetric(
    SupervisionMetric, PersonLevelMetric, ViolationHistoryMetric, AssessmentMetric
):
    """Subclass of SupervisionMetric that contains supervision population information."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_POPULATION
    )

    # Date of the supervision population count
    date_of_supervision: date = attr.ib(default=None)

    # Optional characteristics

    # TODO(#3600): This field should be removed because the daily output makes this unnecessary
    # For person-level metrics only, indicates whether this person was on supervision at the end of the month
    is_on_supervision_last_day_of_month: Optional[bool] = attr.ib(default=None)

    # The projected end date for the person's supervision term.
    projected_end_date: Optional[date] = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionPopulationMetric"]:
        """Builds a SupervisionPopulationMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionPopulationMetric,
            SupervisionPopulationMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SupervisionOutOfStatePopulationMetric(SupervisionPopulationMetric):
    """Subclass of SupervisionPopulationMetric that contains supervision information for people who are serving their
    supervisions in another state."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_OUT_OF_STATE_POPULATION
    )

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionOutOfStatePopulationMetric"]:
        """Builds a SupervisionOutOfStatePopulationMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionOutOfStatePopulationMetric,
            SupervisionOutOfStatePopulationMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SupervisionRevocationMetric(
    SupervisionMetric, PersonLevelMetric, AssessmentMetric
):
    """Subclass of SupervisionMetric that contains supervision revocation information."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_REVOCATION
    )

    # Optional characteristics

    # The StateSupervisionViolationResponseRevocationType enum for the type of revocation of supervision that this
    # metric describes
    revocation_type: Optional[
        StateSupervisionViolationResponseRevocationType
    ] = attr.ib(default=None)

    # A string subtype that provides further insight into the revocation_type above.
    revocation_type_subtype: Optional[str] = attr.ib(default=None)

    # StateSupervisionViolationType enum for the type of violation that eventually caused the revocation of supervision
    source_violation_type: Optional[StateSupervisionViolationType] = attr.ib(
        default=None
    )

    # For person-level metrics only, the date of the revocation admission
    revocation_admission_date: date = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionRevocationMetric"]:
        """Builds a SupervisionRevocationMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionRevocationMetric,
            SupervisionRevocationMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SupervisionRevocationAnalysisMetric(
    SupervisionRevocationMetric, PersonLevelMetric, ViolationHistoryMetric
):
    """Subclass of SupervisionRevocationMetric that contains information for supervision revocation analysis."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_REVOCATION_ANALYSIS
    )

    # Optional characteristics

    # A string representation of the violations recorded in the period leading up to the revocation, which is the
    # number of each of the represented types separated by a semicolon
    violation_history_description: Optional[str] = attr.ib(default=None)

    # A list of a list of strings for each violation type and subtype recorded during the period leading up to the
    # revocation. The elements of the outer list represent every StateSupervisionViolation that was reported in the
    # period leading up to the revocation. Each inner list represents all of the violation types and conditions that
    # were listed on the given violation. For example, 3 violations may be represented as:
    # [['FELONY', 'TECHNICAL'], ['MISDEMEANOR'], ['ABSCONDED', 'MUNICIPAL']]
    violation_type_frequency_counter: Optional[List[List[str]]] = attr.ib(default=None)

    # The most severe decision on the most recent response leading up to the revocation
    most_recent_response_decision: Optional[
        StateSupervisionViolationResponseDecision
    ] = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionRevocationAnalysisMetric"]:
        """Builds a SupervisionRevocationAnalysisMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionRevocationAnalysisMetric,
            SupervisionRevocationAnalysisMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SupervisionSuccessMetric(SupervisionMetric, PersonLevelMetric):
    """Subclass of SupervisionMetric that contains supervision success and failure counts."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_SUCCESS
    )

    # Whether this represents a successful completion
    successful_completion: bool = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionSuccessMetric"]:
        """Builds a SupervisionSuccessMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionSuccessMetric,
            SupervisionSuccessMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SuccessfulSupervisionSentenceDaysServedMetric(
    SupervisionMetric, PersonLevelMetric
):
    """Subclass of SupervisionMetric that contains the average number of days served for successful supervision
    sentences with projected completion dates in the month of the metric, where the person did not spend any time
    incarcerated in the duration of the sentence."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False,
        default=SupervisionMetricType.SUPERVISION_SUCCESSFUL_SENTENCE_DAYS_SERVED,
    )

    # Days served for this sentence
    days_served: int = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SuccessfulSupervisionSentenceDaysServedMetric"]:
        """Builds a SuccessfulSupervisionSentenceDaysServedMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SuccessfulSupervisionSentenceDaysServedMetric,
            SuccessfulSupervisionSentenceDaysServedMetric.build_from_dictionary(
                metric_key
            ),
        )

        return supervision_metric


@attr.s
class SupervisionTerminationMetric(
    SupervisionMetric, PersonLevelMetric, ViolationHistoryMetric, AssessmentMetric
):
    """Subclass of SupervisionMetric that contains information about a supervision that has been terminated, the reason
    for the termination, and the change in assessment score between the last assessment and the first reassessment."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_TERMINATION
    )

    # Optional characteristics

    # Change in scores between the assessment right before termination and first reliable assessment while on
    # supervision. The first "reliable" assessment is determined by state-specific logic.
    assessment_score_change: float = attr.ib(default=None)

    # The reason the supervision was terminated
    termination_reason: Optional[StateSupervisionPeriodTerminationReason] = attr.ib(
        default=None
    )

    # The date the supervision was terminated
    termination_date: Optional[date] = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionTerminationMetric"]:
        """Builds a SupervisionTerminationMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionTerminationMetric,
            SupervisionTerminationMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SupervisionStartMetric(SupervisionMetric, PersonLevelMetric):
    """Subclass of SupervisionMetric that contains information about the start of supervision."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_START
    )

    # Optional characteristics

    # The reason the supervision was started
    is_official_supervision_admission: bool = attr.ib(default=False)
    admission_reason: Optional[StateSupervisionPeriodAdmissionReason] = attr.ib(
        default=None
    )

    # The date the supervision was started
    start_date: Optional[date] = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionStartMetric"]:
        """Builds a SupervisionStartMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionStartMetric,
            SupervisionStartMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SupervisionCaseComplianceMetric(SupervisionPopulationMetric):
    """Subclass of SupervisionPopulationMetric for people who are on supervision on a given day that records
    information regarding whether a supervision case is meeting compliance standards, as well as counts of
    compliance-related tasks that occurred in the month of the evaluation."""

    # Required characteristics

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_COMPLIANCE
    )

    # The date the on which the case's compliance was evaluated
    date_of_evaluation: date = attr.ib(default=None)

    # The number of risk assessments conducted on this person in the month of the date_of_evaluation, preceding the
    # date_of_evaluation
    assessment_count: int = attr.ib(default=None)

    # The number of face-to-face contacts with this person in the month of the date_of_evaluation, preceding the
    # date_of_evaluation
    face_to_face_count: int = attr.ib(default=None)

    # Optional characteristics

    # The date that the last assessment happened. If no assessment has yet happened, this is None.
    most_recent_assessment_date: Optional[date] = attr.ib(default=None)

    # The number of days that an assessment is overdue according to compliance standards. If it is not overdue,
    # its value is zero. We set it to None if we do not know the compliance standards for this person.
    num_days_assessment_overdue: Optional[int] = attr.ib(default=None)

    # The date that the last face-to-face contact happened. If no meetings have yet happened, this is None.
    most_recent_face_to_face_date: Optional[date] = attr.ib(default=None)

    # Whether or not the supervision officer has had face-to-face contact with the person on supervision recently
    # enough to satisfy compliance measures. Should be unset if we do not know the compliance standards for this person.
    face_to_face_frequency_sufficient: Optional[bool] = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionCaseComplianceMetric"]:
        """Builds a SupervisionCaseComplianceMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionCaseComplianceMetric,
            SupervisionCaseComplianceMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric


@attr.s
class SupervisionDowngradeMetric(SupervisionMetric, PersonLevelMetric):
    """
    Subclass of SupervisionMetric for people whose supervision level has been downgraded.

    Note: This metric only identifies supervision level downgrades for states where a new supervision period is created
    if the supervision level changes.
    """

    # The type of SupervisionMetric
    metric_type: SupervisionMetricType = attr.ib(
        init=False, default=SupervisionMetricType.SUPERVISION_DOWNGRADE
    )

    # The date on which the downgrade in supervision level took place
    date_of_downgrade: date = attr.ib(default=None)

    # The previous supervision level, prior to the downgrade
    previous_supervision_level: StateSupervisionLevel = attr.ib(default=None)

    # The new supervision level, after the downgrade
    supervision_level: StateSupervisionLevel = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["SupervisionDowngradeMetric"]:
        """Builds a SupervisionDowngradeMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        supervision_metric = cast(
            SupervisionDowngradeMetric,
            SupervisionDowngradeMetric.build_from_dictionary(metric_key),
        )

        return supervision_metric
