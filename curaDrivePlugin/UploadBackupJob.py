# Copyright (c) 2018 Ultimaker B.V.
import requests

from UM.Job import Job
from UM.Logger import Logger
from UM.Message import Message
from curaDrivePlugin.Settings import Settings


class UploadBackupJob(Job):
    """
    This job is responsible for uploading the backup file to cloud storage.
    As it can take longer than some other tasks, we schedule this using a Cura Job.
    """

    def __init__(self, signed_upload_url: str, backup_zip: bytes):
        super().__init__()
        self._signed_upload_url = signed_upload_url
        self._backup_zip = backup_zip
        self._upload_success = False
        self.backup_upload_error_message = ""

    def run(self):
        Message(Settings.translatable_messages["uploading_backup"]).show()

        backup_upload = requests.put(self._signed_upload_url, data = self._backup_zip)
        if backup_upload.status_code != 200:
            self.backup_upload_error_message = backup_upload.text
            Logger.log("w", "Could not upload backup file: %s", backup_upload.text)
            Message(Settings.translatable_messages["uploading_backup_error"]).show()
        else:
            self._upload_success = True
            Message(Settings.translatable_messages["uploading_backup_success"]).show()

        self.finished.emit(self)
