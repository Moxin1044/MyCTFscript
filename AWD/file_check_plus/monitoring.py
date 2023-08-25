import paramiko
import time
import hashlib
from stat import S_ISDIR


with open('avoid_file_list.txt', 'r') as f:
    avoid_file_lists = f.readlines()
    avoid_file_lists = [line.strip() for line in avoid_file_lists]


def get_md5_checksum(client, file_path):
    stdin, stdout, stderr = client.exec_command(f"md5sum {file_path}")
    md5_output = stdout.read().decode()
    md5_checksum = md5_output.strip().split()[0]
    return md5_checksum


def check_for_changes(client, sftp, path, files):
    changes = []
    for f in sftp.listdir_attr(path):
        if S_ISDIR(f.st_mode):
            changes.extend(check_for_changes(client, sftp, path + '/' + f.filename, files))
        else:
            file_path = path + '/' + f.filename
            if file_path not in files:
                if file_path in avoid_file_lists:
                    changes.append(f"\033[92m初始文件: {file_path}\033[0m")
                    files[file_path] = get_md5_checksum(client, file_path)
                else:
                    changes.append(f"\033[91m新增文件: {file_path}\033[0m")
                    sftp.remove(file_path)
                    changes.append(f"\033[92m成功删除: {file_path}\033[0m")
            else:
                md5_checksum = get_md5_checksum(client, file_path)
                if md5_checksum != files[file_path]:
                    changes.append(f"\033[91m被篡改文件: {file_path}\033[0m")
                    files[file_path] = md5_checksum
    return changes


def monitor_directory_changes(hostname, username, password, directory_path):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        sftp = client.open_sftp()
        files = {}
        while True:
            changes = check_for_changes(client, sftp, directory_path, files)
            if changes:
                print('\n'.join(changes))
            time.sleep(5)
    except (paramiko.AuthenticationException, paramiko.SSHException) as e:
        print(f"Error connecting to remote host: {e}")
    finally:
        client.close()


hostname = 'ip'
username = 'username'
password = 'password'
directory_path = '/var/www/html'

monitor_directory_changes(hostname, username, password, directory_path)
