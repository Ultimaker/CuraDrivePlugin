# Copyright (c) 2018 Ultimaker B.V.
from UM.Qt.ListModel import ListModel

from PyQt5.QtCore import Qt


class BackupListModel(ListModel):
    """
    The BackupListModel transforms the backups data that came from the server so it can be served to the Qt UI.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addRoleName(Qt.UserRole + 1, "backup_id")
        self.addRoleName(Qt.UserRole + 2, "download_url")
        self.addRoleName(Qt.UserRole + 3, "generated_time")
        self.addRoleName(Qt.UserRole + 4, "data")

    def loadBackups(self, data: list) -> None:
        """
        Populate the model with server data.
        :param data:
        :return: The instance of the ListModel itself.
        """
        items = []
        for backup in data:
            items.append({
                "backup_id": backup["backup_id"],
                "download_url": backup["download_url"],
                "generated_time": "",  # TODO: not implemented on server yet: backup["generated_time"],
                "data": backup["metadata"]
            })
        self.setItems(items)
