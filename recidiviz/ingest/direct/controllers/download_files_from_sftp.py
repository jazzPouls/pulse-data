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
"""Class for interacting with and downloading files from SFTP servers"""
import datetime
import logging
import os
from functools import partial
from typing import Optional, List, Tuple

import pysftp
from pysftp import CnOpts
from paramiko import SFTPAttributes, SSHException
from paramiko.hostkeys import HostKeyEntry

from recidiviz.cloud_storage.gcs_file_system import GcsfsSftpFileContentsHandle
from recidiviz.cloud_storage.gcsfs_factory import GcsfsFactory
from recidiviz.cloud_storage.gcsfs_path import GcsfsDirectoryPath, GcsfsFilePath
from recidiviz.common.ingest_metadata import SystemLevel
from recidiviz.ingest.direct.controllers.direct_ingest_gcs_file_system import (
    DirectIngestGCSFileSystem,
)
from recidiviz.ingest.direct.controllers.gcsfs_direct_ingest_utils import (
    gcsfs_direct_ingest_directory_path_for_region,
)
from recidiviz.ingest.direct.sftp_download_delegate_factory import (
    SftpDownloadDelegateFactory,
)
from recidiviz.utils import secrets

RAW_INGEST_DIRECTORY = "raw_data"
BYTES_CONTENT_TYPE = "application/octet-stream"


