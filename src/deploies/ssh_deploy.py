import os
import socket

from src.deploies.deploy import Deploy
from src.tools.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SSHDeploy(Deploy):
    def __init__(self, ip_list, user_name, password):
        Deploy.__init__(self, ip_list, user_name, password)

    def run(self):
        self.clear_local_ssh_folder_files()
        self.init_local_ssh_folder()
        self.re_generate_master_ssh_key()
        self.transform_pub_key()
        i = 1
        for ip in self.ip_list:
            try:
                host = socket.gethostbyaddr(ip)[0]
            except:
                host = None
            if host is not None:
                self.get_ssh_key_from_new_host(host)
            self.get_ssh_key_from_new_host(ip)
            self.init_remote_ssh_folder(ip)
            self.copy_pub_key_to_remote(ip)
            i = i + 1

    def clear_local_ssh_folder_files(self):
        command = "rm -f ~/.ssh/*"
        self.shell_utility.call_shell_command(command)

    def get_ssh_key_from_new_host(self, host):
        command = "ssh-keyscan -H {} >> ~/.ssh/known_hosts".format(host)
        self.shell_utility.call_shell_command(command)

    def re_generate_master_ssh_key(self):
        command = "ssh-keygen -f ~/.ssh/id_rsa -t rsa -N ''"
        self.shell_utility.call_shell_command(command)

    def transform_pub_key(self):
        command = "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
        self.shell_utility.call_shell_command(command)

    def init_local_ssh_folder(self):
        command = " mkdir -p ~/.ssh/"
        self.shell_utility.call_shell_command(command)

    def init_remote_ssh_folder(self, ip):
        command = " mkdir -p ~/.ssh/"
        self.shell_utility.run_remote_command_without_pub_key(ip, command)

    def copy_pub_key_to_remote(self, ip):
        pub_key_path = "~/.ssh/authorized_keys"
        remote_pub_key_folder = "~/.ssh/"
        self.shell_utility.copy_file_to_remote_target_without_pub_key(ip, pub_key_path, remote_pub_key_folder)


if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("test_machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    deploy = SSHDeploy(ip_list, user_name, password)
    deploy.run()
