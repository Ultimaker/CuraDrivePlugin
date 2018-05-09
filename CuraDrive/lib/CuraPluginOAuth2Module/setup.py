# Copyright (c) 2018 Ultimaker B.V.
# CuraPluginOAuth2Module is released under the terms of the LGPLv3 or higher.

from distutils.core import setup

setup(
    name="CuraPluginOAuth2Module",
    version="1.0.0",
    description="A Python module that provides OAuth2 client logic for Cura plugins.",
    author="Ultimaker",
    author_email="c.terbeke@ultimaker.com",
    url="https://github.com/Ultimaker/CuraPluginOAuth2Module",
    packages=["OAuth2Client"],
    requires=["requests", "jwt"]
)
