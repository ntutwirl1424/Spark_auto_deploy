import os

from src.deploies.deploy import Deploy
from src.frameworks.hadoop_framework import HadoopFramework
from src.tools.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HadoopDeploy(Deploy):
    def __init__(self, ip_list, user_name, password):
        Deploy.__init__(self, ip_list, user_name, password)
        self.hadoop_framework = HadoopFramework()

    def run(self):
        self.hadoop_framework.stop_hadoop_all()
        self.set_configuration_file()
        self.clear_log_files()
        self.tar_hadoop_folder()
        for ip in self.ip_list:
            self.clear_hadoop(ip)
            self.deploy_hadoop(ip)
        # time.sleep(5)
        self.format_hdfs()
        self.hadoop_framework.start_hadoop_all()
        self.init_hdfs()

    def set_configuration_file(self):
        self.set_core_site_config_file()
        self.set_hdfs_site_config_file()
        self.set_mapred_site_config_file()
        self.set_yarn_site_config_file()
        self.set_slaves_config_file()

    def set_core_site_config_file(self):
        core_site_file_path = os.path.join(self.hadoop_framework.hadoop_path, "etc/hadoop/core-site.xml")
        configs = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<?xml-stylesheet type="text / xsl" href="configuration.xsl"?>',
                   "<configuration>",
                   "  <property>",
                   "    <name>fs.defaultFS</name>",
                   "    <value>hdfs://{}:9000</value>".format(self.master_hostname),
                   "  </property>",
                   "  <property>",
                   "    <name>hadoop.tmp.dir</name>",
                   "    <value>file://{}/tmp</value>".format(self.hadoop_framework.hadoop_path),
                   "    <description>Abase for other temporary directories.</description>",
                   "  </property>",
                   "</configuration>"]
        self.write_to_config_file(core_site_file_path, configs)

    def set_hdfs_site_config_file(self):
        hdfs_site_file_path = os.path.join(self.hadoop_framework.hadoop_path, "etc/hadoop/hdfs-site.xml")
        configs = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>',
                   "<configuration>",
                   "  <property>",
                   "    <name>dfs.namenode.secondary.http-address</name>",
                   "    <value>{}:50090</value>".format(self.master_hostname),
                   "  </property>",
                   "  <property>",
                   "    <name>dfs.namenode.name.dir</name>",
                   "    <value>file://{}/tmp/dfs/name</value>".format(self.hadoop_framework.hadoop_path),
                   "  </property>",
                   "  <property>",
                   "    <name>dfs.datanode.data.dir</name>",
                   "    <value>file://{}/tmp/dfs/data</value>".format(self.hadoop_framework.hadoop_path),
                   "  </property>",
                   "  <property>",
                   "    <name>dfs.replication</name>",
                   "    <value>3</value>",
                   "  </property>",
                   "</configuration>"]
        self.write_to_config_file(hdfs_site_file_path, configs)

    def set_mapred_site_config_file(self):
        mapred_site_file_path = os.path.join(self.hadoop_framework.hadoop_path,
                                             "etc/hadoop/mapred-site.xml")
        configs = ['<?xml version="1.0"?>',
                   '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>',
                   "<configuration>",
                   "  <property>",
                   "    <name>mapreduce.frameworks.name</name>",
                   "    <value>yarn</value>",
                   "  </property>",
                   "</configuration>"]
        self.write_to_config_file(mapred_site_file_path, configs)

    def set_yarn_site_config_file(self):
        yarn_site_file_path = os.path.join(self.hadoop_framework.hadoop_path, "etc/hadoop/yarn-site.xml")
        configs = ['<?xml version="1.0"?>',
                   "<configuration>",
                   "  <property>",
                   "    <name>yarn.resourcemanager.hostname</name>",
                   "    <value>{}</value>".format(self.master_hostname),
                   "  </property>",
                   "  <property>",
                   "    <name>yarn.nodemanager.aux-services</name>",
                   "    <value>mapreduce_shuffle</value>",
                   "  </property>",
                   "</configuration>"]
        self.write_to_config_file(yarn_site_file_path, configs)

    def set_slaves_config_file(self):
        slaves_file_path = os.path.join(self.hadoop_framework.hadoop_path, "etc/hadoop/slaves")

        slave_content = ["{}@spark-{}".format(self.user_name[ip], i) for i, ip in enumerate(self.ip_list, 1)]
        self.write_to_config_file(slaves_file_path, slave_content)

    def clear_log_files(self):
        remove_log_command = "rm -rf {}".format(os.path.join(self.hadoop_framework.hadoop_path, "logs/*"))
        self.shell_utility.call_shell_command(remove_log_command)
        remove_tmp_command = "rm -rf {}".format(os.path.join(self.hadoop_framework.hadoop_path, "tmp/*"))
        self.shell_utility.call_shell_command(remove_tmp_command)

    def tar_hadoop_folder(self):
        self.shell_utility.package_file(self.hadoop_framework.local_hadoop_tar_file_path,
                                        self.hadoop_framework.framework_folder_root_path.format(username=self.current_user_name),
                                        self.hadoop_framework.hadoop_folder_name)

    def format_hdfs(self):
        self.hadoop_framework.run_hdfs_command("namenode -format -force")

    def init_hdfs(self):
        self.hadoop_framework.run_hdfs_command("dfs -mkdir -p /user/{}/dependency".format(self.current_user_name))
        self.hadoop_framework.run_hdfs_command("dfs -mkdir -p /user/{}/eventLog".format(self.current_user_name))

    def clear_hadoop(self, ip):
        remove_remote_hadoop_folder_command = "rm -rf {}".format(self.hadoop_framework.hadoop_path)
        remove_remote_hadoop_tar_command = "rm -f {}".format(self.hadoop_framework.remote_hadoop_tar_file_path.format(username=self.user_name[ip]))
        self.shell_utility.run_remote_command(ip, remove_remote_hadoop_folder_command)
        self.shell_utility.run_remote_command(ip, remove_remote_hadoop_tar_command)

    def deploy_hadoop(self, ip):
        self.shell_utility.copy_file_to_remote_target(ip, self.hadoop_framework.local_hadoop_tar_file_path,
                                                      self.hadoop_framework.framework_folder_root_path.format(username=self.user_name[ip]))
        self.shell_utility.unzip_remote_file(ip, self.hadoop_framework.remote_hadoop_tar_file_path.format(username=self.user_name[ip]),
                                             self.hadoop_framework.framework_folder_root_path.format(username=self.user_name[ip]))


if __name__ == "__main__":
    config = Config()
    ip_list = config.get_value("test_machines_ip_list")
    user_name = config.get_value("os_user_name")
    password = config.get_value("os_password")
    deploy = HadoopDeploy(ip_list, user_name, password)
    deploy.run()
