from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

def check_file_size_for_diff(client):
    stdin, stdout, stderr = client.exec_command(f"ls -la {file_path} | grep {file_name}")
    stdout_res = stdout.read().strip().decode('utf8')
    stderr_res = stderr.read().strip().decode('utf8')
    print(stdout_res, '\n', f"Error: {stderr_res}")


def put_new_file_to_server(file_name, file_path, ip, username, password):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    check_file_size_for_diff(client)
    scp = SCPClient(client.get_transport())
    scp.put(file_name, remote_path=file_path)
    check_file_size_for_diff(client)
    scp.close()
    client.close()

with open('hosts.txt') as hosts_file:
    res = hosts_file.read().splitlines()
    
for line in res:
    print(line)
    print(put_new_file_to_server(file_name, file_path, line, username, password), '\n\n')
