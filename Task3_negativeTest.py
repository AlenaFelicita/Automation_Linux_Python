import yaml
from checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_step1(self, make_files, make_folders, clear_folders, make_bad_arx):
        result1 = checkout_negative(f"cd {data['folder_out']};"
                                    f" 7z e bad_arx.{data['arc_type']} -o{data['folder_ext']} -y", "ERRORS")
        assert result1, "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, make_bad_arx):
        assert checkout_negative(f"cd {data['folder_out']}; 7z t bad_arx.{data['arc_type']} ",  "ERRORS"),\
            "test2 FAIL"
