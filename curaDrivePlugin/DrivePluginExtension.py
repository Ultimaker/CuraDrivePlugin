# Copyright (c) 2017 Ultimaker B.V.
import os
from typing import Optional

from PyQt5.QtCore import QObject, pyqtSlot

from UM.Application import Application
from UM.Extension import Extension
from UM.PluginRegistry import PluginRegistry
from UM.i18n import i18nCatalog

from curaDrivePlugin.AuthorizationService import AuthorizationService
from curaDrivePlugin.DriveApiService import DriveApiService


class DrivePluginExtension(Extension):
    """
    The DivePluginExtension provides functionality to backup and restore your Cura configuration to Ultimaker's cloud.
    """

    def __init__(self):
        super().__init__()

        self._user_profile = None
        self._backups = []

        # Placeholder for UI components.
        self._drive_window = None

        # Initialize services.
        self._authorization_service = AuthorizationService()  # type: AuthorizationService
        self._drive_api_service = DriveApiService()  # type: DriveApiService

        # Register menu items.
        catalog = i18nCatalog("cura")
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Cura Drive"), self.showDriveWindow)

        Application.getInstance().applicationRunning.connect(self._run)

    def _run(self) -> None:
        """
        Populate initial values.
        :return:
        """
        self._user_profile = self._authorization_service.getUserProfile()
        self._backups = self._drive_api_service.getBackups()

    def showDriveWindow(self) -> None:
        """
        Show the Drive UI popup window.
        :return:
        """
        if not self._drive_window:
            self._drive_window = self.createDriveWindow()
        self._drive_window.show()

    def createDriveWindow(self) -> Optional["QObject"]:
        """
        Create an instance of the Drive UI popup window.
        :return:
        """
        path = os.path.join(PluginRegistry.getInstance().getPluginPath(self.getPluginId()),
                            "curaDrivePlugin/qml/main.qml")
        return Application.getInstance().createQmlComponent(path, {"CuraDrive": self})

    @pyqtSlot()
    def login(self) -> None:
        """
        Login flow.
        :return:
        """
        self._authorization_service.startAuthorizationFlow()
