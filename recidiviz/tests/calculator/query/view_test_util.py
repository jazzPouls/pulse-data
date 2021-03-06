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
"""Utility class for testing BQ views against Postgres"""

import logging
import re
from typing import Dict, Iterator, List, Optional, Set, Tuple, Type
import unittest

import attr
from google.cloud import bigquery
import pandas as pd
import pytest
import sqlalchemy
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.sql import sqltypes

from recidiviz.big_query.big_query_view import BigQueryViewBuilder
from recidiviz.persistence.database.session import Session
from recidiviz.tools.postgres import local_postgres_helpers


def _replace_iter(query: str, regex: str, replacement: str) -> str:
    compiled = re.compile(regex)
    for match in re.finditer(compiled, query):
        query = query.replace(match[0], replacement.format(**match.groupdict()))
    return query


@attr.s(frozen=True)
class MockTableSchema:
    """Defines the table schema to be used when mocking this table in Postgres"""

    data_types: Optional[Dict[str, sqltypes.SchemaType]] = attr.ib()

    @classmethod
    def from_sqlalchemy_table(cls, table: sqlalchemy.Table) -> "MockTableSchema":
        data_types = {}
        for column in table.columns:
            if isinstance(column.type, sqltypes.Enum):
                data_types[column.name] = sqltypes.String(255)
            else:
                data_types[column.name] = column.type
        return cls(data_types)

    @classmethod
    def from_big_query_schema_fields(
        cls, bq_schema: List[bigquery.SchemaField]
    ) -> "MockTableSchema":
        data_types = {}
        for field in bq_schema:
            field_type = bigquery.enums.SqlTypeNames(field.field_type)
            if field_type is bigquery.enums.SqlTypeNames.STRING:
                data_type = sqltypes.String(255)
            elif field_type is bigquery.enums.SqlTypeNames.INTEGER:
                data_type = sqltypes.Integer
            elif field_type is bigquery.enums.SqlTypeNames.FLOAT:
                data_type = sqltypes.Float
            elif field_type is bigquery.enums.SqlTypeNames.DATE:
                data_type = sqltypes.Date
            elif field_type is bigquery.enums.SqlTypeNames.BOOLEAN:
                data_type = sqltypes.Boolean
            else:
                raise ValueError(
                    f"Unhandled big query field type '{field_type}' for attribute '{field.name}'"
                )
            data_types[field.name] = data_type
        return cls(data_types)


_INITIAL_SUFFIX_ASCII = ord("a")


class NameGenerator(Iterator[str]):
    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix
        self.counter = 0

    def _get_name(self, counter: int) -> str:
        return self.prefix + chr(_INITIAL_SUFFIX_ASCII + counter)

    def __next__(self) -> str:
        type_name = self._get_name(self.counter)
        self.counter += 1
        return type_name

    def __iter__(self) -> Iterator[str]:
        return self

    def all_names_generated(self) -> List[str]:
        return [self._get_name(i) for i in range(self.counter)]


_CREATE_ARRAY_CONCAT_AGG_FUNC = """
CREATE AGGREGATE array_concat_agg (anyarray)
(
    sfunc = array_cat,
    stype = anyarray,
    initcond = '{}'
);
"""

_DROP_ARRAY_CONCAT_AGG_FUNC = """
DROP AGGREGATE array_concat_agg (anyarray)
"""


