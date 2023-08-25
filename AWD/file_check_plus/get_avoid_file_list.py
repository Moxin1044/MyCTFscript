import paramiko
from stat import S_ISDIR


def save_file_paths(client, sftp, path, f):
    for item in sftp.listdir_attr(path):
        if S_ISDIR(item.st_mode):
            save_file_paths(client, sftp, path + '/' + item.filename, f)
        else:
            file_path = path + '/' + item.filename
            f.write(file_path + '\n')


def get_file_paths(hostname, username, password, directory_path):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        sftp = client.open_sftp()
        with open('avoid_file_list.txt', 'w') as f:
            save_file_paths(client, sftp, directory_path, f)
    except (paramiko.AuthenticationException, paramiko.SSHException) as e:
        print(f"连接远程主机时出错: {e}")
    finally:
        client.close()


hostname = 'ip'
username = 'username'
password = 'password'
directory_path = '/var/www/html'

get_file_paths(hostname, username, password, directory_path)
