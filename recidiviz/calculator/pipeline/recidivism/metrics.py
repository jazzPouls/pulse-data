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

"""Recidivism metrics we calculate."""

from datetime import date
from typing import Any, Dict, Optional, cast

import attr

from recidiviz.calculator.pipeline.recidivism.release_event import (
    ReincarcerationReturnType,
)
from recidiviz.calculator.pipeline.utils.metric_utils import (
    RecidivizMetric,
    PersonLevelMetric,
    RecidivizMetricType,
)
from recidiviz.common.constants.state.state_supervision_period import (
    StateSupervisionPeriodSupervisionType,
)
from recidiviz.common.constants.state.state_supervision_violation import (
    StateSupervisionViolationType,
)


class ReincarcerationRecidivismMetricType(RecidivizMetricType):
    """The type of reincarceration recidivism metrics."""

    REINCARCERATION_COUNT = "REINCARCERATION_COUNT"
    REINCARCERATION_RATE = "REINCARCERATION_RATE"


# TODO(#1841): Implement rearrest recidivism metrics
# TODO(#1842): Implement reconviction recidivism metrics
@attr.s
class ReincarcerationRecidivismMetric(RecidivizMetric, PersonLevelMetric):
    """Models a single recidivism metric.

    Contains all of the identifying characteristics of the metric, including required characteristics for normalization
    as well as optional characteristics for slicing the data.
    """

    # Required characteristics

    # The type of ReincarcerationRecidivismMetric
    metric_type: ReincarcerationRecidivismMetricType = attr.ib(default=None)

    # Optional characteristics

    # The bucket string of the persons' incarceration stay length (in months), e.g., '<12' or '36-48'
    stay_length_bucket: Optional[str] = attr.ib(default=None)

    # The facility the persons were released from prior to recidivating
    release_facility: Optional[str] = attr.ib(default=None)

    # County of residence
    county_of_residence: Optional[str] = attr.ib(default=None)

    # ReincarcerationReturnType enum indicating whether the persons returned to incarceration because of a revocation
    # of supervision or because of a new admission
    return_type: ReincarcerationReturnType = attr.ib(default=None)

    # StateSupervisionPeriodSupervisionType enum for the type of supervision the persons were on before they
    # returned to incarceration.
    from_supervision_type: StateSupervisionPeriodSupervisionType = attr.ib(default=None)

    # StateSupervisionViolationType enum for the type of violation that eventually caused the revocation of supervision
    source_violation_type: StateSupervisionViolationType = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["ReincarcerationRecidivismMetric"]:
        """Builds a ReincarcerationRecidivismMetric object from the given arguments."""

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        recidivism_metric = cast(
            ReincarcerationRecidivismMetric,
            ReincarcerationRecidivismMetric.build_from_dictionary(metric_key),
        )

        return recidivism_metric


@attr.s
class ReincarcerationRecidivismCountMetric(ReincarcerationRecidivismMetric):
    """Subclass of ReincarcerationRecidivismMetric that contains count data.

    A recidivism count metric contains the number of reincarceration returns in a given window, with a start and end
    date.
    """

    # Required characteristics

    metric_type: ReincarcerationRecidivismMetricType = attr.ib(
        init=False, default=ReincarcerationRecidivismMetricType.REINCARCERATION_COUNT
    )

    # Year
    year: int = attr.ib(default=None)

    # Month
    month: int = attr.ib(default=None)

    # For person-level metrics only, the days at liberty between release and reincarceration
    days_at_liberty: int = attr.ib(default=None)

    # Date of reincarceration
    reincarceration_date: date = attr.ib(default=None)

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["ReincarcerationRecidivismCountMetric"]:

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        recidivism_metric = cast(
            ReincarcerationRecidivismCountMetric,
            ReincarcerationRecidivismCountMetric.build_from_dictionary(metric_key),
        )

        return recidivism_metric


@attr.s
class ReincarcerationRecidivismRateMetric(ReincarcerationRecidivismMetric):
    """Subclass of ReincarcerationRecidivismMetric that contains rate data.

    A recidivism rate metric contains a recidivism rate, including the numerator of total instances of recidivism and a
    denominator of total instances of release from incarceration.
    """

    # Required characteristics

    # The type of ReincarcerationRecidivismMetric
    metric_type: ReincarcerationRecidivismMetricType = attr.ib(
        init=False, default=ReincarcerationRecidivismMetricType.REINCARCERATION_RATE
    )

    # The integer year during which the persons were released
    release_cohort: int = attr.ib(default=None)  # non-nullable

    # The integer number of years after date of release during which recidivism was measured
    follow_up_period: int = attr.ib(default=None)  # non-nullable

    # Required metric values

    # Whether or not the person recidivated
    did_recidivate: bool = attr.ib(default=None)  # non-nullable

    # Date of release
    release_date: date = attr.ib(default=None)  # non-nullable

    @staticmethod
    def build_from_metric_key_group(
        metric_key: Dict[str, Any], job_id: str
    ) -> Optional["ReincarcerationRecidivismRateMetric"]:
        """Constructs a RecidivismMetric object from a dictionary containing all required values and the corresponding
        group of ReleaseEvents, with 1s representing RecidivismReleaseEvents, and 0s representing
        NonRecidivismReleaseEvents.
        """

        if not metric_key:
            raise ValueError("The metric_key is empty.")

        metric_key["job_id"] = job_id
        metric_key["created_on"] = date.today()

        recidivism_metric = cast(
            ReincarcerationRecidivismRateMetric,
            ReincarcerationRecidivismRateMetric.build_from_dictionary(metric_key),
        )

        return recidivism_metric
