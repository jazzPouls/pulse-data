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
"""Creates pseudo lock manager class built on GCSFS.
This isn't a traditional lock and is not suitable for all the general use cases."""
from contextlib import contextmanager
from datetime import datetime
from typing import Iterator, Optional

from recidiviz.cloud_storage.gcsfs_factory import GcsfsFactory
from recidiviz.cloud_storage.gcsfs_path import GcsfsFilePath
from recidiviz.utils import metadata


POSTGRES_TO_BQ_EXPORT_RUNNING_LOCK_NAME = "EXPORT_PROCESS_RUNNING_"
GCS_TO_POSTGRES_INGEST_RUNNING_LOCK_NAME = "INGEST_PROCESS_RUNNING_"


class GCSPseudoLockManager:
    """Class implementing pseudo lock manager using GCS File System. Not a general locks class - may have race
    conditions when locks state altered by multiple processes. A single lock is only ever acquired and released by one
    process, but its presence may be read or examined by another process"""

    _TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"

    def __init__(self, project_id: Optional[str] = None):
        if not project_id:
            project_id = metadata.project_id()
        self.fs = GcsfsFactory.build()
        self.bucket_name = f"{project_id}-gcslock"

    def no_active_locks_with_prefix(self, prefix: str) -> bool:
        """Checks to see if any locks exist with prefix"""
        return (
            len(
                self.fs.ls_with_blob_prefix(
                    bucket_name=self.bucket_name, blob_prefix=prefix
                )
            )
            == 0
        )

    def unlock_locks_with_prefix(self, prefix: str) -> None:
        locks_with_prefix = self.fs.ls_with_blob_prefix(
            bucket_name=self.bucket_name, blob_prefix=prefix
        )
        if len(locks_with_prefix) == 0:
            raise GCSPseudoLockDoesNotExist(
                f"No locks with the prefix {prefix} exist in the bucket "
                f"{self.bucket_name}"
            )
        for lock in locks_with_prefix:
            if isinstance(lock, GcsfsFilePath):
                self.fs.delete(lock)

    def lock(self, name: str, contents: Optional[str] = None) -> None:
        """ "Locks @param name by generating new file. If has @param contents, body of new file is contents.
        Otherwise sets body of file to json formatted time and uuid.
        """
        if self.is_locked(name):
            raise GCSPseudoLockAlreadyExists(
                f"Lock with the name {name} already exists in the bucket "
                f"{self.bucket_name}"
            )
        if contents is None:
            contents = datetime.now().strftime(self._TIME_FORMAT)
        path = GcsfsFilePath(bucket_name=self.bucket_name, blob_name=name)
        self.fs.upload_from_string(path, contents, "text/plain")

    def unlock(self, name: str) -> None:
        """Unlocks @param name by deleting file with name"""
        if self.is_locked(name):
            path = GcsfsFilePath(bucket_name=self.bucket_name, blob_name=name)
            self.fs.delete(path)
        else:
            raise GCSPseudoLockDoesNotExist(
                f"Lock with the name {name} does not yet exist in the bucket "
                f"{self.bucket_name}"
            )

    def is_locked(self, name: str) -> bool:
        """Checks if @param name is locked by checking if file exists. Returns true if locked, false if unlocked"""
        path = GcsfsFilePath(bucket_name=self.bucket_name, blob_name=name)
        return self.fs.exists(path)

    def get_lock_contents(self, name: str) -> str:
        """Returns contents of specified lock as string"""
        path = GcsfsFilePath(bucket_name=self.bucket_name, blob_name=name)
        if not self.fs.exists(path):
            raise GCSPseudoLockDoesNotExist(
                f"Lock with the name {name} does not yet exist in the bucket "
                f"{self.bucket_name}"
            )
        contents = self.fs.download_as_string(path)
        return contents

    @contextmanager
    def using_lock(self, name: str, contents: Optional[str] = None) -> Iterator[None]:
        self.lock(name, contents)
        try:
            yield
        finally:
            self.unlock(name)


class GCSPseudoLockAlreadyExists(ValueError):
    pass


class GCSPseudoLockDoesNotExist(ValueError):
    pass
