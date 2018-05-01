# Copyright (c) 2017 Ultimaker B.V.
from UM.Application import Application
from UM.Extension import Extension


class DrivePluginExtension(Extension):
    """
    The DivePluginExtension provides functionality to backup and restore your Cura configuration to Ultimaker's cloud.
    """
    def __init__(self):
        super().__init__()
        self._authorization_service = None
        self._drive_api_service = None
        Application.getInstance().applicationRunning.connect(self._run)

    def _run(self) -> None:
        """
        Initialize the handlers.
        :return:
        """
        pass
