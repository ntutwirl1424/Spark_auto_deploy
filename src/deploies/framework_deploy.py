from src.deploies.etc_hosts_deploy import EtcHostsDeploy
from src.deploies.hadoop_deploy import HadoopDeploy
from src.deploies.spark_deploy import SparkDeploy
from src.deploies.ssh_deploy import SSHDeploy
from src.tools.config import Config


class FrameworkDeploy(object):
    def __init__(self, ip_list, machine_user_account, machine_user_password):
        self.ip_list = ip_list
        self.machine_user_account = machine_user_account
        self.machine_user_password = machine_user_password
        self.config = Config()

    def deploy(self):
        ip_for_ssh_list = list(self.ip_list)
        ip_for_ssh_list.append(self.config.get_value("spark_master_ip"))
        print(ip_for_ssh_list)
        deploies = [
            SSHDeploy(ip_for_ssh_list, self.machine_user_account, self.machine_user_password),
            EtcHostsDeploy(self.ip_list, self.machine_user_account, self.machine_user_password),
            HadoopDeploy(self.ip_list, self.machine_user_account, self.machine_user_password),
            SparkDeploy(self.ip_list, self.machine_user_account, self.machine_user_password)
        ]
        for deploy in deploies:
            deploy.run()


if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("test_machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    FrameworkDeploy(ip_list, user_name, password).deploy()
