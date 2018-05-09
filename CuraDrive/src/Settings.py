# Copyright (c) 2018 Ultimaker B.V.
from UM import i18nCatalog

from ..lib.CuraPluginOAuth2Module.OAuth2Client.models import OAuth2Settings


class Settings:
    """
    Keeps the application settings.
    """

    CALLBACK_PORT = 32118

    OAUTH_SETTINGS = OAuth2Settings(
        OAUTH_SERVER_URL="https://api-staging.ultimaker.com/auth/v1",
        CALLBACK_PORT = CALLBACK_PORT,  # CUR :)
        CALLBACK_URL = "http://localhost:{}/callback".format(CALLBACK_PORT),
        CLIENT_ID = "um---------------ultimaker_cura_drive_plugin",
        CLIENT_SCOPES = "user.read drive.backups.read drive.backups.write"
    )

    DRIVE_API_URL = "https://api-staging.ultimaker.com/cura-drive/v1"

    I18N_CATALOG_ID = "cura_drive"
    I18N_CATALOG = i18nCatalog(I18N_CATALOG_ID)
    
    MESSAGE_TITLE = "Cura Drive"

    # Translatable messages for the entire plugin.
    translatable_messages = {
        "extension_menu_entry": I18N_CATALOG.i18nc("@item:inmenu", "Cura Drive"),
        "backup_failed": I18N_CATALOG.i18nc("@info:backup_status", "There was an error while creating your backup."),
        "uploading_backup": I18N_CATALOG.i18nc("@info:backup_status", "Uploading your backup..."),
        "uploading_backup_success": I18N_CATALOG.i18nc("@info:backup_status", "Your backup has finished uploading."),
        "uploading_backup_error": I18N_CATALOG.i18nc("@info:backup_status",
                                                     "There was an error while uploading your backup."),
        "get_backups_error": I18N_CATALOG.i18nc("@info:backup_status", "There was an error listing your backups.")
    }