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
"""Shared utils for dealing with PeriodType entities (StateIncarcerationPeriod and StateSupervisionPeriod)."""
from functools import cmp_to_key
from typing import List, Callable

from recidiviz.persistence.entity.state.entities import PeriodType


def sort_periods_by_set_dates_and_statuses(
    periods: List[PeriodType], is_active_period_function: Callable[[PeriodType], int]
) -> None:
    """Sorts periods chronologically by the start and end dates according to this logic:
    - Sorts by start_date_inclusive, if set, else by end_date_exclusive
    - For periods with the same start_date_inclusive:
        - If neither have a end_date_exclusive, sorts by the status
        - Else, sorts by end_date_exclusive, with unset end_date_exclusives before set end_date_exclusives
    """

    def _sort_period_by_external_id(p_a: PeriodType, p_b: PeriodType) -> int:
        """Sorts two periods alphabetically by external_id."""
        if p_a.external_id is None or p_b.external_id is None:
            raise ValueError("Expect no placeholder periods in this function.")

        # Alphabetic sort by external_id
        return -1 if p_a.external_id < p_b.external_id else 1

    def _sort_by_nonnull_end_dates(period_a: PeriodType, period_b: PeriodType) -> int:
        if not period_a.end_date_exclusive or not period_b.end_date_exclusive:
            raise ValueError("Expected nonnull ending dates")
        if period_a.end_date_exclusive != period_b.end_date_exclusive:
            return (period_a.end_date_exclusive - period_b.end_date_exclusive).days
        # They have the same start and end dates. Sort by external_id.
        return _sort_period_by_external_id(period_a, period_b)

    def _sort_by_active_status(period_a: PeriodType, period_b: PeriodType) -> int:
        period_a_active = is_active_period_function(period_a)
        period_b_active = is_active_period_function(period_b)

        if period_a_active == period_b_active:
            return _sort_period_by_external_id(period_a, period_b)
        # Sort by status of the period. Order periods that are active (no end date) after periods that have ended.
        if period_a_active:
            return 1
        if period_b_active:
            return -1
        raise ValueError("One status should have UNDER_SUPERVISION at this point")

    def _sort_equal_start_date(period_a: PeriodType, period_b: PeriodType) -> int:
        if period_a.start_date_inclusive != period_b.start_date_inclusive:
            raise ValueError("Expected equal start dates")
        if period_a.end_date_exclusive and period_b.end_date_exclusive:
            return _sort_by_nonnull_end_dates(period_a, period_b)
        if (
            period_a.start_date_inclusive is None
            or period_b.start_date_inclusive is None
        ):
            raise ValueError(
                "Start dates expected to be equal and nonnull at this point otherwise we would have a "
                "period that has a null ending and null starting reason."
            )
        if period_a.end_date_exclusive is None and period_b.end_date_exclusive is None:
            return _sort_by_active_status(period_a, period_b)
        # Sort by end dates, with unset end dates coming first if the following period is greater than 0 days
        # long (we assume in this case that we forgot to close this open period).
        if period_a.end_date_exclusive:
            return (
                1
                if (period_a.end_date_exclusive - period_a.start_date_inclusive).days
                else -1
            )
        if period_b.end_date_exclusive:
            return (
                -1
                if (period_b.end_date_exclusive - period_b.start_date_inclusive).days
                else 1
            )
        raise ValueError(
            "At least one of the periods is expected to have a end_date_exclusive at this point."
        )

    def _sort_share_date_not_starting(
        period_a: PeriodType, period_b: PeriodType
    ) -> int:
        both_a_set = (
            period_a.start_date_inclusive is not None
            and period_a.end_date_exclusive is not None
        )
        both_b_set = (
            period_b.start_date_inclusive is not None
            and period_b.end_date_exclusive is not None
        )

        if not both_a_set and not both_b_set:
            # One has an start date and the other has an end date on the same day. Order the start before the end.
            return -1 if period_a.start_date_inclusive else 1

        # One period has both a start date and an end date, and the other has only an end date.
        if not period_a.start_date_inclusive:
            if period_a.end_date_exclusive == period_b.start_date_inclusive:
                # period_a is missing a start_date_inclusive, and its end_date_exclusive matches period_b's
                # start_date_inclusive. We want to order the end before the start that has a later ending.
                return -1
            # These share an end date, and period_a does not have a start date. Order the period with the set, earlier
            # start date first.
            return 1
        if not period_b.start_date_inclusive:
            if period_b.end_date_exclusive == period_a.start_date_inclusive:
                # period_b is missing a start date, and its end date matches period_a's start date. We want to order the
                # end date before the start date that has a later end date.
                return 1
            # These share an end date, and period_b does not have a start date. Order the period with the set, earlier
            # start date first.
            return -1
        raise ValueError(
            "It should not be possible to reach this point. If either, but not both, period_a or period_b"
            " only have one date set, and they don't have equal None start dates, then we expect either"
            "period_a or period_b to have a missing start_date_inclusive here."
        )

    def _sort_function(period_a: PeriodType, period_b: PeriodType) -> int:
        if period_a.start_date_inclusive == period_b.start_date_inclusive:
            return _sort_equal_start_date(period_a, period_b)

        # Sort by start_date_inclusive, if set, or end_date_exclusive if not set
        date_a = (
            period_a.start_date_inclusive
            if period_a.start_date_inclusive
            else period_a.end_date_exclusive
        )
        date_b = (
            period_b.start_date_inclusive
            if period_b.start_date_inclusive
            else period_b.end_date_exclusive
        )
        if not date_a:
            raise ValueError(f"Found period with no starting or ending date {period_a}")
        if not date_b:
            raise ValueError(f"Found period with no starting or ending date {period_b}")
        if date_a == date_b:
            return _sort_share_date_not_starting(period_a, period_b)

        return (date_a - date_b).days

    periods.sort(key=cmp_to_key(_sort_function))
