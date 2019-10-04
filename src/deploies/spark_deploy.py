import os

from src.deploies.deploy import Deploy
from src.frameworks.spark_framework import SparkFramework
from src.tools.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SparkDeploy(Deploy):
    def __init__(self, ip_list, user_name, password):
        Deploy.__init__(self, ip_list, user_name, password)
        self.spark_framework = SparkFramework()

    def run(self):
        self.spark_framework.stop_spark_all()
        self.set_configuration_file()
        self.clear_log_files()
        self.tar_spark_folder()
        for ip in self.ip_list:
            self.clear_spark(ip)
            self.deploy_spark(ip)
        self.spark_framework.start_spark_all()

    def set_configuration_file(self):
        self.set_spark_default_config_file()
        self.set_spark_env_config_file()
        self.set_slaves_config_file()

    def set_slaves_config_file(self):
        slaves_file_path = os.path.join(self.spark_framework.spark_path, "conf/slaves")
        slave_content = ["{}@spark-{}".format(self.user_name[ip], i) for i, ip in enumerate(self.ip_list, 1)]
        self.write_to_config_file(slaves_file_path, slave_content)

    def set_spark_env_config_file(self):
        spark_env_file_path = os.path.join(self.spark_framework.spark_path,
                                           "conf/spark-env.sh")
        configs = ["export SPARK_MASTER_HOST={}".format(self.master_hostname),
                   "#export SPARK_MASTER_MEMORY={}g".format(self.config.get_value("SPARK_MASTER_MEMORY")),
                   "#export SPARK_WORKER_MEMORY={}g".format(self.config.get_value("SPARK_WORKER_MEMORY")),
                   "#export SPARK_EXECUTOR_MEMORY={}g".format(self.config.get_value("SPARK_EXECUTOR_MEMORY")),
                   "#export SPARK_WORKER_CORES={}".format(self.config.get_value("SPARK_WORKER_CORES")),
                   "export HADOOP_CONF_DIR={}/hadoop/etc/hadoop".format(self.config.get_value("framework_folder_root_path")),
                   "export YARN_CONF_DIR={}/hadoop/etc/hadoop".format(self.config.get_value("framework_folder_root_path")),
                   "export SPARK_HOME={}".format(self.spark_framework.spark_path),
                   "export JAVA_HOME={}".format(self.config.get_value("JAVA_HOME")),
                   "export PYSPARK_PYTHON={}".format(self.config.get_value("PYTHON_VERSION")),
                   "export PYSPARK_DRIVER_PYTHON={}".format(self.config.get_value("PYTHON_VERSION")),
                   "export PYTHONHASHSEED={}".format(self.config.get_value("PYTHONHASHSEED"))]
        self.write_to_config_file(spark_env_file_path, configs)

    def set_spark_default_config_file(self):
        spark_default_file_path = os.path.join(self.spark_framework.spark_path, "conf/spark-defaults.conf")
        configs = ["spark.master                     spark://{}:7077".format(self.master_hostname),
                   # "spark.eventLog.enabled           true",
                   # "spark.eventLog.dir               hdfs://{}:9000/user/spark/eventLog".format(self.master_hostname),
                   "# spark.serializer                 org.apache.spark.serializer.KryoSerializer",
                   "# spark.driver.memory              {}g".format(self.config.get_value("SPARK_DRIVER_MEMORY")),
                   "spark.driver.memory              {}g".format(self.config.get_value("SPARK_DRIVER_MEMORY")),
                   "spark.executor.memory            {}g".format(self.config.get_value("SPARK_EXECUTOR_MEMORY"))]
        self.write_to_config_file(spark_default_file_path, configs)

    def tar_spark_folder(self):
        self.shell_utility.package_file(self.spark_framework.local_spark_tar_file_path,
                                        self.spark_framework.framework_folder_root_path.format(username=self.current_user_name),
                                        self.spark_framework.spark_folder_name)

    def clear_log_files(self):
        remove_log_command = "rm -rf {}".format(os.path.join(self.spark_framework.spark_path, "logs/*"))
        self.shell_utility.call_shell_command(remove_log_command)

    def clear_spark(self, ip):
        remove_remote_spark_folder_command = "rm -rf {}".format(self.spark_framework.spark_path)
        remove_remote_spark_tar_command = "rm -f {}".format(self.spark_framework.remote_spark_tar_file_path.format(username=self.user_name[ip]))
        self.shell_utility.run_remote_command(ip, remove_remote_spark_folder_command)
        self.shell_utility.run_remote_command(ip, remove_remote_spark_tar_command)

    def deploy_spark(self, ip):
        self.shell_utility.copy_file_to_remote_target(ip, self.spark_framework.local_spark_tar_file_path
                                                      , self.spark_framework.framework_folder_root_path.format(username=self.user_name[ip]))
        print('-'*50)
        print(self.spark_framework.framework_folder_root_path.format(username=self.user_name[ip]))
        print('-'*50)
        self.shell_utility.unzip_remote_file(ip, self.spark_framework.remote_spark_tar_file_path.format(username=self.user_name[ip]),
                                             self.spark_framework.framework_folder_root_path.format(username=self.user_name[ip]))


if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("test_machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    deploy = SparkDeploy(ip_list, user_name, password)
    deploy.run()
