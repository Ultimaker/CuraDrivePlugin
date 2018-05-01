# Copyright (c) 2017 Ultimaker B.V.
import os
from typing import Optional

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal

from UM.Application import Application
from UM.Extension import Extension
from UM.PluginRegistry import PluginRegistry
from UM.i18n import i18nCatalog

from curaDrivePlugin.Authorization.AuthorizationService import AuthorizationService
from curaDrivePlugin.DriveApiService import DriveApiService


class DrivePluginExtension(QObject, Extension):
    """
    The DivePluginExtension provides functionality to backup and restore your Cura configuration to Ultimaker's cloud.
    """

    # Signal emitted when user logged in or out.
    loginStateChanged = pyqtSignal()

    def __init__(self):
        super(DrivePluginExtension, self).__init__()

        self._user_profile = None
        self._backups = []

        # Placeholder for UI components.
        self._drive_window = None

        # Initialize services.
        self._authorization_service = AuthorizationService()  # type: AuthorizationService
        self._drive_api_service = DriveApiService()  # type: DriveApiService

        # Attach signals.
        self._authorization_service.onAuthenticated.connect(self._onLoginStateChanged)

        # Register menu items.
        catalog = i18nCatalog("cura")
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Cura Drive"), self.showDriveWindow)

        Application.getInstance().applicationRunning.connect(self._run)

    def _run(self) -> None:
        """
        Populate initial values.
        """
        self._user_profile = self._authorization_service.getUserProfile()
        self._backups = self._drive_api_service.getBackups()
        self.showDriveWindow()

    def showDriveWindow(self) -> None:
        """
        Show the Drive UI popup window.
        """
        if not self._drive_window:
            self._drive_window = self.createDriveWindow()
        self._drive_window.show()

    def createDriveWindow(self) -> Optional["QObject"]:
        """
        Create an instance of the Drive UI popup window.
        :return: The popup window object.
        """
        path = os.path.join(PluginRegistry.getInstance().getPluginPath(self.getPluginId()),
                            "curaDrivePlugin/qml/main.qml")
        return Application.getInstance().createQmlComponent(path, {"CuraDrive": self})

    def _onLoginStateChanged(self, access_token):
        self.loginStateChanged.emit()

    @pyqtSlot()
    def login(self) -> None:
        """
        Start the OAuth2 authorization flow to log in.
        """
        self._authorization_service.startAuthorizationFlow()

    @pyqtProperty("QVariantMap", notify = loginStateChanged)
    def profile(self) -> dict:
        """
        Get the profile of the authenticated user.
        :return: A dict containing the profile information.
        """
        return self._authorization_service.getUserProfile()

    @pyqtProperty("QVariantMap", notify=loginStateChanged)
    def token(self) -> dict:
        """
        Get the access token and relevant data.
        :return: A dict containing the access token data.
        """
        return self._authorization_service.getAccessToken()
