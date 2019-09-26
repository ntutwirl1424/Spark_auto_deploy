import os
import getpass

from src.tools.config import Config
from src.tools.shell_utility import ShellUtility

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DistributionFramework(object):
    def __init__(self):
        self.config = Config()
        self.framework_folder_root_path = self.config.get_value("framework_folder_root_path")
        self.local_tar_files_folder_path = self.config.get_value("local_tar_files_folder_path")
        self.shell_utility = ShellUtility()
        self.init_framework_environment()
        self.check_framework_environment()

    def init_framework_environment(self):
        self.shell_utility.call_shell_command("mkdir -p {}".format(self.local_tar_files_folder_path))

    def check_framework_environment(self):
        if not os.path.exists(self.framework_folder_root_path.format(username=getpass.getuser())):
            raise FileNotFoundError("{} not found.".format(self.framework_folder_root_path))
        if not os.path.exists(self.local_tar_files_folder_path):
            raise FileNotFoundError("{} not found.".format(self.local_tar_files_folder_path))
