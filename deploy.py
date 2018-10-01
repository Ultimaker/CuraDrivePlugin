# Copyright (c) 2018 Ultimaker B.V.
import os
import logging
import time
from dotenv import load_dotenv

from CuraPackageDeployer.Config import Config
from CuraPackageDeployer.CuraPackageDeployer import CuraPackageDeployer


# Load the environment
load_dotenv()
should_build_remote = os.getenv("BUILD_REMOTE", "False") == "True"
should_request_review = os.getenv("REQUEST_REVIEW", "False") == "True"


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
    if should_build_remote:
        deployer.deploy()
        time.sleep(3)  # Give the API some time to build the package.
        deployer.checkBuildStatus()
    if should_request_review:
        deployer.requestReview()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
