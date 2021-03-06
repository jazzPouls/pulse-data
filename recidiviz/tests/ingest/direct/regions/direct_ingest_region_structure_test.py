# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2020 Recidiviz, Inc.
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
"""Tests that each regions direct ingest directory is set up properly."""
import abc
import os
import re
import unittest
from types import ModuleType
from typing import Callable, List

import yaml
from mock import patch
from parameterized import parameterized

from recidiviz.ingest.direct import regions
from recidiviz.ingest.direct import templates
from recidiviz.ingest.direct.controllers.direct_ingest_raw_file_import_manager import (
    DirectIngestRegionRawFileConfig,
    DirectIngestRawFileConfig,
)
from recidiviz.common.constants.states import StateCode
from recidiviz.ingest.direct.controllers.direct_ingest_raw_table_migration import (
    UpdateRawTableMigration,
)
from recidiviz.ingest.direct.controllers.direct_ingest_raw_table_migration_collector import (
    DirectIngestRawTableMigrationCollector,
)
from recidiviz.ingest.direct.controllers.direct_ingest_view_collector import (
    DirectIngestPreProcessedIngestViewCollector,
)
from recidiviz.ingest.direct.controllers.gcsfs_direct_ingest_controller import (
    GcsfsDirectIngestController,
)
from recidiviz.ingest.direct.direct_ingest_region_utils import (
    get_existing_region_dir_names,
    get_existing_region_dir_paths,
)
from recidiviz.utils.environment import GCPEnvironment
from recidiviz.utils.metadata import local_project_id_override
from recidiviz.utils.regions import get_region

_REGION_REGEX = re.compile(r"us_[a-z]{2}(_[a-z]+)?")


