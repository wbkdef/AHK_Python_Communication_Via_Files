from lib.argv_in_clip_out_tools import get_from_argv, put_on_clipboard

# print("get_from_argv(): ", get_from_argv())

argv_in = "passed to argv"


def double(s):
    return 2*s

assert get_from_argv() == argv_in

put_on_clipboard("This from test_argv_in_clip_out_tools")
# modify_input_and_copy_to_clipboard(double) #Should give "passed to argvpassed to argv"





# def test_get_from_argv():
#     assert get_from_argv() == argv_in



