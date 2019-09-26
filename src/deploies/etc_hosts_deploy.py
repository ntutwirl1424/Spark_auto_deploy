import os

from src.deploies.deploy import Deploy
from src.tools.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EtcHostsDeploy(Deploy):
    def __init__(self, ip_list, user_name, password):
        Deploy.__init__(self, ip_list, user_name, password)
        self.master_hostname = self.config.get_value("master_hostname")
        self.client_hostname = self.config.get_value("client_hostname")
        self.client_name_prefix = self.config.get_value("client_name_prefix")
        self.hosts_default_content = []
        self.hosts_client_info_content = []

    def run(self):
        self.init_remote_etc_hosts_hostname()
        self.change_localhost_hostname()

        self.change_remote_hostname()

        self.generate_hosts_default_file_content()
        self.generate_hosts_client_info_file_content()

        self.clear_localhost_hosts_file()

        self.clear_remote_hosts_file()

        self.write_localhost_hosts_file()

        self.write_remote_hosts_file()

    def init_remote_etc_hosts_hostname(self):
        i = 1
        for ip in self.ip_list:
            command = "echo \"127.0.0.1\t{}\" | sudo tee --append /etc/hosts".format(self.client_hostname[ip])
            self.shell_utility.run_remote_sudo_command(ip, command)
            i = i + 1

    def change_localhost_hostname(self):
        command = "echo '{}' > /etc/hostname".format(self.master_hostname)
        self.shell_utility.call_sudo_shell_command(command)
        command = "hostname -F /etc/hostname"
        self.shell_utility.call_sudo_shell_command(command)

    def change_remote_hostname(self):
        for ip in self.ip_list:
            command = "echo '{}' > /etc/hostname".format(self.client_hostname[ip])
            self.shell_utility.run_remote_sudo_command(ip, command)
            command = "hostname -F /etc/hostname"
            self.shell_utility.run_remote_sudo_command(ip, command)

    def clear_localhost_hosts_file(self):
        command = "echo \"{}\t{}\" > /etc/hosts".format(self.master_ip, self.master_hostname)
        self.shell_utility.call_sudo_shell_command(command)

    def clear_remote_hosts_file(self):
        for ip in self.ip_list:
            command = "echo '127.0.0.1\t{}' > /etc/hosts".format(self.client_hostname[ip])
            self.shell_utility.run_remote_sudo_command(ip, command)

    def write_localhost_hosts_file(self):
        for line in self.hosts_default_content:
            command = "echo \"{}\" | sudo tee --append /etc/hosts".format(line)
            self.shell_utility.call_sudo_shell_command(command)

        for line in self.hosts_client_info_content:
            command = "echo \"{}\" | sudo tee --append /etc/hosts".format(line)
            self.shell_utility.call_sudo_shell_command(command)

    def write_remote_hosts_file(self):
        for ip in self.ip_list:
            command = "echo '{}\t{}' | sudo tee --appen /etc/hosts".format(self.master_ip, self.master_hostname)
            self.shell_utility.run_remote_sudo_command(ip, command)
            for line in self.hosts_default_content:
                command = "echo \"{}\" | sudo tee --append /etc/hosts".format(line)
                self.shell_utility.run_remote_sudo_command(ip, command)

            for line in self.hosts_client_info_content:
                command = "echo \"{}\" | sudo tee --append /etc/hosts".format(line)
                self.shell_utility.run_remote_sudo_command(ip, command)

    def generate_hosts_default_file_content(self):
        self.hosts_default_content = [
            "127.0.0.1\tlocalhost",
            "::1\tip6-localhost ip6-loopback",
            "fe00::0\tip6-localnet",
            "ff00::0\tip6-mcastprefix",
            "ff02::1\tip6-allnodes",
            "ff02::2\tip6-allrouters"
        ]

    def generate_hosts_client_info_file_content(self):
        i = 1
        self.hosts_client_info_content = []
        print('-'*50)
        print(self.ip_list)
        print('-'*50)
        for ip in self.ip_list:
            self.hosts_client_info_content.append("{}\t{}".format(ip, "{}{}".format(self.client_name_prefix, i)))
            i = i + 1


if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("test_machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    deploy = EtcHostsDeploy(ip_list, user_name, password)
    deploy.run()
