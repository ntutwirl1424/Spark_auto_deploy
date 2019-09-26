import os
import time
import getpass

from src.frameworks.distribution_framework import DistributionFramework


class SparkFramework(DistributionFramework):
    def __init__(self):
        DistributionFramework.__init__(self)
        self.spark_folder_name = self.config.get_value("spark_folder_name")
        self.spark_tar_name = self.config.get_value("spark_tar_name")
        self.local_spark_tar_file_path = os.path.join(self.local_tar_files_folder_path, self.spark_tar_name)
        self.remote_spark_tar_file_path = os.path.join(self.framework_folder_root_path, self.spark_tar_name)

        self.spark_path = os.path.join(self.framework_folder_root_path, 
                                       self.spark_folder_name).format(username=getpass.getuser())
        print(self.spark_path)

    def start_spark_all(self):
        start_bash_file_path = os.path.join(self.spark_path, "sbin/start-all.sh")
        self.shell_utility.call_bash_script(start_bash_file_path)

    def stop_spark_all(self):
        stop_bash_file_path = os.path.join(self.spark_path, "sbin/stop-all.sh")
        self.shell_utility.call_bash_script(stop_bash_file_path)
        time.sleep(5)


if __name__ == "__main__":
    SparkFramework()
