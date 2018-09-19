# Copyright (c) 2017 Ultimaker B.V.
import base64
import hashlib
from datetime import datetime
from tempfile import NamedTemporaryFile
from typing import Optional, List, Dict

import requests

from UM.Logger import Logger
from UM.Message import Message
from UM.Signal import Signal

from cura.API import CuraAPI

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
    api = CuraAPI()

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
        if backup_list_request.status_code > 299:
            Logger.log("w", "Could not get backups list from remote: %s", backup_list_request.text)
            Message(Settings.translatable_messages["get_backups_error"], title = Settings.MESSAGE_TITLE,
                    lifetime = 10).show()
            return []
        return backup_list_request.json()["data"]

    def createBackup(self) -> None:
        """Create a backup and upload it to CuraDrive cloud storage."""
        self.onCreatingStateChanged.emit(is_creating=True)

        # Create the backup.
        backup_zip_file, backup_meta_data = self.api.backups.createBackup()
        if not backup_zip_file or not backup_meta_data:
            self.onCreatingStateChanged.emit(is_creating=False, error_message="Could not create backup.")
            return

        # Create an upload entry for the backup.
        timestamp = datetime.now().isoformat()
        backup_meta_data["description"] = "{}.backup.{}.cura.zip".format(timestamp, backup_meta_data["cura_release"])
        backup_upload_url = self._requestBackupUpload(backup_meta_data, len(backup_zip_file))
        if not backup_upload_url:
            self.onCreatingStateChanged.emit(is_creating=False, error_message="Could not upload backup.")
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
            self.onCreatingStateChanged.emit(is_creating=False, error_message=job.backup_upload_error_message)
        else:
            self.onCreatingStateChanged.emit(is_creating=False)

    def restoreBackup(self, backup: Dict[str, any]) -> None:
        """
        Restore a previously exported backup from cloud storage.
        :param backup: A dict containing an entry from the API list response.
        """
        self.onRestoringStateChanged.emit(is_restoring=True)
        download_url = backup.get("download_url")
        if not download_url:
            # If there is no download URL, we can't restore the backup.
            return self._emitRestoreError()

        download_package = requests.get(download_url, stream=True)
        if download_package.status_code != 200:
            # Something went wrong when attempting to download the backup.
            Logger.log("w", "Could not download backup from url %s: %s", download_url, download_package.text)
            return self._emitRestoreError()

        # We store the file in a temporary path fist to ensure integrity.
        temporary_backup_file = NamedTemporaryFile(delete=False)
        with open(temporary_backup_file.name, "wb") as write_backup:
            for chunk in download_package:
                write_backup.write(chunk)

        if not self._verifyMd5Hash(temporary_backup_file.name, backup.get("md5_hash")):
            # Don't restore the backup if the MD5 hashes do not match.
            # This can happen if the download was interrupted.
            Logger.log("w", "Remote and local MD5 hashes do not match, not restoring backup.")
            return self._emitRestoreError()

        # Tell Cura to place the backup back in the user data folder.
        with open(temporary_backup_file.name, "rb") as read_backup:
            self.api.backups.restoreBackup(read_backup.read(), backup.get("data"))
            self.onRestoringStateChanged.emit(is_restoring=False)

    def _emitRestoreError(self, error_message: str = Settings.translatable_messages["backup_restore_error_message"]):
        """Helper method for emitting a signal when restoring failed."""
        self.onRestoringStateChanged.emit(
            is_restoring=False,
            error_message=error_message
        )

    @staticmethod
    def _verifyMd5Hash(file_path: str, known_hash: str) -> bool:
        """
        Verify the MD5 hash of a file.
        :param file_path: Full path to the file.
        :param known_hash: The known MD5 hash of the file.
        :return: Success or not.
        """
        with open(file_path, "rb") as read_backup:
            local_md5_hash = base64.b64encode(hashlib.md5(read_backup.read()).digest(), altchars=b"_-").decode("utf-8")
            return known_hash == local_md5_hash

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
        if delete_backup.status_code > 299:
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
        if backup_upload_request.status_code > 299:
            Logger.log("w", "Could not request backup upload: %s", backup_upload_request.text)
            return None
        return backup_upload_request.json()["data"]["upload_url"]

    def _getAccessToken(self) -> Optional[str]:
        """
        Get the access token.
        :return: The access token as string.
        """
        return self._authorization_service.getAccessToken()
