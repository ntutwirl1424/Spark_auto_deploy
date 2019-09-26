import os

from src.deploies.deploy import Deploy
from src.tools.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class InitDeploy(Deploy):
    def __init__(self, ip_list, user_name, password):
        Deploy.__init__(self, ip_list, user_name, password)

    def run(self):
        self.clear_remote_folder_and_tar_file()

    def clear_remote_folder_and_tar_file(self):
        for ip in self.ip_list:
            self.shell_utility.run_remote_command(ip, "rm -rf tes/")
            self.shell_utility.run_remote_command(ip, "rm -rf tes2/")
            self.shell_utility.run_remote_command(ip, "rm -rf tes.tar.gz")
            self.shell_utility.run_remote_command(ip, "rm -rf tes2.tar.gz")


if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("test_machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    deploy = InitDeploy(ip_list, user_name, password)
    deploy.run()
