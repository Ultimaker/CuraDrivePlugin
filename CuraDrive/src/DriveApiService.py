# Copyright (c) 2017 Ultimaker B.V.
from datetime import datetime
from typing import Optional, List, Dict

import requests

from UM.Logger import Logger
from UM.Message import Message
from UM.Signal import Signal

from cura.Api import CuraApi

from ..lib.CuraPluginOAuth2Module.OAuth2Client.AuthorizationService import AuthorizationService

from .UploadBackupJob import UploadBackupJob
from .Settings import Settings


class DriveApiService:
    """
    The DriveApiService is responsible for interacting with the CuraDrive API and Cura's backup handling.
    """

    GET_BACKUPS_URL = "{}/backups".format(Settings.DRIVE_API_URL)
    PUT_BACKUP_URL = "{}/backups".format(Settings.DRIVE_API_URL)
    DELETE_BACKUP_URL = "{}/backups".format(Settings.DRIVE_API_URL)

    # Re-used instance of the Cura plugin API.
    api = CuraApi()

    # Emit signal when restoring backup started or finished.
    onRestoringStateChanged = Signal()

    # Emit signal when creating backup started or finished.
    onCreatingStateChanged = Signal()

    def __init__(self, authorization_service: "AuthorizationService"):
        self._authorization_service = authorization_service

    def getBackups(self) -> List[Dict[str, any]]:
        """Get all backups from the API."""
        access_token = self._getAccessToken()
        if not access_token:
            Logger.log("w", "Could not get access token.")
            return []

        backup_list_request = requests.get(self.GET_BACKUPS_URL, headers={
            "Authorization": "Bearer {}".format(access_token)
        })
        if backup_list_request.status_code not in (200, 201):
            Logger.log("w", "Could not get backups list from remote: %s", backup_list_request.text)
            Message(Settings.translatable_messages["get_backups_error"], title = Settings.MESSAGE_TITLE,
                    lifetime = 10).show()
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

    def restoreBackup(self, backup: Dict[str, any]) -> None:
        """
        Restore a previously exported backup from cloud storage.
        :param backup: A dict containing an entry from the API list response.
        """
        # TODO: validate dict (or make it a model?)
        self.onRestoringStateChanged.emit(True)
        download_url = backup.get("download_url")
        if not download_url or download_url == "":
            # If there is no download URL, we can't restore the backup.
            self.onRestoringStateChanged.emit(False, Settings.translatable_messages["backup_restore_error_message"])

        download_package = requests.get(download_url, stream=True)
        if download_package.status_code != 200:
            # Something went wrong when attempting to download the backup.
            Logger.log("w", "Could not download backup from url %s: %s", download_url, download_package.text)
            return

        # We store the file in a temporary path fist to ensure integrity.
        temporary_backup_path = "/tmp/cura-backup-{}".format(backup.get("backup_id"))
        with open(temporary_backup_path, "wb") as f:
            for chunk in download_package:
                f.write(chunk)

        # TODO: check md5 hash of downloaded file

        with open(temporary_backup_path, "rb") as f:
            self.api.backups.restoreBackup(f.read(), backup.get("data"))

    def deleteBackup(self, backup_id: str) -> bool:
        """
        Delete a backup from the server by ID.
        :param backup_id: The ID of the backup to delete.
        :return: Success bool.
        """
        access_token = self._getAccessToken()
        if not access_token:
            Logger.log("w", "Could not get access token.")
            return False

        delete_backup = requests.delete("{}/{}".format(self.DELETE_BACKUP_URL, backup_id), headers = {
            "Authorization": "Bearer {}".format(access_token)
        })
        if delete_backup.status_code not in (200, 201):
            Logger.log("w", "Could not delete backup: %s", delete_backup.text)
            return False
        return True

    def _requestBackupUpload(self, backup_metadata: Dict[str, any], backup_size: int) -> Optional[str]:
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
        if backup_upload_request.status_code not in (200, 201):
            Logger.log("w", "Could not request backup upload: %s", backup_upload_request.text)
            return None
        return backup_upload_request.json()["data"]["upload_url"]

    def _downloadBackupFile(self):
        pass

    def _passBackupToCura(self):
        pass

    def _getAccessToken(self) -> Optional[str]:
        return self._authorization_service.getAccessToken()
