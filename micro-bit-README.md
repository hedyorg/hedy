#  Documentation for Micro:Bit integration.



## Questions 
1. To display text on the Micro:Bit LED screen, we can use display.scroll('User_text'). When there are no errors, display.show(Image.HAPPY) can be used, 
    and display.show(Image.ANGRY) can be utilized to indicate an error. There is a library called microbit which we can import using from microbit import *, 
    but it is available exclusively for the MicroPython language. This language is specifically designed for microcontrollers and requires parameters tailored to the specific board, in our case, the Micro:Bit.

2. The Micro:Bit comes pre-flashed with a version of MicroPython. However, we cannot directly run .py scripts on the board. They first need to be converted into a specific .hex
    format. I discovered a GitHub repository that accomplishes this: (https://github.com/GauravBole/microbit-micropython-hex), but I encountered some difficulties using it. There's also the official
    https://github.com/bbcmicrobit/micropython, but it's somewhat complex to operate. I found a simpler 'Python-to-hex' tool (bbcmicrobit/PythonEditor). Specifically,
    the .js script located at PythonEditor/js/python-main.js appears to handle the conversion from .py to .hex efficiently.

3. My idea is that when we click 'Run code', it triggers the normal transpiler. Additionally, there should be another button labeled 'Run on Micro:Bit'. When this button is clicked, the transpiler outputs a
    'microbit' .py script. This script then needs to be converted into a .hex file, which can be donloaded and then directly uploaded onto the Micro:Bit board when connected. If we utilize the tool from 
    https://github.com/bbcmicrobit/PythonEditor, and have this line as a first line 'from microbit import *' in our code, an emulated Micro:Bit board will appears on the screen. We can incorporate this feature into
    our website as an output option for people who don't have the physical board but still want to experiment with it.




