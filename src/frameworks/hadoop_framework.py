import os
import getpass

from src.frameworks.distribution_framework import DistributionFramework

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HadoopFramework(DistributionFramework):
    def __init__(self):
        DistributionFramework.__init__(self)
        self.hadoop_folder_name = self.config.get_value("hadoop_folder_name")
        self.hadoop_tar_name = self.config.get_value("hadoop_tar_name")

        self.local_hadoop_tar_file_path = os.path.join(self.local_tar_files_folder_path, self.hadoop_tar_name)
        self.remote_hadoop_tar_file_path = os.path.join(self.framework_folder_root_path, self.hadoop_tar_name)

        self.hadoop_path = os.path.join(self.framework_folder_root_path, 
                                        self.hadoop_folder_name).format(username=getpass.getuser())
        self.hadoop_hdfs_path = os.path.join(self.hadoop_path, "bin/hdfs")

    def start_hadoop_all(self):
        start_bash_file_path = os.path.join(self.hadoop_path, "sbin/start-all.sh")
        self.shell_utility.call_bash_script(start_bash_file_path)

    def stop_hadoop_all(self):
        start_bash_file_path = os.path.join(self.hadoop_path, "sbin/stop-all.sh")
        self.shell_utility.call_bash_script(start_bash_file_path)

    def run_hdfs_command(self, command):
        hdfs_command = "{} {}".format(self.hadoop_hdfs_path, command)
        self.shell_utility.call_shell_command(hdfs_command)

    def copy_file_from_local_to_hdfs(self, local_file_path, hdfs_file_path):
        command = "dfs -copyFromLocal {} {}".format(local_file_path, hdfs_file_path)
        self.run_hdfs_command(command)


if __name__ == "__main__":
    HadoopFramework()
