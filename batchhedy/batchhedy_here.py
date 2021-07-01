"""
Python program to run batchhedy in the current directory with default options.
"""

import sys
import os
from os import path
import glob

# Since hedy module lives one directory up from here, we need to
# add that directory to the search path.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from batchhedy import RunHedy

if __name__ == '__main__':
    os.chdir(path.dirname(path.abspath(__file__)))
    RunHedy(
        filename=glob.glob('input/*.hedy'),
        output='output_programs',
        report='output_report.csv').run()