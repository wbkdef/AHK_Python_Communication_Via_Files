from lib.argv_in_clip_out_tools import modify_input_and_copy_to_clipboard

# __c This is not used!
from lib.case_conversion import convert_to_python_variable_name

modify_input_and_copy_to_clipboard(convert_to_python_variable_name)

if __name__ == "__main__":
    converted = convert_to_python_variable_name("Hello there")
    print("converted: ", converted)

