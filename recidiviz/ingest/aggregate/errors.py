# Recidiviz - a platform for tracking granular recidivism metrics in real time
# Copyright (C) 2018 Recidiviz, Inc.
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
"""Errors raised by Aggregate Ingest."""


class AggregateIngestError(Exception):
    """Generic error when aggregate ingest fails."""


class AggregateDateParsingError(Exception):
    """Raised when a Date can't be parsed from an Aggregate Report."""


class FipsMergingError(Exception):
    """Raised when a scraped county_name can't be assigned a fips."""


class DataFrameCastError(Exception):
    """Raised when attempting to cast a non-existent DataFrame column."""
