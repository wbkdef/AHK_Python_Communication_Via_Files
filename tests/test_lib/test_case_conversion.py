# __Q:  Get the lib package on the path todo_2016_06_06 todo_2017_02_06 todo_2019_07_08 todo_2026_04_06
lib_dir = 0
lib_dir = 0
# __A:
from os.path import realpath, dirname, join
parent_dir = dirname(dirname(dirname(realpath(__file__))))
lib_dir = join(parent_dir, "lib")
import sys
sys.path.append(lib_dir)
# https://docs.python.org/3/library/os.path.html
# os.path.realpath(path)
#     Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system).
# os.path.abspath(path)
# Return a normalized absolutized version of the pathname path.



from case_conversion import convert_to_python_class_name, convert_to_python_variable_name
import pytest

@pytest.fixture()
def camel():
    return "ThisIsCamel"

@pytest.fixture()
def underscore():
    return "this_is_camel"

def test_convert_to_python_variable_name(camel, underscore):
    assert convert_to_python_variable_name(camel) == underscore

def test_convert_to_python_class_name(camel, underscore):
    assert convert_to_python_class_name(underscore) == camel


