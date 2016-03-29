from os.path import join, dirname, realpath

python_dir = dirname(dirname(dirname(realpath(__file__))))
fil_communicators_dir = join(python_dir, 'file_communicators')

import sys
sys.path.append(fil_communicators_dir)

import tempfile

import pytest

import command_get_put

@pytest.fixture()
def temp_dir():
    return tempfile.mkdtemp()

@pytest.fixture()
def in_file(temp_dir, filename='to_python_tester'):
    in_file_name = join(temp_dir, filename)
    return in_file_name

@pytest.fixture()
def out_file(temp_dir, filename='from_python_tester'):
    return join(temp_dir, filename)

@pytest.fixture()
def in_file_contents(): return "generic_fcn_name,--,for in file"

@pytest.fixture()
def initialize_infile(in_file, in_file_contents):
    with open(in_file, 'w') as f:
        f.write(in_file_contents)

pytestmark = pytest.mark.usefixtures('initialize_infile')

def my_fcn(arg):
    return 'my_fcn called with argument %s' % arg

class CmdDispatcher:
    def __init__(self):
        self.args = []
        self.kwargs = {}
        self.generic_fcn_name = my_fcn

    def __call__(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)
        return "Output,--,from,--,CmdDispatcher"

@pytest.fixture()
def cmd_dispatcher():
    return CmdDispatcher()

@pytest.fixture()
def cmd_get_put(in_file, out_file, cmd_dispatcher):
    cgp = command_get_put.CommandGetterAndPutter(in_file, out_file, cmd_dispatcher)
    return cgp

def test_init(in_file: str,
              out_file: str,
              cmd_dispatcher: CmdDispatcher,
              cmd_get_put: command_get_put.CommandGetterAndPutter):
    assert cmd_get_put.in_file is in_file
    assert cmd_get_put.out_file is out_file
    assert cmd_get_put.out_file is out_file
    assert isinstance(cmd_get_put.in_file_last_modified_time, float)
    assert cmd_get_put.sleep_time_between_listen == .02
    assert cmd_get_put.command_dispatcher is cmd_dispatcher

def test_dispatch_command(cmd_get_put: command_get_put.CommandGetterAndPutter,
                          cmd_dispatcher: CmdDispatcher,
                          out_file: str):
    cmd_get_put._dispatch_command()
    assert cmd_dispatcher.args == ['Generic contents', 'for in file']
    with open(out_file) as f:
        assert f.read() == 'Output,--,from,--,CmdDispatcher'

def test_dispatch_command2(cmd_get_put: command_get_put.CommandGetterAndPutter,
                          in_file: str):
    assert cmd_get_put.in_file_modified_since_last_check() is False
    assert cmd_get_put.in_file_modified_since_last_check() is False
    with open(in_file, 'w') as f:
        f.write("new stuff")
    assert cmd_get_put.in_file_modified_since_last_check() is True
    assert cmd_get_put.in_file_modified_since_last_check() is False


        # __c Continue From Here!




