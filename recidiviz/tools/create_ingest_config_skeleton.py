#  Recidiviz - a data platform for criminal justice reform
#  Copyright (C) 2021 Recidiviz, Inc.
#  #
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#  =============================================================================
#
"""Tool to create skeleton ingest config yamls from raw data dumps.

Usage:
    python -m recidiviz.tools.create_ingest_config_skeleton --state [us_xx] \
    --delimiter <field separator> (--file|--folder) [path_to_raw_table(s)] \
    [--allow-overwrite] [--initialize-state]

Example:
    python -m recidiviz.tools.create_ingest_config_skeleton --state-code us_xx \
    --delimiter '|' --path Xxandland/db/historical/
"""
import argparse
import logging
import os
import sys

from typing import List
from pandas import read_csv

from recidiviz.common.constants import states

PLACEHOLDER = "TO" + "DO"  # split tag so we don't trigger the linter


def make_config_directory(state_code: str) -> str:
    return os.path.join(
        os.path.split(os.path.dirname(__file__))[0],
        "ingest",
        "direct",
        "regions",
        state_code,
        "raw_data",
    )


def initialize_state_directories(state_code: str) -> None:
    config_directory = make_config_directory(state_code)
    os.makedirs(config_directory, exist_ok=True)
    base_config_filename = f"{state_code}_default.yaml"

    base_config_path = os.path.join(config_directory, base_config_filename)

    if os.path.exists(base_config_path):
        logging.error(
            "Default config file %s already exists. Cannot initialize state.",
            base_config_path,
        )
        sys.exit(1)

    with open(base_config_path, "w") as file:
        file.writelines(
            [
                f"default_encoding: {PLACEHOLDER}\n",
                f"default_separator: {PLACEHOLDER}\n",
            ]
        )


def write_skeleton_config(
    raw_table_path: str, state_code: str, delimiter: str, allow_overwrite: bool
) -> None:
    """Generates a config skeleton for the table at the given path"""
    table_name = os.path.basename(raw_table_path)
    table_name = os.path.splitext(table_name)[0]

    df = read_csv(raw_table_path, delimiter=delimiter)

    fields = list(df.columns)

    if len(fields) == 1:
        logging.error(
            "Unable to split header of %s on delimiter '%s'", raw_table_path, delimiter
        )
        return

    config_directory = make_config_directory(state_code)
    config_file_name = f"{state_code}_{table_name}.yaml"
    config_path = os.path.join(config_directory, config_file_name)

    if not allow_overwrite and os.path.exists(config_path):
        logging.info(
            "File %s already exists. Skipping skeleton generation", config_path
        )
        return

    config = [
        f"file_tag: {table_name}",
        "file_description: |-",
        f"  {PLACEHOLDER}",
        "primary_key_cols: []",
        "columns:",
    ]

    config += [f"  - name : {field}" for field in fields]

    with open(config_path, "w") as config_file:
        for line in config:
            config_file.write(line + "\n")


def create_ingest_config_skeleton(
    raw_table_paths: List[str],
    state_code: str,
    delimiter: str,
    allow_overwrite: bool,
    initialize_state: bool,
) -> None:
    """Reads the header off of a raw config file and generate a config yaml skeleton for it."""
    state_code = state_code.lower()

    if initialize_state:
        initialize_state_directories(state_code)
    elif not os.path.exists(make_config_directory(state_code)):
        logging.error(
            "Folder %s does not exist. Run with --initialize-state to create directory structure.",
            make_config_directory(state_code),
        )

    for path in raw_table_paths:
        write_skeleton_config(path, state_code, delimiter, allow_overwrite)


def parse_arguments(argv: List[str]) -> argparse.Namespace:
    """Parses the named arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--delimiter",
        dest="delimiter",
        help="String used to separate fields.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--state-code",
        dest="state_code",
        help="State to which this config belongs in the form US_XX.",
        type=str,
        choices=[state.value for state in states.StateCode],
        required=True,
    )

    file_group = parser.add_mutually_exclusive_group(required=True)

    file_group.add_argument(
        "--file",
        dest="file_path",
        help="Path to the raw DB file to generate a skeleton for.",
        type=str,
    )

    file_group.add_argument(
        "--folder",
        dest="folder_path",
        help="Path to folder containing raw DB files to generate skeleton for.",
        type=str,
    )

    parser.add_argument(
        "--allow-overwrite",
        dest="allow_overwrite",
        help="Flag to allow overwriting existing files.",
        action="store_true",
        required=False,
        default=False,
    )

    parser.add_argument(
        "--initialize-state",
        dest="initialize_state",
        help="Generate directory structure and base config file for the state.",
        action="store_true",
        required=False,
        default=False,
    )

    known_args, _ = parser.parse_known_args(argv)

    return known_args


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    args = parse_arguments(sys.argv)

    if args.file_path:
        create_ingest_config_skeleton(
            [args.file_path],
            args.state_code,
            args.delimiter,
            args.allow_overwrite,
            args.initialize_state,
        )
    else:
        # get all files in the supplied folder
        create_ingest_config_skeleton(
            [
                f"{args.folder_path}/{filename}"
                for filename in os.listdir(args.folder_path)
            ],
            args.state_code,
            args.delimiter,
            args.allow_overwrite,
            args.initialize_state,
        )
