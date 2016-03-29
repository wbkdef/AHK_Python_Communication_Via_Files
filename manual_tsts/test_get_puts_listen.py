from os.path import join, dirname, realpath
current_dir = dirname(realpath(__file__))
python_dir = dirname(current_dir)
file_communicators_dir = join(python_dir, 'file_communicators')

import random
import sys
sys.path.append(file_communicators_dir)

import time
from subprocess import Popen, PIPE



in_file = "C:\\Users\\Willem\\Desktop\\organization\\Autohotkey\\Python\\manual_tsts\\in_file"
out_file = "C:\\Users\\Willem\\Desktop\\organization\\Autohotkey\\Python\\manual_tsts\\out_file"

in_file_start_contents = "generic_fcn_name,--,for in file"
out_file_start_contents = "initial contents for out file"

def initialize_file(file, contents):
    with open(file, 'w') as f:
        f.write(contents)

initialize_file(in_file, in_file_start_contents)
initialize_file(out_file, out_file_start_contents)


def get_file_contents(file):
    with open(file) as f:
        return f.read()

# sys.exit()

def exit_and_print_subprocess_data(proc):
    print("in exit_and_print_subprocess_data")
    assert isinstance(proc, Popen) #Just to help PyCharm
    poll_before = proc.poll()
    (std_out, std_err) = proc.communicate(timeout=1)
    print("\n\n--- std_out: ---\n", std_out, "\n------------\n")
    print("\n\n--- std_err: ---\n", std_err, "\n------------\n")
    poll_after = proc.poll()
    poll_before_after = poll_before, poll_after
    print("\n\n--- poll_before_after: ---\n", poll_before_after, "\n------------\n")
    sys.exit()

def set_infile_sleep_assert_out(in_file, in_file_fcn_args, out_file, out_file_expected_contents):
    start_time = time.time()

    id = random.randint(0, 1000)
    in_file_contents = "%s,--,%s"%(id, in_file_fcn_args)
    out_file_expected_contents = "%s,--,%s"%(id, out_file_expected_contents)

    initialize_file(in_file, in_file_contents)
    time.sleep(SLEEP_TIME)
    assert get_file_contents(in_file) == in_file_contents
    out_file_actual_contents = get_file_contents(out_file)
    assert out_file_actual_contents == out_file_expected_contents, out_file_actual_contents + " != " + out_file_expected_contents
    return time.time() - start_time



SLEEP_TIME = .005
print("about to create subprocess")
_Ans = True
sub_file_path = join(current_dir, 'communicator_for_subprocess.py')

def do_subprocess(subprocess_file_path, in_file, out_file):
    start_time = time.time()
    proc = Popen(['python', subprocess_file_path, in_file, out_file], stderr=PIPE, stdout=PIPE)
    assert proc.poll() is None
    time.sleep(.5) #Make sure the process is up and running!
    assert get_file_contents(out_file) == "initial contents for out file"
    for i in range(8):
        set_infile_sleep_assert_out(
                in_file, 'generic_fcn_name,--,for in file new %s' % i,
                out_file, 'proc my_fcn2 called with argument for in file new %s' % i
        )
    set_infile_sleep_assert_out(
            in_file, 'cd1.generic_fcn_name,--,for in file composite',
            out_file, 'proc my_fcn1 called with argument for in file composite'
    )

    assert proc.poll() is None

    initialize_file(in_file, "0,--,shut_down")
    time.sleep(.5)
    assert proc.poll() == 0

    subprocess_std_out, subprocess_std_err = proc.communicate()
    elapsed_time = time.time() - start_time
    return elapsed_time, subprocess_std_out, subprocess_std_err

def deliberative_practice_do_subprocess_bak(subprocess_file_path, in_file, out_file):
    """This fcn tests that the command_get_put does what it is supposed to (after the process is started)

    The subprocess should be run like this if it were on the command line:
        python subprocess_file_path in_file out_file
    """
    assert get_file_contents(out_file) == "initial contents for out file"
    # Hint __A: You need to put some sleeps in to give the subprocess time to get running, otherwise get some assertion errors!
    for i in range(8):
        set_infile_sleep_assert_out(
                in_file, 'generic_fcn_name,--,for in file new %s' % i,
                out_file, 'proc my_fcn2 called with argument for in file new %s' % i
        )
    set_infile_sleep_assert_out(
            in_file, 'cd1.generic_fcn_name,--,for in file composite',
            out_file, 'proc my_fcn1 called with argument for in file composite'
    )
    initialize_file(in_file, "0,--,shut_down")
    # __c Your Code Here
    # __c Check that the subprocess is running when it should be and stopped when it should be!
    return elapsed_time, subprocess_std_out, subprocess_std_err

def deliberative_practice_do_subprocess(subprocess_file_path, in_file, out_file):
    """This fcn tests that the command_get_put does what it is supposed to (after the process is started)

    The subprocess should be run like this if it were on the command line:
        python subprocess_file_path in_file out_file
    """
    assert get_file_contents(out_file) == "initial contents for out file"
    # Hint __A: You need to put some sleeps in to give the subprocess time to get running, otherwise get some assertion errors!
    for i in range(8):
        set_infile_sleep_assert_out(
                in_file, 'generic_fcn_name,--,for in file new %s' % i,
                out_file, 'proc my_fcn2 called with argument for in file new %s' % i
        )
    set_infile_sleep_assert_out(
            in_file, 'cd1.generic_fcn_name,--,for in file composite',
            out_file, 'proc my_fcn1 called with argument for in file composite'
    )
    initialize_file(in_file, "0,--,shut_down")
    # __c Your Code Here
    # __c Check that the subprocess is running when it should be and stopped when it should be!
    return elapsed_time, subprocess_std_out, subprocess_std_err

# __Q:  Change which fcn is commented out below, then implement the fcn above and check that runs correctly! todo_2016_01_25 todo_2016_03_07 todo_2016_06_06 todo_2017_02_06 todo_2019_07_08 todo_2026_04_06
elapsed_time, subprocess_std_out, subprocess_std_err = do_subprocess(sub_file_path, in_file, out_file)
# elapsed_time, subprocess_std_out, subprocess_std_err = deliberative_practice_do_subprocess(sub_file_path, in_file, out_file)

# __Q:  How to turn subprocess_std_out back into a string so it prints properly? todo_2016_01_25 todo_2016_03_07 todo_2016_06_06 todo_2017_02_06 todo_2019_07_08 todo_2026_04_06
subprocess_std_out = subprocess_std_out
# __A:
subprocess_std_out = subprocess_std_out.decode()

print("\n\n--- subprocess_std_out: ---\n", subprocess_std_out, "\n------------\n")
print("\n\n--- subprocess_std_err: ---\n", subprocess_std_err, "\n------------\n")
print("\n\n--- elapsed_time: ---\n", elapsed_time, "\n------------\n")



# assert std_out == b"", std_out
# assert std_err == b"", str(std_err)