class DirectIngestRegionDirStructureBase:
    """Tests that each regions direct ingest directory is set up properly."""

    def setUp(self) -> None:
        self.bq_client_patcher = patch("google.cloud.bigquery.Client")
        self.storage_client_patcher = patch("google.cloud.storage.Client")
        self.task_client_patcher = patch("google.cloud.tasks_v2.CloudTasksClient")
        self.bq_client_patcher.start()
        self.storage_client_patcher.start()
        self.task_client_patcher.start()

    def tearDown(self) -> None:
        self.bq_client_patcher.stop()
        self.storage_client_patcher.stop()
        self.task_client_patcher.stop()

    @property
    @abc.abstractmethod
    def region_dir_names(self) -> List[str]:
        pass

    @property
    @abc.abstractmethod
    def region_dir_paths(self) -> List[str]:
        pass

    @property
    @abc.abstractmethod
    def region_module_override(self) -> ModuleType:
        pass

    @property
    @abc.abstractmethod
    def test(self) -> unittest.TestCase:
        pass

    def test_region_dirname_matches_pattern(self) -> None:
        for d in self.region_dir_names:
            self.test.assertIsNotNone(
                re.match(_REGION_REGEX, d),
                f"Region [{d}] does not match expected region pattern.",
            )

    def run_check_valid_yamls_exist_in_all_regions(
        self,
        generate_yaml_name_fn: Callable[[str], str],
        validate_contents_fn: Callable[[str, object], None],
    ) -> None:
        for dir_path in self.region_dir_paths:
            region_code = os.path.basename(dir_path)

            yaml_path = os.path.join(dir_path, generate_yaml_name_fn(region_code))
            self.test.assertTrue(
                os.path.exists(yaml_path), f"Path [{yaml_path}] does not exist."
            )
            with open(yaml_path, "r") as ymlfile:
                file_contents = yaml.full_load(ymlfile)
                self.test.assertTrue(file_contents)
                validate_contents_fn(yaml_path, file_contents)

    def test_manifest_yaml_format(self) -> None:
        def validate_manifest_contents(file_path: str, file_contents: object) -> None:

            if not isinstance(file_contents, dict):
                self.test.fail(
                    f"File contents type [{type(file_contents)}], expected dict."
                )

            manifest_yaml_required_keys = [
                "agency_name",
                "agency_type",
                "timezone",
                "environment",
                "shared_queue",
                "jurisdiction_id",
            ]

            for k in manifest_yaml_required_keys:
                self.test.assertTrue(
                    k in file_contents, f"Key [{k}] not in [{file_path}]"
                )
                self.test.assertTrue(
                    file_contents[k], f"Contents of key [{k}] are falsy"
                )

        self.run_check_valid_yamls_exist_in_all_regions(
            lambda region_code: "manifest.yaml", validate_manifest_contents
        )

    def test_region_controller_exists_and_builds(self) -> None:
        for dir_path in self.region_dir_paths:
            region_code = os.path.basename(dir_path)
            controller_path = os.path.join(dir_path, f"{region_code}_controller.py")
            self.test.assertTrue(
                os.path.exists(controller_path),
                f"Path [{controller_path}] does not exist.",
            )

            region = get_region(
                region_code,
                is_direct_ingest=True,
                region_module_override=self.region_module_override,
            )
            with local_project_id_override("project"):
                self.test.assertIsNotNone(region.get_ingestor_class())

    def test_region_controller_builds(self) -> None:
        for dir_path in self.region_dir_paths:
            region_code = os.path.basename(dir_path)

            region = get_region(
                region_code,
                is_direct_ingest=True,
                region_module_override=self.region_module_override,
            )
            with local_project_id_override("project"):
                self.test.assertIsNotNone(region.get_ingestor())

    def test_raw_files_yaml_parses_all_regions(self) -> None:
        for region_code in self.region_dir_names:
            region = get_region(
                region_code,
                is_direct_ingest=True,
                region_module_override=self.region_module_override,
            )

            controller_class = region.get_ingestor_class()
            if not issubclass(controller_class, GcsfsDirectIngestController):
                continue

            builders = DirectIngestPreProcessedIngestViewCollector(
                region, controller_class.get_file_tag_rank_list()
            ).collect_view_builders()

            raw_file_manager = DirectIngestRegionRawFileConfig(
                region_code=region.region_code,
                region_module=self.region_module_override,
            )

            if builders or raw_file_manager.raw_file_configs:
                if region.raw_data_bq_imports_enabled_env is not None:
                    self.test.assertTrue(raw_file_manager.raw_file_configs)
                config_file_tags = set()
                for config in raw_file_manager.raw_file_configs.values():
                    self.test.assertTrue(
                        config.file_tag not in config_file_tags,
                        f"Multiple raw file configs defined with the same "
                        f"file_tag [{config.file_tag}]",
                    )
                    config_file_tags.add(config.file_tag)

    @parameterized.expand(
        [
            ("build_prod", "recidiviz-123", GCPEnvironment.PRODUCTION.value),
            ("build_staging", "recidiviz-staging", GCPEnvironment.STAGING.value),
        ]
    )
    def test_collect_and_build_ingest_view_builders(
        self, _name: str, project_id: str, environment: GCPEnvironment
    ) -> None:
        with patch(
            "recidiviz.utils.environment.get_gcp_environment", return_value=environment
        ):
            with patch("recidiviz.utils.metadata.project_id", return_value=project_id):
                for region_code in self.region_dir_names:
                    region = get_region(
                        region_code,
                        is_direct_ingest=True,
                        region_module_override=self.region_module_override,
                    )

                    controller_class = region.get_ingestor_class()
                    if not issubclass(controller_class, GcsfsDirectIngestController):
                        continue

                    builders = DirectIngestPreProcessedIngestViewCollector(
                        region, controller_class.get_file_tag_rank_list()
                    ).collect_view_builders()
                    for builder in builders:
                        builder.build()

    def test_collect_and_build_raw_table_migrations(self) -> None:
        with patch("recidiviz.utils.metadata.project_id", return_value="recidiviz-789"):
            for region_code in self.region_dir_names:
                raw_file_manager = DirectIngestRegionRawFileConfig(
                    region_code=region_code, region_module=self.region_module_override
                )
                collector = DirectIngestRawTableMigrationCollector(
                    region_code, regions_module_override=self.region_module_override
                )
                # Test this doesn't crash
                _ = collector.collect_raw_table_migration_queries()

                # Check that migrations are valid
                migrations = collector.collect_raw_table_migrations()
                for migration in migrations:
                    self.test.assertTrue(
                        migration.file_tag in raw_file_manager.raw_file_tags,
                        f"Tag {migration.file_tag} listed in migration for region "
                        f"[{region_code}] is not listed in config.",
                    )

                    raw_file_config = raw_file_manager.raw_file_configs[
                        migration.file_tag
                    ]
                    for col_name, _value in migration.filters:
                        self.assertColumnIsDocumented(
                            migration.file_tag, col_name, raw_file_config
                        )
                    if isinstance(migration, UpdateRawTableMigration):
                        for col_name, _value in migration.updates:
                            self.assertColumnIsDocumented(
                                migration.file_tag, col_name, raw_file_config
                            )

    def assertColumnIsDocumented(
        self, file_tag: str, col_name: str, raw_file_config: DirectIngestRawFileConfig
    ) -> None:
        documented_column_names = {
            c.name for c in raw_file_config.columns if c.description
        }
        self.test.assertTrue(
            col_name in documented_column_names,
            f"Found column [{col_name}] listed as a filter column in a migration for file "
            f"tag [{file_tag}] which either not listed or missing a docstring.",
        )


class DirectIngestRegionDirStructure(
    DirectIngestRegionDirStructureBase, unittest.TestCase
):
    @property
    def region_dir_names(self) -> List[str]:
        return get_existing_region_dir_names()

    @property
    def region_dir_paths(self) -> List[str]:
        return get_existing_region_dir_paths()

    @property
    @abc.abstractmethod
    def test(self) -> unittest.TestCase:
        return self

    @property
    def region_module_override(self) -> ModuleType:
        return regions

    def test_regions_are_clean(self) -> None:
        """Check that all existing region directories start with a valid state code."""
        for region in self.region_dir_names:
            self.test.assertTrue(StateCode.is_state_code(region[:5]))


class DirectIngestRegionTemplateDirStructure(
    DirectIngestRegionDirStructureBase, unittest.TestCase
):
    @property
    def region_dir_names(self) -> List[str]:
        return ["us_xx"]

    @property
    def region_dir_paths(self) -> List[str]:
        return [
            os.path.join(os.path.dirname(templates.__file__), d)
            for d in self.region_dir_names
        ]

    @property
    def test(self) -> unittest.TestCase:
        return self

    @property
    def region_module_override(self) -> ModuleType:
        return templates