class SftpAuth:
    """Handles authentication for a given SFTP server."""

    def __init__(
        self,
        hostname: str,
        username: Optional[str],
        password: Optional[str],
        connection_options: Optional[CnOpts],
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        # connection_options hold advanced options that help when creating a pysftp Connection
        # such as overriding where to check for hosts or enabling compression.
        self.connection_options = connection_options if connection_options else CnOpts()

    @staticmethod
    def set_up_connection_options(prefix: str, host: str) -> CnOpts:
        connection_options = CnOpts()
        try:
            connection_options.get_hostkey(host)
        except SSHException as s:
            hostkey = secrets.get_secret(f"{prefix}_hostkey")
            if hostkey is None:
                raise ValueError(
                    f"Unable to find hostkey for secret key {prefix}_hostkey"
                ) from s
            hostkeyEntry = HostKeyEntry.from_line(hostkey)
            if hostkeyEntry:
                key = hostkeyEntry.key
                name, keytype, _ = hostkey.split(" ")
                connection_options.hostkeys.add(name, keytype, key)
            else:
                raise ValueError(
                    f"Unable to add hostkey to connection_options for secret key {prefix}_hostkey"
                ) from s
        return connection_options

    @classmethod
    def for_region(cls, region_code: str) -> "SftpAuth":
        prefix = f"{region_code}_sftp"
        host = secrets.get_secret(f"{prefix}_host")
        if host is None:
            raise ValueError(f"Unable to find host name for secret key {prefix}_host")
        username = secrets.get_secret(f"{prefix}_username")
        password = secrets.get_secret(f"{prefix}_password")

        connection_options = SftpAuth.set_up_connection_options(prefix, host)

        return SftpAuth(host, username, password, connection_options)


class DownloadFilesFromSftpController:
    """Class for interacting with and downloading files from SFTP servers."""

    def __init__(
        self,
        project_id: str,
        region: str,
        lower_bound_update_datetime: Optional[datetime.datetime],
        gcs_destination_path: Optional[str] = None,
    ):
        self.project_id = project_id
        self.region = region.lower()

        self.auth = SftpAuth.for_region(region)
        self.delegate = SftpDownloadDelegateFactory.build(region_code=region)
        self.gcsfs = DirectIngestGCSFileSystem(GcsfsFactory.build())

        self.unable_to_download_items: List[str] = []
        self.downloaded_items: List[Tuple[str, datetime.datetime]] = []

        self.lower_bound_update_datetime = lower_bound_update_datetime
        self.bucket = (
            GcsfsDirectoryPath.from_absolute_path(
                gcsfs_direct_ingest_directory_path_for_region(
                    region, SystemLevel.STATE, project_id=self.project_id
                )
            )
            if gcs_destination_path is None
            else GcsfsDirectoryPath.from_absolute_path(gcs_destination_path)
        )
        self.download_dir = GcsfsDirectoryPath.from_dir_and_subdir(
            dir_path=self.bucket, subdir=RAW_INGEST_DIRECTORY
        )

    def _is_after_update_bound(self, sftp_attr: SFTPAttributes) -> bool:
        if self.lower_bound_update_datetime is None:
            return True
        update_time = datetime.datetime.fromtimestamp(sftp_attr.st_mtime)
        return update_time >= self.lower_bound_update_datetime

    def _fetch(
        self,
        connection: pysftp.Connection,
        file_path: str,
        file_timestamp: datetime.datetime,
    ) -> None:
        """Fetches data files from the SFTP, tracking which items downloaded and failed to download."""
        normalized_sftp_path = os.path.normpath(file_path)
        logging.info("Downloading %s into %s", normalized_sftp_path, self.download_dir)
        try:
            path = GcsfsFilePath.from_directory_and_file_name(
                dir_path=self.download_dir, file_name=normalized_sftp_path
            )
            self.gcsfs.upload_from_contents_handle_stream(
                path=path,
                contents_handle=GcsfsSftpFileContentsHandle(
                    sftp_connection=connection, local_file_path=file_path
                ),
                content_type=BYTES_CONTENT_TYPE,
            )
            logging.info("Post processing %s", path.uri())
            self.downloaded_items.append(
                (self.delegate.post_process_downloads(path, self.gcsfs), file_timestamp)
            )
        except IOError as e:
            logging.info(
                "Could not download %s into %s: %s",
                normalized_sftp_path,
                self.download_dir,
                e.args,
            )
            self.unable_to_download_items.append(file_path)

    def get_paths_to_download(self) -> List[Tuple[str, datetime.datetime]]:
        """Opens a connection to SFTP and based on the delegate, find and recursively list items
        that are after the update bound and match the delegate's criteria, returning items and
        corresponding timestamps that are to be downloaded."""
        with pysftp.Connection(
            host=self.auth.hostname,
            username=self.auth.username,
            password=self.auth.password,
            cnopts=self.auth.connection_options,
        ) as connection:
            remote_dirs = connection.listdir()
            root = self.delegate.root_directory(remote_dirs)
            dirs_with_attributes = connection.listdir_attr(root)
            paths_post_timestamp = {
                sftp_attr.filename: datetime.datetime.fromtimestamp(sftp_attr.st_mtime)
                for sftp_attr in dirs_with_attributes
                if self._is_after_update_bound(sftp_attr)
            }
            paths_to_download = self.delegate.filter_paths(
                list(paths_post_timestamp.keys())
            )

            files_to_download_with_timestamps: List[Tuple[str, datetime.datetime]] = []
            for path in paths_to_download:
                file_timestamp = paths_post_timestamp[path]
                if connection.isdir(path):

                    def set_file(
                        file_to_fetch: str, file_timestamp: datetime.datetime
                    ) -> None:
                        files_to_download_with_timestamps.append(
                            (file_to_fetch, file_timestamp)
                        )

                    connection.walktree(
                        remotepath=path,
                        fcallback=partial(set_file, file_timestamp=file_timestamp),
                        dcallback=lambda _: None,
                        ucallback=self.unable_to_download_items.append,
                        recurse=True,
                    )
                else:
                    files_to_download_with_timestamps.append((path, file_timestamp))
            return files_to_download_with_timestamps

    def clean_up(self) -> None:
        """Attempts to recursively remove any downloaded folders created as part of do_fetch."""
        try:
            logging.info("Cleaning up items in %s.", self.download_dir.uri())
            files_to_delete = self.gcsfs.ls_with_blob_prefix(
                bucket_name=self.bucket.abs_path(), blob_prefix=RAW_INGEST_DIRECTORY
            )
            for file in files_to_delete:
                self.gcsfs.delete(GcsfsFilePath.from_absolute_path(file.abs_path()))
        except Exception as e:
            logging.info(
                "%s could not be cleaned up due to an error %s.",
                self.download_dir.uri(),
                e.args,
            )

    def fetch_files(
        self, files_to_download_with_timestamps: List[Tuple[str, datetime.datetime]]
    ) -> None:
        """Opens up one connection and loops through all of the files with timestamps to upload
        to the GCS bucket."""
        with pysftp.Connection(
            host=self.auth.hostname,
            username=self.auth.username,
            password=self.auth.password,
            cnopts=self.auth.connection_options,
        ) as connection:
            for file_path, file_timestamp in files_to_download_with_timestamps:
                self._fetch(connection, file_path, file_timestamp)

    def do_fetch(self) -> Tuple[List[Tuple[str, datetime.datetime]], List[str]]:
        """Attempts to open an SFTP connection and download items, returning the corresponding paths
        and the timestamp associated, and also any unable to be downloaded."""
        logging.info(
            "Downloading raw files from SFTP server [%s] to ingest bucket [%s] for project [%s]",
            self.auth.hostname,
            self.bucket.uri(),
            self.project_id,
        )

        files_to_download_with_timestamps = self.get_paths_to_download()
        logging.info(
            "Found %s items to download from SFTP server [%s] to upload to ingest bucket [%s]",
            len(files_to_download_with_timestamps),
            self.auth.hostname,
            self.bucket,
        )

        self.fetch_files(files_to_download_with_timestamps)

        logging.info(
            "Download complete, successfully downloaded %s files to ingest bucket [%s] "
            "could not download %s files",
            len(self.downloaded_items),
            self.download_dir.uri(),
            len(self.unable_to_download_items),
        )
        return self.downloaded_items, self.unable_to_download_items