@pytest.mark.uses_db
class BaseViewTest(unittest.TestCase):
    """This is a utility class that allows BQ views to be tested using Postgres instead.

    This is NOT fully featured and has some shortcomings, most notably:
    1. It uses naive regexes to rewrite parts of the query. This works for the most part but may produce invalid
       queries in some cases. For instance, the lazy capture groups may capture the wrong tokens in nested function
       calls.
    2. Postgres can only use ORDINALS when unnesting and indexing into arrays, while BigQuery uses OFFSETS (or both).
       This does not translate the results (add or subtract one). So long as the query consistently uses one or the
       other, it should produce correct results.
    3. This does not (yet) support chaining of views. To test a view query, any tables or views that it queries from
       must be created and seeded with data using `create_table`.
    4. Not all BigQuery SQL syntax has been translated, and it is possible that some features may not have equivalent
       functionality in Postgres and therefore can't be translated.

    Given these, it may not make sense to use this for all of our views. If it prevents you from using BQ features that
    would be helpful, or creates more headaches than value it provides, it may not be necessary.
    """

    # Stores the on-disk location of the postgres DB for this test run
    temp_db_dir: Optional[str]

    postgres_engine: Optional[Engine]

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_db_dir = local_postgres_helpers.start_on_disk_postgresql_database()

    def setUp(self) -> None:
        # Stores the list of mock tables that have been created as (dataset_id, table_id) tuples.
        self.mock_bq_tables: Set[Tuple[str, str]] = set()

        self.type_name_generator = NameGenerator("__type_")
        self.postgres_engine = create_engine(
            local_postgres_helpers.on_disk_postgres_db_url()
        )

        # Implement ARRAY_CONCAT_AGG function that behaves the same (ARRAY_AGG fails on empty arrays)
        self._execute_statement(_CREATE_ARRAY_CONCAT_AGG_FUNC)

    def _execute_statement(self, statement: str) -> None:
        session = Session(bind=self.postgres_engine)
        try:
            session.execute(statement)
            session.commit()
        except Exception as e:
            logging.warning("Failed to cleanup: %s", e)
            session.rollback()
        finally:
            session.close()

    def tearDown(self) -> None:
        close_all_sessions()

        if self.mock_bq_tables:
            # Execute each statement one at a time for resilience.
            for dataset_id, table_id in self.mock_bq_tables:
                self._execute_statement(
                    f"DROP TABLE {self._to_postgres_table_name(dataset_id, table_id)}"
                )
            for type_name in self.type_name_generator.all_names_generated():
                self._execute_statement(f"DROP TYPE {type_name}")
        self._execute_statement(_DROP_ARRAY_CONCAT_AGG_FUNC)

        if self.postgres_engine is not None:
            self.postgres_engine.dispose()
            self.postgres_engine = None

    @classmethod
    def tearDownClass(cls) -> None:
        local_postgres_helpers.stop_and_clear_on_disk_postgresql_database(
            cls.temp_db_dir
        )

    def create_mock_bq_table(
        self,
        dataset_id: str,
        table_id: str,
        mock_schema: MockTableSchema,
        mock_data: pd.DataFrame,
    ) -> None:
        self.mock_bq_tables.add((dataset_id, table_id))
        mock_data.to_sql(
            name=self._to_postgres_table_name(dataset_id, table_id),
            con=self.postgres_engine,
            dtype=mock_schema.data_types,
        )

    def query_view(
        self,
        view_builder: BigQueryViewBuilder,
        data_types: Dict[str, Type],
        dimensions: List[str],
    ) -> pd.DataFrame:
        view_query = self._rewrite_sql(view_builder.build().view_query)
        results = pd.read_sql_query(view_query, con=self.postgres_engine)
        results = results.astype(data_types)
        # TODO(#5533): If we add `dimensions` to all `BigQueryViewBuilder`, instead of just
        # `MetricBigQueryViewBuilder`, then we can reuse that here instead of forcing the caller to specify them
        # manually.
        results = results.set_index(dimensions)
        return results.sort_index()

    @classmethod
    def _to_postgres_table_name(cls, dataset_id: str, table_id: str) -> str:
        # Postgres does not support '.' in table names, so we instead join them with an underscore.
        return "_".join([dataset_id, table_id])

    def _rewrite_sql(self, query: str) -> str:
        """Modifies the SQL query, translating BQ syntax to Postgres syntax where necessary."""
        query = self._rewrite_table_references(query)

        query = self._rewrite_unnest_with_offset(query)

        # Must index the array directly, instead of using OFFSET or ORDINAL
        query = _replace_iter(query, r"\[OFFSET\((?P<offset>.+?)\)\]", "[{offset}]")
        query = _replace_iter(query, r"\[ORDINAL\((?P<ordinal>.+?)\)\]", "[{ordinal}]")

        # Array concatenation is performed with the || operator
        query = _replace_iter(query, r"ARRAY_CONCAT\((?P<first>[^,]+?)\)", "({first})")
        query = _replace_iter(
            query,
            r"ARRAY_CONCAT\((?P<first>[^,]+?), (?P<second>[^,]+?)\)",
            "({first} || {second})",
        )

        # Postgres requires you to specify the dimension of the array to measure the length of. BigQuery doesn't
        # support multi-dimensional arrays so mapping to cardinality, which returns the total number of elements in an
        # array, provides the same behavior. Simply specifying 1 as the dimension to measure will differ in behavior
        # for empty arrays.
        query = _replace_iter(query, r"ARRAY_LENGTH", "CARDINALITY")

        # IN UNNEST doesn't work in postgres when passing an array column, instead use = ANY
        query = _replace_iter(query, r"IN UNNEST", "= ANY")

        # ENDS_WITH doesn't exist in postgres so use LIKE instead
        query = _replace_iter(
            query,
            r"ENDS_WITH\((?P<column>.+?), \'(?P<predicate>.+?)\'\)",
            "{column} LIKE '%%{predicate}'",
        )

        # Postgres doesn't have ANY_VALUE, but since we don't care what the value is we can just use MIN
        query = _replace_iter(query, r"ANY_VALUE\((?P<column>.+?)\)", "MIN({column})")

        # The interval must be quoted.
        query = _replace_iter(
            query,
            r"INTERVAL (?P<num>\d+?) (?P<unit>\w+?)(?P<end>\W)",
            "INTERVAL '{num} {unit}'{end}",
        )

        # Postgres doesn't have DATE_DIFF where you can specify the units to return, but subtracting two dates always
        # returns the number of days between them.
        query = _replace_iter(
            query,
            r"DATE_DIFF\((?P<first>.+?), (?P<second>.+?), DAY\)",
            "({first} - {second})",
        )

        # Date arithmetic just uses operators (e.g. -), not function calls
        query = _replace_iter(
            query, r"DATE_SUB\((?P<first>.+?), (?P<second>.+?)\)", "{first} - {second}"
        )

        # The parameters for DATE_TRUNC are in the opposite order, and the interval must be quoted.
        query = _replace_iter(
            query,
            r"DATE_TRUNC\((?P<first>.+?), (?P<second>.+?)\)",
            "DATE_TRUNC('{second}', {first})",
        )

        # LAST_DAY doesn't exist in postgres, so replace with the logic to calculate it
        query = _replace_iter(
            query,
            r"LAST_DAY\((?P<column>.+?)\)",
            "(DATE_TRUNC('MONTH', {column} + INTERVAL '1 MONTH')::date - 1)",
        )

        # Postgres doesn't have SAFE_DIVIDE, instead we use NULLIF to make the denominator NULL if it was going to be
        # zero, which will make the whole expression NULL, the same behavior as SAFE_DIVIDE.
        query = _replace_iter(
            query,
            r"SAFE_DIVIDE\((?P<first>.+?), (?P<second>.+?)\)",
            "({first} / NULLIF({second}, 0))",
        )

        query = self._rewrite_structs(query)

        return query

    def _rewrite_table_references(self, query: str) -> str:
        """Maps BQ table references to the underlying Postgres tables"""
        table_reference_regex = re.compile(
            r"`[\w-]+\.(?P<dataset_id>[\w-]+)\.(?P<table_id>[\w-]+)`"
        )
        for match in re.finditer(table_reference_regex, query):
            table_reference = match.group()
            dataset_id, table_id = match.groups()
            if (dataset_id, table_id) not in self.mock_bq_tables:
                raise KeyError(
                    f"Table {table_reference} does not exist, must be created via create_mock_bq_table."
                )
            query = query.replace(
                table_reference, self._to_postgres_table_name(dataset_id, table_id)
            )
        return query

    def _rewrite_unnest_with_offset(self, query: str) -> str:
        """UNNEST WITH OFFSET must be transformed significantly, and returns the ordinality instead of the offset."""
        # TODO(#5081): If we move dimensions to their own tables, we may be able to get rid of the unnest clauses as
        # well as this logic to rewrite them.

        # Postgres requires a table alias when aliasing the outputs of unnest and it must be unique for each unnest. We
        # just use the letters of the alphabet for this starting with 'a'.
        table_alias_name_generator = NameGenerator()
        with_offset_regex = re.compile(
            r",\s+UNNEST\((?P<colname>.+?)\) AS (?P<unnestname>\w+?) "
            r"WITH OFFSET (?P<offsetname>\w+?)(?P<end>\W)"
        )
        match = re.search(with_offset_regex, query)
        while match:
            query = query.replace(
                match[0],
                f"\nLEFT JOIN LATERAL UNNEST({match[1]}) "
                f"WITH ORDINALITY AS {next(table_alias_name_generator)}({match[2]}, {match[3]}) ON TRUE{match[4]}",
            )
            match = re.search(with_offset_regex, query)
        return query

    def _rewrite_structs(self, query: str) -> str:
        """Define STRUCTS as new composite types and cast the elements to that type.

        Postgres supports creating anonymous types with ROW but does not support naming their fields so we have to
        cast them to a type instead.
        Note: This only supports the `STRUCT<field_name field_type, ...>` syntax.
        """
        # TODO(#5081): If we move dimensions to their own tables, we may be able to get rid of the structs as well as
        # this logic to rewrite them.
        struct_regex = re.compile(r"STRUCT<(?P<types>.+)>\((?P<fields>.+?)\)")
        match = re.search(struct_regex, query)
        while match:
            type_name = next(self.type_name_generator)

            converted_fields = []
            # The fields are of the form "field1 type1, field2 type2, ..."
            # We have to parse them so that we can convert the types to postgres types.
            for field in match[1].split(","):
                name, field_type = field.strip().split(" ")
                if field_type == "string":
                    converted_type = "text"
                else:
                    converted_type = field_type
                converted_fields.append((name, converted_type))
            field_stanza = ", ".join(
                [f"{name} {field_type}" for name, field_type in converted_fields]
            )

            # Create the type at the start of the query
            query = f"CREATE TYPE {type_name} AS ({field_stanza});\n{query}"

            # Instead of building a STRUCT, use ROW and cast to our type
            query = query.replace(match[0], f"CAST(ROW({match[2]}) AS {type_name})")

            match = re.search(struct_regex, query)
        return query
