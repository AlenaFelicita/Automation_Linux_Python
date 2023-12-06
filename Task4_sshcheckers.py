import paramiko


def ssh_checkout(host, user, password, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode('utf-8')
    client.close()
    if text in out and exit_code == 0:
        return True
    return False


def ssh_checkout_negative(host, user, password, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode('utf-8')
    client.close()
    if text in out and exit_code != 0:
        return True
    return False


def ssh_checkout_get(host, user, password, cmd, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = (stdout.read() + stderr.read()).decode('utf-8')
    client.close()
    return out


def upload_files(host, user, password, local_path, remote_path, port=22):
    print(f'Load files {local_path} in {remote_path}')
    trasport = paramiko.Transport((host, port))
    trasport.connect(None, username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(trasport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if trasport:
        trasport.close()


def dowload_files(host, user, password, local_path, remote_path, port=22):
    print(f'Load files {local_path} in {remote_path}')
    trasport = paramiko.Transport((host, port))
    trasport.connect(None, username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(trasport)
    sftp.get(local_path, remote_path)
    if sftp:
        sftp.close()
    if trasport:
        trasport.close()
