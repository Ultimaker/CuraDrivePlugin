# Copyright (c) 2018 Ultimaker B.V.
from UM import i18nCatalog


class Settings:
    """
    Keeps the application settings.
    """

    OAUTH_SERVER_URL = "https://api-staging.ultimaker.com/auth/v1"
    CALLBACK_PORT = 32118  # CUR :)
    CALLBACK_URL = "http://localhost:{}/callback".format(CALLBACK_PORT)
    CLIENT_ID = "um---------------ultimaker_cura_drive_plugin"

    I18N_CATALOG_ID = "cura_drive"
    I18N_CATALOG = i18nCatalog(I18N_CATALOG_ID)

    # Translatable messages for the entire plugin.
    translatable_messages = {
        "extension_menu_entry": I18N_CATALOG.i18nc("@item:inmenu", "Cura Drive"),
        "login_failed_permission": I18N_CATALOG.i18nc("@info:login_status",
                                                      "Please allow Cura Drive to access your data."),
        "login_failed_unknown": I18N_CATALOG.i18nc("@info:login_status",
                                                   "An unknown error occurred, check the logs."),
        "backup_failed": I18N_CATALOG.i18nc("@info:backup_status", "Creating the backup failed.")
    }
