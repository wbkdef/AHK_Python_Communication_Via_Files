import os
import time
from glob import glob

from flexible_logger import log


class CommandGetterAndPutter:
    def __init__(self, communication_directory, in_file_base, command_dispatcher, sleep_time_between_listen=.001, logfile=None):
        self.communication_directory = communication_directory
        self.in_file_base = in_file_base
        try:
            self.in_file_last_modified_time = os.path.getmtime(self.in_file_base)
        except FileNotFoundError:
            self.in_file_last_modified_time = 0
        self.sleep_time_between_listen = sleep_time_between_listen
        self.command_dispatcher = command_dispatcher

        self._call_fcn_from_str__last_id = None

        files_to_delete = glob(communication_directory + "return*")
        files_to_delete += glob(communication_directory + "to_python*")
        for f in files_to_delete:
            os.remove(f)
        # msgbox("hi")
        log('files_to_delete are %s' % files_to_delete, 3)
        s = 'self.communication_directory is %s' % self.communication_directory
        s += '\nself.in_file_base is %s' % self.in_file_base
        log(s, 3)
        # log('self.communication_directory is %s' % self.communication_directory)
        # log('self.in_file_base is %s' % self.in_file_base)

    def _dispatch_command(self, file):
        print("\n-----in _dispatch_command-----")
        with open(file, "r") as f:
            id_fcn_args_str = f.read()
        os.remove(file)
        log("file_in is:" + id_fcn_args_str)
        log("Command to Python Received:" + id_fcn_args_str)
        id, result = self._call_fcn_from_str(id_fcn_args_str)
        log("file: %s\nid_fcn_args_str: %s\nid: %s\n result: %s" % (file, id_fcn_args_str, id, result), 3)
        self.write_to_out_file(id, result)

    def _call_fcn_from_str(self, id_fcn_args_str):
        args = id_fcn_args_str.split(',--,')
        id = args[0]
        if self._call_fcn_from_str__last_id == id:
            raise ConnectionError
        self._call_fcn_from_str__last_id = id
        try:
            fcn = self._get_method(args[1])
        except Exception as e:
            log('_call_fcn_from_str: Error getting attributes for calling method.  String was: ' + id_fcn_args_str + ",\n\n exception is: %s" % e, 3)
            raise
        log('about to call %s with args %s' % (fcn, args[2:]), 3)
        try:
            result = fcn(*args[2:])
        except Exception as e:
            log('_call_fcn_from_str: Error calling method.  String was: ' + id_fcn_args_str + ",\n\n exception is: %s" % e, 3)
            raise
        return id, result

    def _get_method(self, str_method_desc):
        items = str_method_desc.split('.')
        curr = self.command_dispatcher
        for it in items:
            curr = getattr(curr, it)
        return curr

    def write_to_out_file(self, id, result):
        outfile = os.path.join(self.communication_directory, id)
        # msgbox('outfile is:' + outfile)
        log(("writing '%s' to" % result) + outfile + "\n")
        with open(outfile, "w") as f:
            f.write(id + ',--,%s' % result)

    # def in_file_modified_since_last_check(self):
    #     try:
    #         in_file_last_modified_time = os.path.getmtime(self.in_file_base)
    #     except:
    #         return False
    #         # logging.debug("in file DNE")
    #     if self.in_file_last_modified_time == in_file_last_modified_time:
    #         return False
    #     else:
    #         self.in_file_last_modified_time = in_file_last_modified_time
    #         return True

    def listen_to_in_file(self):
        print("starting to listen")
        log("start of listen_to_in_file " + self.in_file_base)
        while True:
            # if self.in_file_modified_since_last_check():
            infiles = glob(self.in_file_base + "*")
            for file in infiles:
                log("dispatching command from %s" % file, 3)
                start_time = time.time()
                try:
                    self._dispatch_command(file)
                except ConnectionError:
                    log("listen_to_in_file: ConnectionError RAISED B/C COMMAND HAS SAME ID AS PREV. ONE!!!!", 3)
                except Exception as e:
                    log("listen_to_in_file: Exception raised in trying to dispatch from file: %s" % e, 3)
                except BaseException as e: #This doesn't catch the errors I want to catch, but displays whenever send shutdown!
                    log("EXITING PYTHON:\n\nlisten_to_in_file: BaseException raised in trying to dispatch from file: %s" % e, 3)
                    raise
                elapsed_time = time.time() - start_time
                print("\n--- elapsed_time: -"
                      "--", elapsed_time, "------------")

            time.sleep(self.sleep_time_between_listen)

if __name__ == '__main__':
    CommandGetterAndPutter(r'C:\Users\Willem\Desktop\organization\Autohotkey\file_communication\to_python',
                           r'C:\Users\Willem\Desktop\organization\Autohotkey\file_communication\return', '3')

