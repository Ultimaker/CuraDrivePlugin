# Copyright (c) 2017 Ultimaker B.V.
from UM.Application import Application
from UM.Extension import Extension
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

        # Initialize services.
        self._authorization_service = AuthorizationService()  # type: AuthorizationService
        self._drive_api_service = DriveApiService()  # type: DriveApiService

        Application.getInstance().applicationRunning.connect(self._run)

    def _run(self) -> None:
        """
        Populate initial values.
        :return:
        """
        self._user_profile = self._authorization_service.getUserProfile()
        self._backups = self._drive_api_service.getBackups()

    def login(self):
        """
        Login flow.
        :return:
        """
        self._authorization_service.startAuthorizationFlow()
