import getpass
import os

from src.tools.config import Config
from src.tools.shell_utility import ShellUtility

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Deploy(object):
    def __init__(self, ip_list, user_name, password):
        self.config = Config()
        self.ip_list = ip_list
        self.user_name = user_name
        self.password = password
        self.current_user_name = getpass.getuser()
        self.master_ip = self.config.get_value("spark_master_ip")
        self.master_hostname = self.config.get_value('master_hostname')
        self.local_password = self.config.get_value('local_password')
        self.shell_utility = ShellUtility(user_name, password, self.local_password)

    def run(self):
        pass

    def write_to_config_file(self, file_path, contents):
        with open(file_path, "w+", encoding="utf-8") as config_file:
            for content in contents:
                config_file.write(content)
                config_file.write("\n")


if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("test_machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    deploy = Deploy(ip_list, user_name, password)
    deploy.run()
