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

"""Constants related to a StateIncarcerationPeriod."""

import recidiviz.common.constants.enum_canonical_strings as enum_strings
import recidiviz.common.constants.state.enum_canonical_strings as \
    state_enum_strings
from recidiviz.common.constants.entity_enum import EntityEnum, EntityEnumMeta


class StateIncarcerationPeriodStatus(EntityEnum, metaclass=EntityEnumMeta):
    EXTERNAL_UNKNOWN = enum_strings.external_unknown
    IN_CUSTODY = state_enum_strings.state_incarceration_period_status_in_custody
    NOT_IN_CUSTODY = \
        state_enum_strings.state_incarceration_period_status_not_in_custody
    PRESENT_WITHOUT_INFO = enum_strings.present_without_info

    @staticmethod
    def _get_default_map():
        return _STATE_INCARCERATION_PERIOD_STATUS_MAP


class StateIncarcerationFacilitySecurityLevel(EntityEnum,
                                              metaclass=EntityEnumMeta):
    MAXIMUM = \
        state_enum_strings.state_incarceration_facility_security_level_maximum
    MEDIUM = \
        state_enum_strings.state_incarceration_facility_security_level_medium
    MINIMUM = \
        state_enum_strings.state_incarceration_facility_security_level_minimum

    @staticmethod
    def _get_default_map():
        return _STATE_INCARCERATION_FACILITY_SECURITY_LEVEL_MAP


class StateIncarcerationPeriodAdmissionReason(EntityEnum,
                                              metaclass=EntityEnumMeta):
    """Reasons for admission to a period of incarceration."""
    ADMITTED_IN_ERROR = \
        state_enum_strings.\
        state_incarceration_period_admission_reason_admitted_in_error
    EXTERNAL_UNKNOWN = enum_strings.external_unknown
    NEW_ADMISSION = \
        state_enum_strings.\
        state_incarceration_period_admission_reason_new_admission
    PAROLE_REVOCATION = state_enum_strings.\
        state_incarceration_period_admission_reason_parole_revocation
    PROBATION_REVOCATION = state_enum_strings.\
        state_incarceration_period_admission_reason_probation_revocation
    # pylint:disable=line-too-long
    RETURN_FROM_ERRONEOUS_RELEASE = \
        state_enum_strings.\
        state_incarceration_period_admission_reason_return_from_erroneous_release
    RETURN_FROM_ESCAPE = \
        state_enum_strings.\
        state_incarceration_period_admission_reason_return_from_escape
    TRANSFER = \
        state_enum_strings.state_incarceration_period_admission_reason_transfer

    @staticmethod
    def _get_default_map():
        return _STATE_INCARCERATION_PERIOD_ADMISSION_REASON_MAP


class StateIncarcerationPeriodReleaseReason(EntityEnum,
                                            metaclass=EntityEnumMeta):
    """Reasons for release from a period of incarceration."""
    COMMUTED = \
        state_enum_strings.\
        state_incarceration_period_release_reason_commuted
    # This release type corresponds to any release into some sort of
    # supervision.
    CONDITIONAL_RELEASE = \
        state_enum_strings.\
        state_incarceration_period_release_reason_conditional_release
    COURT_ORDER = \
        state_enum_strings.\
        state_incarceration_period_release_reason_court_order
    DEATH = state_enum_strings.state_incarceration_period_release_reason_death
    ESCAPE = state_enum_strings.state_incarceration_period_release_reason_escape
    EXTERNAL_UNKNOWN = enum_strings.external_unknown
    RELEASED_IN_ERROR = \
        state_enum_strings.\
        state_incarceration_period_release_reason_released_in_error
    SENTENCE_SERVED = \
        state_enum_strings.\
        state_incarceration_period_release_reason_sentence_served
    TRANSFER = \
        state_enum_strings.state_incarceration_period_release_reason_transfer

    @staticmethod
    def _get_default_map():
        return _STATE_INCARCERATION_PERIOD_RELEASE_REASON_MAP


_STATE_INCARCERATION_FACILITY_SECURITY_LEVEL_MAP = {
    'MAXIMUM': StateIncarcerationFacilitySecurityLevel.MAXIMUM,
    'MAX': StateIncarcerationFacilitySecurityLevel.MAXIMUM,
    'MEDIUM': StateIncarcerationFacilitySecurityLevel.MEDIUM,
    'MED': StateIncarcerationFacilitySecurityLevel.MEDIUM,
    'MINIMUM': StateIncarcerationFacilitySecurityLevel.MINIMUM,
    'MIN': StateIncarcerationFacilitySecurityLevel.MINIMUM,
}


_STATE_INCARCERATION_PERIOD_STATUS_MAP = {
    'ADM': StateIncarcerationPeriodStatus.IN_CUSTODY,
    'CUSTODY': StateIncarcerationPeriodStatus.IN_CUSTODY,
    'IN CUSTODY': StateIncarcerationPeriodStatus.IN_CUSTODY,
    'NOT IN CUSTODY': StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
    'REL': StateIncarcerationPeriodStatus.NOT_IN_CUSTODY,
}

