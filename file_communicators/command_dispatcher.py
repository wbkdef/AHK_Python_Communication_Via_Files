import sys
from easygui import msgbox

class CommandDispatcher:
    def shut_down(self):
        sys.exit()

    def __getattr__(self, item):
        msgbox("attribute not found: %s" % item)

