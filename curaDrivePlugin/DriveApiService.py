# Copyright (c) 2017 Ultimaker B.V.
from time import sleep

from UM.Signal import Signal


class DriveApiService:

    # Emit signal when restoring backup started or finished.
    onRestoringStateChanged = Signal()

    # Emit signal when creating backup started or finished.
    onCreatingStateChanged = Signal()

    def __init__(self):
        pass

    def getBackups(self):
        # TODO: actually get data from server when that's ready.
        return [{
            "backup_id": "CxTAWARWV6EtlLk3953oQr0EgWZImWgTpwV3UlJkOs8e",
            "download_url": "",
            "generated_time": "2018-05-03T12:15:07.787Z",
            "data": {
                "machine_count": 10,
                "material_count": 12,
                "profile_count": 3,
                "plugin_count": 2,
                "cura_release": "3.1.1",
                "description": "Just a backup."
            }
        }, {
            "backup_id": "CxTAWARWV6EtlLk3953oQr0EgWZImWgTpwV3UlJkOs8e",
            "download_url": "",
            "generated_time": "2018-05-03T12:15:07.787Z",
            "data": {
                "machine_count": 10,
                "material_count": 12,
                "profile_count": 3,
                "plugin_count": 2,
                "cura_release": "3.1.1",
                "description": "Just a backup."
            }
        }, {
            "backup_id": "CxTAWARWV6EtlLk3953oQr0EgWZImWgTpwV3UlJkOs8e",
            "download_url": "",
            "generated_time": "2018-05-03T12:15:07.787Z",
            "data": {
                "machine_count": 10,
                "material_count": 12,
                "profile_count": 3,
                "plugin_count": 2,
                "cura_release": "3.1.1",
                "description": "Just a backup."
            }
        }, {
            "backup_id": "CxTAWARWV6EtlLk3953oQr0EgWZImWgTpwV3UlJkOs8e",
            "download_url": "",
            "generated_time": "2018-05-03T12:15:07.787Z",
            "data": {
                "machine_count": 10,
                "material_count": 12,
                "profile_count": 3,
                "plugin_count": 2,
                "cura_release": "3.1.1",
                "description": "Just a backup."
            }
        }]

    def createBackup(self):
        self.onCreatingStateChanged.emit(True)
        # TODO: actually create backup and upload it.
        self.onCreatingStateChanged.emit(False)

    def restoreBackup(self, backup: dict) -> None:
        self.onRestoringStateChanged.emit(True)
        download_url = backup.get("download_url")
        if not download_url or download_url == "":
            self.onRestoringStateChanged.emit(False)
        # TODO: download backup file and offer to Cura.

    def _downloadBackupFile(self):
        pass

    def _passBackupToCura(self):
        pass
