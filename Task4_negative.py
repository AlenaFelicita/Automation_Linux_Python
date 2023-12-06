import yaml
from tests.sshcheckers import ssh_checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_step1(self, make_bad_arx):
        result1 = ssh_checkout_negative(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                                        f"cd {data['folder_out']}; 7z e bad_arx.{data['type']} -o{data['folder_ext']} -y",
                                        "ERRORS")
        assert result1, "test1 FAIL"

    def test_step2(self):
        assert ssh_checkout_negative(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                                     f"cd {data['folder_out']}; 7z t bad_arx.{data['type']}",  "ERRORS"), 'test2 FAIL'
