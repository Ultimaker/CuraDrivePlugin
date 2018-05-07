# Copyright (c) 2018 Ultimaker B.V.


class Settings:
    """
    Keeps the application settings.
    """
    OAUTH_SERVER_URL = "https://api-staging.ultimaker.com/auth/v1"
    CALLBACK_PORT = 1337
    CALLBACK_URL = "http://localhost:{}/callback".format(CALLBACK_PORT)
    CLIENT_ID = "um---------------ultimaker_cura_drive_plugin"

    I18N_CATALOG_ID = "cura_drive"
