import yaml

from tests.sshcheckers import ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self, make_folders, make_files):
        result1 = ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                               f"cd {data['folder_in']}; 7z a -t{data['type']} {data['folder_out']}/arx2",
                               f"{data['valid']}")
        result2 = ssh_checkout('0.0.0.0', f"{data['user']}", f"{data['password']}",
                               f"cd {data['folder_out']}; ls", f"arx2.{data['type']}")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, make_files):
        result1 = ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                               f"cd {data['folder_out']}; 7z e arx2.{data['type']} -o{data['folder_ext']} -y",
                               f"{data['valid']}")
        result2 = ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                               "cd {}; ls".format(data['folder_ext']), make_files[0])
        assert result1 and result2, "test2 FAIL"

    def test_step4(self):
        result1 = ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                               f"cd {data['folder_out']}; 7z x arx2.{data['type']} -o{data['folder_ext2']}",
                               f"{data['valid']}")
        assert result1, "test4 FAIL"

    def test_step6(self):
        assert ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                            f"cd {data['folder_out']}; 7z t arx2.{data['type']}",
                            f"{data['valid']}"), "test6 FAIL"

    def test_step7(self):
        assert ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                            f"cd {data['folder_in']}; 7z u {data['folder_out']}/arx2.{data['type']}",
                            f"{data['valid']}"), "test7 FAIL"

    def test_step8(self):
        assert ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                            f"cd {data['folder_out']}; 7z d arx2.{data['type']}",
                            f"{data['valid']}"), "test8 FAIL"

    def test_step5(self, make_files, make_sub_folder):
        result2 = ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                               f"cd {data['folder_in']}; 7z a -t{data['type']} {data['folder_out']}/arx2",
                               f"{data['valid']}")
        result1 = ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                               f"cd {data['folder_out']}; 7z d arx2.{data['type']}",
                               f"{data['valid']}")
        assert result1 and result2, "test5 FAIL"
