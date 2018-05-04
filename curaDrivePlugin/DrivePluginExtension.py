# Copyright (c) 2017 Ultimaker B.V.
import os
from typing import Optional

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal

from UM.Application import Application
from UM.Extension import Extension
from UM.Message import Message
from UM.PluginRegistry import PluginRegistry
from UM.i18n import i18nCatalog

from .authorization.AuthorizationService import AuthorizationService
from .DriveApiService import DriveApiService
from .models.BackupListModel import BackupListModel


class DrivePluginExtension(QObject, Extension):
    """
    The DivePluginExtension provides functionality to backup and restore your Cura configuration to Ultimaker's cloud.
    """

    # Signal emitted when user logged in or out.
    loginStateChanged = pyqtSignal()

    # Signal emitted when the list of backups changed.
    backupsChanged = pyqtSignal()

    # Signal emitted when restoring has started. Needed to prevent parallel restoring.
    restoringStateChanged = pyqtSignal()

    def __init__(self):
        super(DrivePluginExtension, self).__init__()

        # Local data caching for the UI.
        self._auth_error_message = ""
        self._drive_window = None  # type: Optional[QObject]
        self._backups_list_model = BackupListModel()
        self._is_restoring_backup = False

        # Initialize services.
        self._authorization_service = AuthorizationService()  # type: AuthorizationService
        self._drive_api_service = DriveApiService()  # type: DriveApiService

        # Attach signals.
        self._authorization_service.onAuthStateChanged.connect(self._onLoginStateChanged)
        self._authorization_service.onAuthenticationError.connect(self._onLoginStateChanged)

        # Register menu items.
        catalog = i18nCatalog("cura")
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Cura Drive"), self.showDriveWindow)

        # Initialize data after Cura has started.
        Application.getInstance().applicationRunning.connect(self._run)

    def _run(self) -> None:
        """Populate initial values."""
        self._backups = self._drive_api_service.getBackups()
        self.showDriveWindow()

        # TODO: move these
        self._backups_list_model.loadBackups(self._drive_api_service.getBackups())
        self.backupsChanged.emit()

    def showDriveWindow(self) -> None:
        """Show the Drive UI popup window."""
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

    def _onLoginStateChanged(self, error_message: str = None):
        """Callback handler for changes in the login state."""
        if error_message:
            Message(error_message, lifetime=30, title="Cura Drive login").show()
        self.loginStateChanged.emit()

    @pyqtProperty(bool, notify = loginStateChanged)
    def isLoggedIn(self) -> bool:
        """Check if a user is logged in or not."""
        return bool(self._authorization_service.getUserProfile())

    @pyqtSlot(name = "login")
    def login(self) -> None:
        """Start the OAuth2 authorization flow to log in."""
        self._authorization_service.startAuthorizationFlow()

    @pyqtSlot(name = "logout")
    def logout(self) -> None:
        """Delete all auth data."""
        self._authorization_service.deleteAuthData()

    @pyqtProperty("QVariantMap", notify = loginStateChanged)
    def profile(self) -> dict:
        """
        Get the profile of the authenticated user.
        :return: A dict containing the profile information.
        """
        return self._authorization_service.getUserProfile()

    @pyqtProperty(str, notify = loginStateChanged)
    def authError(self) -> str:
        """
        Get the error message from the authorization flow.
        :return: The error message as string.
        """
        return self._auth_error_message

    @pyqtProperty(QObject, notify = backupsChanged)
    def backups(self) -> BackupListModel:
        """
        Get a list of the backups.
        :return: The backups as Qt List Model.
        """
        return self._backups_list_model

    @pyqtProperty(bool, notify = restoringStateChanged)
    def isRestoringBackup(self) -> bool:
        """
        Get the current restoring state.
        :return: Boolean if we are restoring or not.
        """
        return self._is_restoring_backup

    @pyqtSlot(str, name = "restoreBackup")
    def restoreBackup(self, backup_id: str) -> None:
        """
        Download and restore a backup by ID.
        :param backup_id:
        """
        self._is_restoring_backup = True
        self.restoringStateChanged.emit()
        index = self._backups_list_model.find("backup_id", backup_id)
        backup = self._backups_list_model.getItem(index)
        self._drive_api_service.downloadBackup(backup)
