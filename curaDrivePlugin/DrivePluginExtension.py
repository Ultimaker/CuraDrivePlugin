# Copyright (c) 2017 Ultimaker B.V.
import os
from typing import Optional

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal

from UM.Application import Application
from UM.Extension import Extension
from UM.Message import Message
from UM.PluginRegistry import PluginRegistry

from .Settings import Settings
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

    # Signal emitted when creating has started. Needed to prevent parallel creation of backups.
    creatingStateChanged = pyqtSignal()

    def __init__(self):
        super(DrivePluginExtension, self).__init__()

        # Local data caching for the UI.
        self._auth_error_message = ""
        self._drive_window = None  # type: Optional[QObject]
        self._backups_list_model = BackupListModel()
        self._is_restoring_backup = False
        self._is_creating_backup = False

        # Initialize services.
        self._authorization_service = AuthorizationService()  # type: AuthorizationService
        self._drive_api_service = DriveApiService(self._authorization_service)  # type: DriveApiService

        # Attach signals.
        self._authorization_service.onAuthStateChanged.connect(self._onLoginStateChanged)
        self._authorization_service.onAuthenticationError.connect(self._onLoginStateChanged)
        self._drive_api_service.onRestoringStateChanged.connect(self._onRestoringStateChanged)
        self._drive_api_service.onCreatingStateChanged.connect(self._onCreatingStateChanged)

        # Register menu items.
        self.addMenuItem(Settings.translatable_messages["extension_menu_entry"], self.showDriveWindow)

    def showDriveWindow(self) -> None:
        """Show the Drive UI popup window."""
        if not self._drive_window:
            self._drive_window = self.createDriveWindow()
        self._drive_window.show()
        self.refreshBackups()

    def createDriveWindow(self) -> Optional["QObject"]:
        """
        Create an instance of the Drive UI popup window.
        :return: The popup window object.
        """
        path = os.path.join(PluginRegistry.getInstance().getPluginPath(self.getPluginId()),
                            "curaDrivePlugin/qml/main.qml")
        return Application.getInstance().createQmlComponent(path, {"CuraDrive": self})

    def _onLoginStateChanged(self, logged_in: bool = False, error_message: str = None):
        """Callback handler for changes in the login state."""
        if error_message:
            Message(error_message, lifetime=30).show()
        if logged_in:
            self.refreshBackups()
        self.loginStateChanged.emit()

    def _onRestoringStateChanged(self, is_restoring: bool = False, error_message: str = None):
        """Callback handler for changes in the restoring state."""
        if error_message:
            Message(error_message, lifetime=10).show()
        self._is_restoring_backup = is_restoring
        self.restoringStateChanged.emit()

    def _onCreatingStateChanged(self, is_creating: bool = False, error_message: str = None):
        """Callback handler for changes in the creation state."""
        if error_message:
            Message(error_message, lifetime=10).show()
        self._is_creating_backup = is_creating
        if not is_creating:
            # We've finished creating a new backup, to the list has to be updated.
            self.refreshBackups()

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

    @pyqtSlot(name = "refreshBackups")
    def refreshBackups(self) -> None:
        """
        Forcefully refresh the backups list.
        :return:
        """
        self._backups_list_model.loadBackups(self._drive_api_service.getBackups())
        self.backupsChanged.emit()

    @pyqtProperty(bool, notify = restoringStateChanged)
    def isRestoringBackup(self) -> bool:
        """
        Get the current restoring state.
        :return: Boolean if we are restoring or not.
        """
        return self._is_restoring_backup

    @pyqtProperty(bool, notify = creatingStateChanged)
    def isCreatingBackup(self) -> bool:
        """
        Get the current creating state.
        :return: Boolean if we are creating or not.
        """
        return self._is_creating_backup

    @pyqtSlot(str, name = "restoreBackup")
    def restoreBackup(self, backup_id: str) -> None:
        """
        Download and restore a backup by ID.
        :param backup_id: The ID of the backup.
        """
        index = self._backups_list_model.find("backup_id", backup_id)
        backup = self._backups_list_model.getItem(index)
        self._drive_api_service.restoreBackup(backup)

    @pyqtSlot(name = "createBackup")
    def createBackup(self) -> None:
        """
        Create a new backup.
        """
        self._drive_api_service.createBackup()

    @pyqtSlot(str, name = "deleteBackup")
    def deleteBackup(self, backup_id: str) -> None:
        """
        Delete a backup by ID.
        :param backup_id: The ID of the backup.
        """
        self._drive_api_service.deleteBackup(backup_id)
        self.refreshBackups()
