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
"""A static reference cache for converting raw incoming codes into normalized
county codes."""
from typing import Dict

COUNTY_CODES: Dict[str, str] = {
    "ADAI": "US_MO_ADAIR",
    "ANDR": "US_MO_ANDREW",
    "ATCH": "US_MO_ATCHISON",
    "AUDR": "US_MO_AUDRAIN",
    "BARR": "US_MO_BARRY",
    "BART": "US_MO_BARTON",
    "BATE": "US_MO_BATES",
    "BENT": "US_MO_BENTON",
    "BOLL": "US_MO_BOLLINGER",
    "BOON": "US_MO_BOONE",
    "BUCH": "US_MO_BUCHANAN",
    "BUTL": "US_MO_BUTLER",
    "CALD": "US_MO_CALDWELL",
    "CALL": "US_MO_CALLAWAY",
    "CAMD": "US_MO_CAMDEN",
    "CAPE": "US_MO_CAPE_GIRARDEAU",
    "CARR": "US_MO_CARROLL",
    "CART": "US_MO_CARTER",
    "CASS": "US_MO_CASS",
    "CEDA": "US_MO_CEDAR",
    "CHAR": "US_MO_CHARITON",
    "CHRI": "US_MO_CHRISTIAN",
    "CLAR": "US_MO_CLARK",
    "CLAY": "US_MO_CLAY",
    "CLIN": "US_MO_CLINTON",
    "COLE": "US_MO_COLE",
    "COOP": "US_MO_COOPER",
    "CRAW": "US_MO_CRAWFORD",
    "DADE": "US_MO_DADE",
    "DALL": "US_MO_DALLAS",
    "DAVI": "US_MO_DAVIESS",
    "DEKA": "US_MO_DEKALB",
    "DENT": "US_MO_DENT",
    "DOUG": "US_MO_DOUGLAS",
    "DUNK": "US_MO_DUNKLIN",
    "FRAN": "US_MO_FRANKLIN",
    "GASC": "US_MO_GASCONADE",
    "GENT": "US_MO_GENTRY",
    "GREE": "US_MO_GREENE",
    "GRUN": "US_MO_GRUNDY",
    "HARR": "US_MO_HARRISON",
    "HENR": "US_MO_HENRY",
    "HICK": "US_MO_HICKORY",
    "HOLT": "US_MO_HOLT",
    "HOWA": "US_MO_HOWARD",
    "HOWE": "US_MO_HOWELL",
    "IRON": "US_MO_IRON",
    "JACK": "US_MO_JACKSON",
    "JASP": "US_MO_JASPER",
    "JEFF": "US_MO_JEFFERSON",
    "JOHN": "US_MO_JOHNSON",
    "KNOX": "US_MO_KNOX",
    "LACL": "US_MO_LACLEDE",
    "LAFA": "US_MO_LAFAYETTE",
    "LAWR": "US_MO_LAWRENCE",
    "LEWI": "US_MO_LEWIS",
    "LINC": "US_MO_LINCOLN",
    "LINN": "US_MO_LINN",
    "LIVI": "US_MO_LIVINGSTON",
    "MACO": "US_MO_MACON",
    "MADI": "US_MO_MADISON",
    "MARE": "US_MO_MARIES",
    "MARI": "US_MO_MARION",
    "MCDO": "US_MO_MCDONALD",
    "MERC": "US_MO_MERCER",
    "MILL": "US_MO_MILLER",
    "MISS": "US_MO_MISSISSIPPI",
    "MONI": "US_MO_MONITEAU",
    "MONR": "US_MO_MONROE",
    "MONT": "US_MO_MONTGOMERY",
    "MORG": "US_MO_MORGAN",
    "NEWM": "US_MO_NEW_MADRID",
    "NEWT": "US_MO_NEWTON",
    "NODA": "US_MO_NODAWAY",
    "OREG": "US_MO_OREGON",
    "OSAG": "US_MO_OSAGE",
    "OZAR": "US_MO_OZARK",
    "PEMI": "US_MO_PEMISCOT",
    "PERR": "US_MO_PERRY",
    "PETT": "US_MO_PETTIS",
    "PHEL": "US_MO_PHELPS",
    "PIKE": "US_MO_PIKE",
    "PLAT": "US_MO_PLATTE",
    "POLK": "US_MO_POLK",
    "PULA": "US_MO_PULASKI",
    "PUTN": "US_MO_PUTNAM",
    "RALL": "US_MO_RALLS",
    "RAND": "US_MO_RANDOLPH",
    "RAY": "US_MO_RAY",
    "REYN": "US_MO_REYNOLDS",
    "RIPL": "US_MO_RIPLEY",
    "SALI": "US_MO_SALINE",
    "SCHU": "US_MO_SCHUYLER",
    "SCOL": "US_MO_SCOTLAND",
    "SCOT": "US_MO_SCOTT",
    "SHAN": "US_MO_SHANNON",
    "SHEL": "US_MO_SHELBY",
    "STCH": "US_MO_ST_CHARLES",
    "STCL": "US_MO_ST_CLAIR",
    "STEG": "US_MO_STE_GENEVIEVE",
    "STFR": "US_MO_ST_FRANCOIS",
    "STLC": "US_MO_ST_LOUIS_CITY",
    "STLO": "US_MO_ST_LOUIS_COUNTY",
    "STOD": "US_MO_STODDARD",
    "STON": "US_MO_STONE",
    "SULL": "US_MO_SULLLIVAN",
    "TANE": "US_MO_TANEY",
    "TEXA": "US_MO_TEXAS",
    "VERN": "US_MO_VERNON",
    "WARR": "US_MO_WARREN",
    "WASH": "US_MO_WASHINGTON",
    "WAYN": "US_MO_WAYNE",
    "WEBS": "US_MO_WEBSTER",
    "WORT": "US_MO_WORTH",
    "WRIG": "US_MO_WRIGHT",
    "OTST": "OUT_OF_STATE",
}
