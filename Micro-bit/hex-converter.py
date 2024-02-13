# import uflash

# The uflash module takes a Micro:bit script and converts it to a hex file(its not saved) and then
#   flashes it to the Micro:bit automatically.
# If there is no Micro:bit connected, it will give an error.
# I managed to save the hex file to a specific location only if i run the code from the terminal
#   (uflash Micro-bit/Micro-bit.py C:\Users\Teodor\Desktop\hex).
# Saving the hex file to a specific location is not nessesary at the moment but
#   if we want to emulate the Micro:bit we need it.
#
# Managed to find a way to save a .hex file.

# def flash_hex(input_file):
#     try:
#         uflash.flash(input_file)
#         print("Hex file created successfully")
#     except Exception as e:
#         print(f"Error creating hex file: {e}")
#
#
# input_py_script = 'Micro-bit.py'
# flash_hex(input_py_script)


import subprocess
python_script_path = 'Micro-bit.py'
hex_file_path = ''
subprocess.run(['uflash', python_script_path, hex_file_path])