_STATE_INCARCERATION_PERIOD_ADMISSION_REASON_MAP = {
    'ADM ERROR': StateIncarcerationPeriodAdmissionReason.ADMITTED_IN_ERROR,
    'ERROR': StateIncarcerationPeriodAdmissionReason.ADMITTED_IN_ERROR,
    'ADMN': StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
    'NEW ADMISSION': StateIncarcerationPeriodAdmissionReason.NEW_ADMISSION,
    'PAROLE REVOCATION':
        StateIncarcerationPeriodAdmissionReason.PAROLE_REVOCATION,
    'PV': StateIncarcerationPeriodAdmissionReason.PAROLE_REVOCATION,
    'PRB': StateIncarcerationPeriodAdmissionReason.PROBATION_REVOCATION,
    'PROBATION REVOCATION':
        StateIncarcerationPeriodAdmissionReason.PROBATION_REVOCATION,
    'REC': StateIncarcerationPeriodAdmissionReason.RETURN_FROM_ESCAPE,
    'RECA': StateIncarcerationPeriodAdmissionReason.RETURN_FROM_ESCAPE,
    'RETURN FROM ESCAPE':
        StateIncarcerationPeriodAdmissionReason.RETURN_FROM_ESCAPE,
    'COURT': StateIncarcerationPeriodAdmissionReason.TRANSFER,
    'CRT': StateIncarcerationPeriodAdmissionReason.TRANSFER,
    'DETOX': StateIncarcerationPeriodAdmissionReason.TRANSFER,
    'HOSPITAL': StateIncarcerationPeriodAdmissionReason.TRANSFER,
    'MED': StateIncarcerationPeriodAdmissionReason.TRANSFER,
    'MEDICAL': StateIncarcerationPeriodAdmissionReason.TRANSFER,
    'RETURN FROM MEDICAL': StateIncarcerationPeriodAdmissionReason.TRANSFER,
    'TRANSFER': StateIncarcerationPeriodAdmissionReason.TRANSFER
}

_STATE_INCARCERATION_PERIOD_RELEASE_REASON_MAP = {
    'CMM': StateIncarcerationPeriodReleaseReason.COMMUTED,
    'COMMUTED': StateIncarcerationPeriodReleaseReason.COMMUTED,
    'COMMUTATION': StateIncarcerationPeriodReleaseReason.COMMUTED,
    'CONDITIONAL': StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'CONDITIONAL RELEASE':
        StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'COURT ORDER': StateIncarcerationPeriodReleaseReason.COURT_ORDER,
    'DEATH': StateIncarcerationPeriodReleaseReason.DEATH,
    'DECE': StateIncarcerationPeriodReleaseReason.DEATH,
    'DECEASED': StateIncarcerationPeriodReleaseReason.DEATH,
    'EARNED TIME': StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
    'ESC': StateIncarcerationPeriodReleaseReason.ESCAPE,
    'ESCP': StateIncarcerationPeriodReleaseReason.ESCAPE,
    'ESCAPED': StateIncarcerationPeriodReleaseReason.ESCAPE,
    'ESCAPE': StateIncarcerationPeriodReleaseReason.ESCAPE,
    'EXPIRED': StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
    'GOOD TIME': StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,

    # TODO(1697): Is this actually what these mean?
    'HELD ELSEWHERE': StateIncarcerationPeriodReleaseReason.TRANSFER,
    'HOLD': StateIncarcerationPeriodReleaseReason.TRANSFER,

    'PAROLE': StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'PARL': StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'RPAR': StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'RPRB': StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'SUPL': StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,

    # TODO(1697): Should this actually be SENTENCE_SERVED? The probation is now
    #  a new stacked sentence that is being served?
    'PROBATION': StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'RELEASE TO PAROLE':
        StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,

    # TODO(1697): Should this actually be SENTENCE_SERVED? The probation is now
    #  a new stacked sentence that is being served?
    'RELEASE TO PROBATION':
        StateIncarcerationPeriodReleaseReason.CONDITIONAL_RELEASE,
    'ERR': StateIncarcerationPeriodReleaseReason.RELEASED_IN_ERROR,
    'ERROR': StateIncarcerationPeriodReleaseReason.RELEASED_IN_ERROR,
    'RELEASED': StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
    'SERVED': StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
    'TIME EARNED': StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
    'TIME SERVED': StateIncarcerationPeriodReleaseReason.SENTENCE_SERVED,
    'COURT': StateIncarcerationPeriodReleaseReason.TRANSFER,
    'CRT': StateIncarcerationPeriodReleaseReason.TRANSFER,
    'DETOX': StateIncarcerationPeriodReleaseReason.TRANSFER,
    'HOSPITAL': StateIncarcerationPeriodReleaseReason.TRANSFER,
    'MED': StateIncarcerationPeriodReleaseReason.TRANSFER,
    'MEDICAL': StateIncarcerationPeriodReleaseReason.TRANSFER,
    'TRN': StateIncarcerationPeriodReleaseReason.TRANSFER,
}