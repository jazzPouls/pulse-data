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
"""Defines the base class for all table classes in the state schema.

For actual schema definitions, see /state/schema.py.
"""

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from recidiviz.persistence.database.database_entity import DatabaseEntity

# Base class for all table classes in the state schema
StateBase: DeclarativeMeta = declarative_base(cls=DatabaseEntity)
