import pytest
from checkers import checkout, getout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(
        f"mkdir -p {data['folder_in']} {data['folder_out']} {data['folder_ext']} {data['folder_ext2']}",
        "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f"cd {data['folder_in']}; "
                    f"dd if=/dev/urandom of={filename} bs={data['bs']} count=1 iflag=fullblock", ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def clear_folders():
    return checkout(
        f"rm -rf {data['folder_in']}/* {data['folder_out']}/* {data['folder_ext']}/* {data['folder_ext2']}/*",
        "")


@pytest.fixture()
def make_sub_folder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f"cd {data['folder_in']}; mkdir {subfoldername} ", ''):
        return None, None
    if not checkout(f"cd {data['folder_in']}/{subfoldername};"
                    f" dd if=/dev/urandom of={testfilename} bs={data['bs']} count=1 iflag=fullblock", ''):
        return subfoldername, None
    return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    checkout(f"cd {data['folder_in']}; 7z a -t{data['arc_type']}{data['folder_out']}/bad_arx",
             "Everything is Ok")
    checkout(f"truncate -s 1 {data['folder_out']}/bad_arx.{data['arc_type']}", "")


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%s.%f")}')
    yield
    print(f'\nFinish: {datetime.now().strftime("%H:%M:%s.%f")}')


@pytest.fixture(autouse=True)
def stat_log():
    yield
    time = datetime.now().strftime("%H:%M:%s.%f")
    stat = getout('cat /proc/loadavg')
    checkout(f"echo 'time:{time} count:{data['count']} size;{data['bs']} stat:{stat}' >> stat.txt", '')
