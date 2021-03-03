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

"""Constants that correspond to the largely opaque column names from the
MODOC data warehouse."""

# Table prefixes
import re

TAK076_PREFIX = "CZ"
TAK291_PREFIX = "JS"

# Field names
DOC_ID = "DOC"
CYCLE_ID = "CYC"
SENTENCE_KEY_SEQ = "SEO"
FIELD_KEY_SEQ = "FSO"
VIOLATION_KEY_SEQ = "VSN"
CITATION_KEY_SEQ = "CSQ"

# Columns (Table prefixes + field names)
STATE_ID = "EK_SID"
FBI_ID = "EK_FBI"
LICENSE_ID = "EK_OLN"

CHARGE_COUNTY_CODE = "BS_CNT"

SENTENCE_COUNTY_CODE = "BS_CNS"
SENTENCE_OFFENSE_DATE = "BS_DO"
SENTENCE_COMPLETED_FLAG = "BS_SCF"
SUPERVISION_SENTENCE_TYPE = "SENTENCE_TYPE"

MOST_RECENT_SENTENCE_STATUS_DATE = "MOST_RECENT_SENTENCE_STATUS_DATE"
MOST_RECENT_SENTENCE_STATUS_CODE = "MOST_RECENT_SENTENCE_STATUS_SCD"

INCARCERATION_SENTENCE_LENGTH_YEARS = "BT_SLY"
INCARCERATION_SENTENCE_LENGTH_MONTHS = "BT_SLM"
INCARCERATION_SENTENCE_LENGTH_DAYS = "BT_SLD"
INCARCERATION_SENTENCE_MIN_RELEASE_TYPE = "BT_CRR"
INCARCERATION_SENTENCE_PAROLE_INELIGIBLE_YEARS = "BT_PIE"
INCARCERATION_SENTENCE_START_DATE = "BT_EM"
INCARCERATION_SENTENCE_PROJECTED_MIN_DATE = "BT_PC"
INCARCERATION_SENTENCE_PROJECTED_MAX_DATE = "BS_PD"

SUPERVISION_SENTENCE_LENGTH_YEARS = "BU_SBY"
SUPERVISION_SENTENCE_LENGTH_MONTHS = "BU_SBM"
SUPERVISION_SENTENCE_LENGTH_DAYS = "BU_SBD"
SUPERVISION_SENTENCE_START_DATE = "BU_SF"
SUPERVISION_SENTENCE_PROJECTED_COMPLETION_DATE = "BS_PD"

PERIOD_CLOSE_CODE = "END_STATUS_CODE"
PERIOD_CLOSE_CODE_SUBTYPE = "END_STATUS_SUBTYPE"
PERIOD_START_DATE = "SUB_SUBCYCLE_START_DT"
PERIOD_RELEASE_DATE = "SUB_SUBCYCLE_END_DT"
PERIOD_PURPOSE_FOR_INCARCERATION = "F1_PFI"

SUPERVISION_PERIOD_RELEASE_DATE = "SUPV_PERIOD_END_DT"
SUPERVISION_PERIOD_START_STATUSES = "START_STATUS_CODE_LIST"
SUPERVISION_PERIOD_END_STATUSES = "END_STATUS_CODE_LIST"

TAK026_STATUS_CYCLE_TERMINATION_REGEX = re.compile(r"99O\d{4}")
TAK026_STATUS_SUPERVISION_SENTENCE_COMPLETION_REGEX = re.compile(r"95O\d{4}")
TAK026_STATUS_SUPERVISION_PERIOD_TERMINATION_REGEX = re.compile(r"\d5O\d{4}")
TAK026_STATUS_SUPERVISION_PERIOD_START_REGEX = re.compile(r"\d5I\d{4}")

SUPERVISION_VIOLATION_VIOLATED_CONDITIONS = "VIOLATED_CONDITIONS"
SUPERVISION_VIOLATION_TYPES = "BY_VTY"
SUPERVISION_VIOLATION_RECOMMENDATIONS = "BY_VOR"

ORAS_ASSESSMENTS_DOC_ID = "E04"
ORAS_ASSESSMENT_ID = "FOCLIST"

# Recidiviz internal constants
VIOLATION_REPORT_ID_PREFIX = "R"
CITATION_ID_PREFIX = "C"
