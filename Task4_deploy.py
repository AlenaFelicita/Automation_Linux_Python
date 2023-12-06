import yaml

from sshcheckers import ssh_checkout, upload_files


with open('config.yaml') as f:
    data = yaml.safe_load(f)


def deploy():
    res = []
    upload_files(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 'tests/p7zip-full.deb',
                 '/home/user2/p7zip-full.deb')
    res.append(ssh_checkout(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",
                            'echo "1111" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            'Настраивается пакет'))
    res.append(ssh_checkout(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",
                            'echo "1111" | sudo -S dpkg -s p7zip-full',
                            'Status: install ok installed'))
    return all(res)


if deploy():
    print('Yes')
else:
    print('fail')
