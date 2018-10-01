# Copyright (c) 2018 Ultimaker B.V.
import os
import logging
import time
from dotenv import load_dotenv

from CuraPackageDeployer.Config import Config
from CuraPackageDeployer.CuraPackageDeployer import CuraPackageDeployer


load_dotenv()


class CuraDriveConfig(Config):
    package_id = "CuraDrive"
    package_sources_dir = "./CuraDrive"
    tags = ["backups", "cloud", "restore", "configuration", "settings", "sync"]
    website = "https://ultimaker.com"
    release_notes = "Switched to the new Ultimaker Account functionality baked into Cura."
    access_token = os.getenv("ACCESS_TOKEN", None)


def main() -> None:
    config = CuraDriveConfig()
    deployer = CuraPackageDeployer(config)
    deployer.loadPluginSources()
    deployer.buildPlugin()
    
    if os.getenv("BUILD_REMOTE") == "True":
        deployer.deploy()
        time.sleep(3)  # Give the API some time to build the package.
        deployer.checkBuildStatus()
    
    if os.getenv("DEPLOY") == "True":
        deployer.requestReview()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
