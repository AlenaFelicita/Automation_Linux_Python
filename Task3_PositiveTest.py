from checkers import checkout
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files):
        result1 = checkout(f"cd {data['folder_in']}; 7z a -t{data['arc_type']} {data['folder_out']}/arx2",
                           "Everything is Ok")
        result2 = checkout(f"cd {data['folder_out']}; ls", f"arx2.{data['arc_type']}")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        result1 = checkout(f"cd {data['folder_in']}; 7z a -t{data['arc_type']} {data['folder_out']}/arx2",
                           "Everything is Ok")
        result2 = checkout(f"cd {data['folder_out']}; 7z e arx2.{data['arc_type']} -o{data['folder_ext']} -y",
                           "Everything is Ok")
        result3 = checkout(f"cd {data['folder_ext']}; ls", make_files[0])
        assert result1 and result2 and result3, "test2 FAIL"

    def test_step3(self, clear_folders, make_files):
        result2 = checkout(f"cd {data['folder_in']}; 7z a -t{data['arc_type']} {data['folder_out']}/arx2",
                           "Everything is Ok")
        result1 = checkout(f"cd {data['folder_out']}; 7z x arx2.{data['arc_type']} -o{data['folder_ext2']}",
                           "Everything is Ok")
        assert result1 and result2, "test3 FAIL"

    def test_step4(self, clear_folders, make_files):
        result1 = checkout(f"cd {data['folder_in']}; 7z a -t{data['arc_type']} {data['folder_out']}/arx2",
                           "Everything is Ok")
        result2 = checkout(f"cd {data['folder_out']}; 7z l arx2.{data['arc_type']}", make_files[0])
        assert result1 and result2, "test4 FAIL"


    def test_step5(self, clear_folders, make_files):
        result2 = checkout(f"cd {data['folder_in']}; 7z a -t{data['arc_type']} {data['folder_out']}/arx2",
                           "Everything is Ok")
        result1 = checkout(f"cd {data['folder_out']}; 7z t arx2.{data['arc_type']}",
                        "Everything is Ok")
        assert result1 and result2, "test5 FAIL"

    def test_step6(self):
        assert checkout(f"cd {data['folder_in']}; 7z u {data['folder_out']}/arx2.{data['arc_type']}",
                        "Everything is Ok"), "test6 FAIL"

    def test_step7(self, make_files, make_sub_folder):
        result2 = checkout(f"cd {data['folder_in']}; 7z a -t{data['arc_type']} {data['folder_out']}/arx2",
                           "Everything is Ok")
        result1 = checkout(f"cd {data['folder_out']}; 7z d arx2.{data['arc_type']}",
                        "Everything is Ok")
        assert result1 and result2, "test7 FAIL"
