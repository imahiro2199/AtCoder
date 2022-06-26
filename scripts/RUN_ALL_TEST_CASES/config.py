import os
import sys

# user file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LIB import text_utils as tu

PS_CNCT = tu.PS_CNCT

# Folder setting (do NOT write / or \\ at both end)
# Recommend use PS_CNCT instead of / or \\
TEST_CASE_HOME = 'answer'
BUILD_FOLDER   = 'build'

# Timeout setting (unit: second)
TLE_SECOND = 10

# set DEFAULT_LANG used in commands()
DEFAULT_LANG = "c++"

# fix here for your environment
def commands(lang, run_question, build_path):
    # Uncomment if your source code file name is uppercase letter.
    # run_question.upper()

    # c++ (gcc)
    if  (lang == "c++"):
        compile_commands = ['g++ -o ' + build_path + run_question + ' .' + PS_CNCT + run_question + '.cpp']
        run_command      = build_path + run_question + '.exe'

    # python
    elif(lang == "python"):
        compile_commands = ['echo  - Python runs without compile']
        run_command      = 'python ' + run_question + '.py'

    # pypy3
    elif(lang == "pypy3"):
        compile_commands = ['echo  - Python runs without compile']
        run_command      = 'pypy3 ' + run_question + '.py'

    # jupyter notebook -> python
    elif(lang == "jn_python"):
        compile_commands = ['echo  - Convert to python', 'jupyter nbconvert --to python ' + run_question + '.ipynb --output ' + build_path + PS_CNCT + run_question + '.py']
        run_command      = 'python ' + build_path + run_question + '.py'

    # jupyter notebook -> pypy3
    elif(lang == "jn_pypy3"):
        compile_commands = ['echo  - Convert to python', 'jupyter nbconvert --to python ' + run_question + '.ipynb --output ' + build_path + PS_CNCT + run_question + '.py']
        run_command      = 'pypy3 ' + build_path + run_question + '.py'

    # not found
    else:
        print(tu.red_text("NOT DEFINED LANGUAGE"), ":", str(lang))
        exit()
    return [compile_commands, run_command]
