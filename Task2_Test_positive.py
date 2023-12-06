import subprocess
import zlib
tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"
folder2 = "/home/user/folder2"


def crc32(cmd):
    with open(cmd, 'rb') as g:
        hash = 0
        while True:
            s = g.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "test1 FAIL"


def test_step2():
    result1 = checkout(f"cd {out}; 7z e arx2.7z -o{folder1} -y", "Everything is Ok")
    result2 = checkout(f"cd {folder1}; ls", "one")
    result3 = checkout(f"cd {folder1}; ls", "two")
    assert result1 and result2 and result3, "test2 FAIL"


def test_step3():
    result1 = checkout(f"cd {out}; 7z l arx2.7z", "")
    result2 = checkout(f"cd {out}; 7z l arx2.7z", "one")
    result3 = checkout(f"cd {out}; 7z l arx2.7z", "two")
    assert result1 and result2 and result3, "test3 FAIL"


def test_step4():
    result1 = checkout(f"cd {out}; 7z x arx2.7z -o{folder2}", "Everything is Ok")
    result2 = checkout(f"cd {folder2}; ls", "one")
    result3 = checkout(f"cd {folder2}; ls", "two")
    assert result1 and result2 and result3, "test4 FAIL"


def test_step5():
    result1 = crc32(f'{out}/arx2.7z').lower()
    assert checkout(f'crc32 {out}/arx2.7z', result1), "test5 FAIL"


def test_step6():
    assert checkout(f"cd {out}; 7z t arx2.7z", "Everything is Ok"), "test6 FAIL"


def test_step7():
    assert checkout(f"cd {tst}; 7z u {out}/arx2.7z", "Everything is Ok"), "test7 FAIL"


def test_step8():
    assert checkout(f"cd {out}; 7z d arx2.7z", "Everything is Ok"), "test8 FAIL"
