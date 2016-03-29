from os.path import join, dirname, realpath

python_dir = dirname(dirname(dirname(realpath(__file__))))
file_communicators_dir = join(python_dir, 'file_communicators')

import sys
sys.path.append(file_communicators_dir)

from command_get_put import CommandGetterAndPutter
from command_dispatcher import CommandDispatcher

def my_fcn1(arg): return 'proc my_fcn1 called with argument %s' % arg
def my_fcn2(arg): return 'proc my_fcn2 called with argument %s' % arg

cd1 = CommandDispatcher()
cd1.generic_fcn_name = my_fcn1

cd2 = CommandDispatcher()
cd2.generic_fcn_name = my_fcn2
cd2.cd1 = cd1

in_file, out_file = sys.argv[1:]
cgp = CommandGetterAndPutter(in_file, out_file, cd2)

print('infile is', in_file)
print('outfile is', out_file)

cgp.listen_to_in_file()

