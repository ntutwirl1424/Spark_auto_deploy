import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
paths = [ROOT_DIR, SRC_DIR]
for p in paths:
    sys.path.append(p)

from src.deploies.framework_deploy import FrameworkDeploy
from src.tools.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    FrameworkDeploy(ip_list, user_name, password).deploy()
