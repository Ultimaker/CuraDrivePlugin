# Copyright (c) 2017 Ultimaker B.V.
from datetime import datetime
from threading import Thread
from typing import Optional

import requests

from UM.Logger import Logger
from UM.Signal import Signal
from cura.Api import CuraApi
from curaDrivePlugin.UploadBackupJob import UploadBackupJob
from .authorization.AuthorizationService import AuthorizationService
from .Settings import Settings


class DriveApiService:
    """
    The DriveApiService is responsible for interacting with the CuraDrive API and Cura's backup handling.
    """

    GET_BACKUPS_URL = "{}/backups".format(Settings.DRIVE_API_URL)
    PUT_BACKUP_URL = "{}/backups".format(Settings.DRIVE_API_URL)

    # Re-used instance of the Cura plugin API.
    api = CuraApi()

    # Emit signal when restoring backup started or finished.
    onRestoringStateChanged = Signal()

    # Emit signal when creating backup started or finished.
    onCreatingStateChanged = Signal()

    def __init__(self, authorization_service: "AuthorizationService"):
        self._authorization_service = authorization_service

    def getBackups(self) -> list:
        """Get all backups from the API."""
        backup_list_request = requests.get(self.GET_BACKUPS_URL, headers={
            "Authorization": "Bearer {}".format(self._authorization_service.getAccessToken())
        })
        if backup_list_request.status_code != 200:
            Logger.log("w", "Could not get backups list from remote: %s", backup_list_request.text)
            return []
        return backup_list_request.json()["data"]

    def createBackup(self) -> None:
        """Create a backup and upload it to CuraDrive cloud storage."""
        self.onCreatingStateChanged.emit(True)

        # Create the backup.
        backup_zip_file, backup_meta_data = self.api.backups.createBackup()
        if not backup_zip_file or not backup_meta_data:
            self.onCreatingStateChanged.emit(False, "Could not create backup.")
            return

        # Create an upload entry for the backup.
        timestamp = datetime.now().isoformat()
        backup_meta_data["description"] = "{}.backup.{}.cura.zip".format(timestamp, backup_meta_data["cura_release"])
        backup_upload_url = self._requestBackupUpload(backup_meta_data, len(backup_zip_file))
        if not backup_upload_url:
            self.onCreatingStateChanged.emit(False, "Could not upload backup.")
            return

        # Upload the backup to storage.
        upload_backup_job = UploadBackupJob(backup_upload_url, backup_zip_file)
        upload_backup_job.finished.connect(self._onUploadFinished)
        upload_backup_job.start()

    def _onUploadFinished(self, job: "UploadBackupJob") -> None:
        """
        Callback handler for the upload job.
        :param job: The executed job.
        """
        if job.backup_upload_error_message != "":
            # If the job contains an error message we pass it along so the UI can display it.
            self.onCreatingStateChanged.emit(False, job.backup_upload_error_message)
        else:
            self.onCreatingStateChanged.emit(False)

    def restoreBackup(self, backup: dict) -> None:
        """
        Restore a previously exported backup from cloud storage.
        :param backup: A dict containing an entry from the API list response.
        """
        self.onRestoringStateChanged.emit(True)
        download_url = backup.get("download_url")
        if not download_url or download_url == "":
            self.onRestoringStateChanged.emit(False)

        # self.api.backups.restoreBackup()
        # TODO: download backup file and offer to Cura.

    def _requestBackupUpload(self, backup_metadata: dict, backup_size: int) -> Optional[str]:
        """
        Request a backup upload slot from the API.
        :param backup_metadata: A dict containing some meta data about the backup.
        :param backup_size: The size of the backup file in bytes.
        :return: The upload URL for the actual backup file if successful, otherwise None.
        """
        backup_upload_request = requests.put(self.PUT_BACKUP_URL, json={
            "data": {
                "backup_size": backup_size,
                "metadata": backup_metadata
            }
        }, headers={
            "Authorization": "Bearer {}".format(self._authorization_service.getAccessToken())
        })
        if backup_upload_request.status_code != 200:
            Logger.log("w", "Could not request backup upload: %s", backup_upload_request.text)
            return None
        return backup_upload_request.json()["data"]["upload_url"]

    def _downloadBackupFile(self):
        pass

    def _passBackupToCura(self):
        pass
