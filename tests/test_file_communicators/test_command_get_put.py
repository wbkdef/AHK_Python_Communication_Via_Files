from os.path import join, dirname, realpath

python_dir = dirname(dirname(dirname(realpath(__file__))))
file_communicators_dir = join(python_dir, 'file_communicators')

import sys
sys.path.append(file_communicators_dir)

import tempfile
import time

from pytest import fixture, mark

from command_get_put import CommandGetterAndPutter
from command_dispatcher import CommandDispatcher

@fixture()
def temp_dir():
    return tempfile.mkdtemp()

@fixture()
def in_file(temp_dir, filename='to_python_tester'):
    in_file_name = join(temp_dir, filename)
    return in_file_name

@fixture()
def out_file(temp_dir, filename='from_python_tester'):
    return join(temp_dir, filename)

@fixture()
def in_file_contents(): return "generic_fcn_name,--,for in file"

@fixture()
def initialize_infile(in_file, in_file_contents):
    with open(in_file, 'w') as f:
        f.write(in_file_contents)

pytestmark = mark.usefixtures('initialize_infile')

def my_fcn1(arg): return 'my_fcn1 called with argument %s' % arg
def my_fcn2(arg): return 'my_fcn2 called with argument %s' % arg

@fixture()
def cd1():
    cd = CommandDispatcher()
    cd.generic_fcn_name = my_fcn1
    return cd

@fixture()
def cd2(cd1):
    cd = CommandDispatcher()
    cd.generic_fcn_name = my_fcn2
    cd.cd1 = cd1
    return cd

@fixture()
def cgp1(in_file, out_file, cd1):
    cgp = CommandGetterAndPutter(in_file, out_file, cd1)
    return cgp

@fixture()
def cgp2(in_file, out_file, cd2):
    cgp = CommandGetterAndPutter(in_file, out_file, cd2)
    return cgp

def get_file_contents(file):
    with open(file) as f:
        return f.read()

def test_listen_to_in_file(in_file, out_file):
    from subprocess import Popen, PIPE
    from os.path import dirname, realpath, join
    communicator_for_subprocess_path = join(dirname(realpath(__file__)), 'communicator_for_subprocess.py')
    initialize_infile(out_file, "out_file initial contents")
    proc = Popen(['python', communicator_for_subprocess_path, in_file, out_file], stderr=PIPE, stdout=PIPE)
    assert proc.poll() is None
    time.sleep(.05)
    assert get_file_contents(out_file) == "out_file initial contents"
    initialize_infile(in_file, "generic_fcn_name,--,for in file modified")
    time.sleep(.5)
    assert get_file_contents(out_file) == "out_file initial contents"
    time.sleep(.05)

    proc.kill()
    time.sleep(.01)
    assert proc.poll() is 1
    (std_out, std_err) = proc.communicate()
    assert std_out == b""
    assert std_err == b"", str(std_err)


def test_in_file_modified_since_last_check(in_file, cgp1: CommandGetterAndPutter):
    assert cgp1.in_file_modified_since_last_check() is False
    with open(in_file, 'w') as f:
        f.write("hi ho")
        time.sleep(.01)
    assert cgp1.in_file_modified_since_last_check() is True
    assert cgp1.in_file_modified_since_last_check() is False
    assert cgp1.in_file_modified_since_last_check() is False
    with open(in_file, 'w') as f:
        f.write("hide ho")
        time.sleep(.01)
    assert cgp1.in_file_modified_since_last_check() is True
    assert cgp1.in_file_modified_since_last_check() is False
    assert cgp1.in_file_modified_since_last_check() is False
    with open(in_file, 'w') as f:
        f.write("hide ho joe")
        time.sleep(.01)
    assert cgp1.in_file_modified_since_last_check() is True
    assert cgp1.in_file_modified_since_last_check() is False
    assert cgp1.in_file_modified_since_last_check() is False

def test_dispatch_command(in_file, out_file, cd1, cd2,
                          cgp1: CommandGetterAndPutter,
                          cgp2: CommandGetterAndPutter):
    cgp1._dispatch_command()
    assert get_file_contents(out_file) == 'my_fcn1 called with argument for in file'
    cgp2._dispatch_command()
    assert get_file_contents(out_file) == 'my_fcn2 called with argument for in file'
    initialize_infile(in_file, "cd1.generic_fcn_name,--,for in file")
    cgp2._dispatch_command()
    assert get_file_contents(out_file) == 'my_fcn1 called with argument for in file'


def test_call_fcn_from_str(in_file, out_file, cd1, cd2,
                           cgp1: CommandGetterAndPutter,
                           cgp2: CommandGetterAndPutter):
    assert cgp1._call_fcn_from_str("generic_fcn_name,--,for in file") == 'my_fcn1 called with argument for in file'
    assert cgp2._call_fcn_from_str("generic_fcn_name,--,for in file") == 'my_fcn2 called with argument for in file'
    assert cgp2._call_fcn_from_str("cd1.generic_fcn_name,--,for in file") == 'my_fcn1 called with argument for in file'

def test_get_method(in_file, out_file, cd1, cd2, cgp1, cgp2):
    assert cgp1._get_method('generic_fcn_name') == my_fcn1
    assert cgp2._get_method('generic_fcn_name') == my_fcn2
    assert cgp2._get_method('cd1') == cd1
    assert cgp2._get_method('cd1.generic_fcn_name') == my_fcn1

def test_init(in_file: str,
              out_file: str,
              cd1: CommandDispatcher,
              cgp1: CommandGetterAndPutter):
    assert cgp1.in_file is in_file
    assert cgp1.out_file is out_file
    assert isinstance(cgp1.in_file_last_modified_time, float)
    assert cgp1.sleep_time_between_listen == .01
    assert cgp1.command_dispatcher is cd1

# def test_dispatch_command(cmd_get_put: CommandGetterAndPutter,
#                           cmd_dispatcher: CmdDispatcher,
#                           out_file: str):
#     cmd_get_put._dispatch_command()
#     assert cmd_dispatcher.args == ['Generic contents', 'for in file']
#     with open(out_file) as f:
#         assert f.read() == 'Output,--,from,--,CmdDispatcher'
#
# def test_dispatch_command2(cmd_get_put: CommandGetterAndPutter,
#                           in_file: str):
#     assert cmd_get_put.in_file_modified_since_last_check() is False
#     assert cmd_get_put.in_file_modified_since_last_check() is False
#     with open(in_file, 'w') as f:
#         f.write("new stuff")
#     assert cmd_get_put.in_file_modified_since_last_check() is True
#     assert cmd_get_put.in_file_modified_since_last_check() is False


        # __c Continue From Here!




