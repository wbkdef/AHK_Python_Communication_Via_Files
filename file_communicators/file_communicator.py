import os
import sys
import time

from flexible_logger import log

time.sleep(.05)




if len(sys.argv) > 3:
    dir = sys.argv[1]
    in_file = sys.argv[2]
    logfile = sys.argv[3]
else:
    dir = r'C:\Users\Willem\Desktop\organization\Autohotkey\file_communication'
    in_file = r'C:\Users\Willem\Desktop\organization\Autohotkey\file_communication\return.txt'
    logging_filename = r'C:\Users\Willem\Desktop\organization\Autohotkey\file_communication\log.txt'
    log('using default values', 1)


log("python started")
# log("python started")

# __Q:  Set parent_dir="path to parent directory"
parent_dir = 0
# __A:
abs_path = os.path.realpath(__file__)
dir_name = os.path.dirname(abs_path)
parent_dir = os.path.dirname(dir_name)

sys.path.append(parent_dir)

from command_get_put import CommandGetterAndPutter
from command_dispatcher import CommandDispatcher
from lib import case_conversion
import todo_dates

log("\n\n--- abs_path: ---\n" + abs_path + "\n------------\n", 5)
log("\n\n--- dir_name: ---\n" + dir_name + "\n------------\n", 5)
log("\n\n--- parent_dir: ---\n" + parent_dir + "\n------------\n", 5)

cd = CommandDispatcher()
cd.case_conversion = case_conversion
cd.case_conversion = case_conversion
cd.todo_dates = todo_dates

cgp = CommandGetterAndPutter(dir, in_file, cd, .01)
cgp.listen_to_in_file()


