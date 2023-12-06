import pytest
import random, string
import yaml
from sshcheckers import upload_files, ssh_checkout, ssh_checkout_get
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='module')
def make_folders():
    return ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        f"mkdir -p {data['folder_in']} {data['folder_out']} "
                        f"{data['folder_ext']} {data['folder_ext2']}",
                        "")


@pytest.fixture(autouse=True)
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        f"cd {data['folder_ext']}; dd if=/dev/urandom of={filename} b"
                        f"s={data['bs']} count=1 iflag=fullblock",
                        ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def clear_folders():
    return ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        'rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'],
                                                            data['folder_ext'], data['folder_ext2']),
                        "")


@pytest.fixture()
def make_bad_arx():
    ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 f"cd {data['folder_in']}; 7z a {data['folder_out']}/bad_arx -t{data['type']}",
                 "Everything is Ok")
    ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 f"truncate -s 1 {data['folder_out']}/bad_arx.{data['type']}",
                 "")


@pytest.fixture(autouse=True, scope='module')
def deploy():
    res = []
    upload_files(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 '/home/user/p7zip-full.deb',
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


@pytest.fixture()
def make_sub_folder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(f"{data['ip']}",
                        f"{data['user']}", f"{data['password']}",
                        f"cd {data['folder_in']}; mkdir {subfoldername} ",
                        ''):
        return None, None
    if not ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        f"cd {data['folder_in']}/{subfoldername};"
                        f" dd if=/dev/urandom of={testfilename} bs={data['bs']} count=1 iflag=fullblock",
                        ''):
        return subfoldername, None
    return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%s.%f")}')
    yield
    print(f'\nFinish: {datetime.now().strftime("%H:%M:%s.%f")}')


@pytest.fixture(autouse=True)
def stat_log():
    yield
    time = datetime.now().strftime("%H:%M:%s.%f")
    stat = ssh_checkout_get(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",
                            'cat /proc/loadavg')
    ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 f"echo 'time:{time} count:{data['count']} size;{data['bs']} stat:{stat}' >> stat.txt",
                 '')

@pytest.fixture()
def start_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@pytest.fixture(autouse=True)
def stat(start_time):
    yield
    stat = ssh_checkout_get(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",'cat /proc/loadavg')
    log_load = (f"Start: {start_time}, time: {datetime.now().strftime('%H:%M:%S')},"
                f" count:{data['count']} size;{data['bs']} stat:{stat} \n Finish: {stat}")
    with open('stat', 'a') as f:
        f.write(log_load + "\n")
