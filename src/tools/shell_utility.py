from subprocess import call


class ShellUtility(object):
    def __init__(self, user_name=None, password=None, local_password=None):
        self.user_name = user_name
        self.password = password
        self.local_password = local_password

    def call_shell_command(self, command):
        call([command], shell=True)

    def call_sudo_shell_command(self, command):
        command = "echo \'{}\' | sudo -S /bin/su -c \'{}\'".format(self.local_password, command)
        self.call_shell_command(command)

    def call_bash_script(self, bash_script_path):
        command = "bash {}".format(bash_script_path)
        self.call_shell_command(command)

    def copy_file_to_remote_target(self, ip, local_file_path, remote_target_folder_path):
        copy_file_command = 'scp "{}" {}@{}:{}'.format(local_file_path, self.user_name[ip], ip, remote_target_folder_path)
        self.call_shell_command(copy_file_command)

    def copy_file_to_remote_target_without_pub_key(self, ip, local_file_path, remote_target_folder_path):
        copy_file_command = 'sshpass -p "{}" scp {} {}@{}:{}'.format(self.password[ip], local_file_path, self.user_name[ip],
                                                                     ip, remote_target_folder_path)
        print(copy_file_command)
        self.call_shell_command(copy_file_command)

    def run_remote_command(self, ip, command):
        remote_command = "ssh {}@{} {}".format(self.user_name[ip], ip, command)
        self.call_shell_command(remote_command)

    def run_remote_sudo_command(self, ip, command):
        remote_command = 'echo "{}" | ssh {}@{} "sudo -S /bin/su -c \\\"{}\\\""'.format(self.password[ip], self.user_name[ip],
                                                                                        ip,
                                                                                        command)
        self.call_shell_command(remote_command)

    def run_remote_command_without_pub_key(self, ip, command):
        remote_command = "sshpass -p '{}' ssh {}@{}  \"{}\"".format(self.password[ip], self.user_name[ip], ip,
                                                                    command)
        self.call_shell_command(remote_command)

    def run_remote_sudo_command_without_pub_key(self, ip, command):
        remote_command = "sshpass -p '{}' ssh  {}@{} \"echo '{}' | sudo -S {}\"".format(self.password[ip], self.user_name[ip],
                                                                                        ip, self.password[ip], command)
        self.call_shell_command(remote_command)

    def unzip_remote_file(self, ip, zip_file_path, target_folder):
        unzip_command = "tar -zxf {} -C {}".format(zip_file_path, target_folder)
        self.run_remote_command(ip, unzip_command)

    def package_file(self, output_path, source_folder_path, source_file_path):
        tar_command = "tar -zcf {} -C {} {}".format(output_path, source_folder_path, source_file_path)
        self.call_shell_command(tar_command)
