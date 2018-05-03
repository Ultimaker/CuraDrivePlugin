# Copyright (c) 2017 Ultimaker B.V.


class DriveApiService:

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
        }]

    def uploadBackup(self, backup_zip, metadata):
        pass

    def downloadBackup(self, backup):
        pass
