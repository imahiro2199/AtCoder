import os
import sys
import subprocess
from subprocess import PIPE
import time

# user file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LIB import text_utils as tu
import config

PS_CNCT = tu.PS_CNCT

def result_text(flg):
    if flg:
        return tu.green_text("AC")
    else:
        return tu.red_text("WA")

def show_help():
    print(tu.yellow_text('Show Help'))
    print('Set args')
    print(' - args[' + tu.red_text(str(1))   + ']: Question case (lower)')
    print(' - args[' + tu.green_text(str(2)) + ']: Your language [option, default: c++]')
    print('   - e.g., python .\\run_test_case.py', tu.red_text("a"), tu.green_text('c++'))
    print('   - detail: see \"commands()\" function in config.py')
    print('Input file')
    print(' - answer/[args[1]].txt')
    print('   * Inputs')
    print('   * [empty line]')
    print('   * Outputs')
    print('   * [empty line]')
    print('   * Inputs')
    print('   * ...')
    print()

def main():
    args = sys.argv
    arg_len = len(args)

    # Is NOT set question number
    if(arg_len == 1):
        show_help()
        exit()

    run_question     = args[1]

    # Set default language
    lang             = config.DEFAULT_LANG

    if(arg_len > 2):
        lang = args[2]

    if(arg_len > 3):
        option = args[3]

    answer_text = '.' + PS_CNCT + config.TEST_CASE_HOME + PS_CNCT + run_question + '.txt'
    build_path  = '.' + PS_CNCT + config.BUILD_FOLDER   + PS_CNCT

    compile_commands, run_command = config.commands(lang, run_question, build_path)

    print(tu.yellow_text("Information"))
    print(" -", "compile_commands", ":", compile_commands)
    if (not os.path.isdir(build_path)):
        os.mkdir(build_path)
    print(" -", "run_command     ", ":", run_command)
    print()

    # compile
    print(tu.yellow_text("Compile"))
    for cmd in compile_commands:
        try:
            subprocess.run(cmd, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(" -", tu.red_text("COMPILE ERROR"))
            exit()
    print(" -", "Compile finished without Error")
    print()

    input_strs  = []
    output_strs = []
    if os.path.exists(answer_text):
        # context_flg ? output text: input text
        context_flg = False
        file_texts = []
        striped_line = ""
        with open(answer_text, 'r') as f:
            for line in f:
                striped_line = line.strip()
                if(striped_line == "" and len(file_texts) > 0):
                    if context_flg:
                        output_strs.append("\r".join(file_texts))
                    else:
                        input_strs.append("\n".join(file_texts))
                    context_flg = not context_flg
                    file_texts = []
                else:
                    file_texts.append(striped_line)
        if(len(file_texts) > 0 and context_flg):
            output_strs.append("\n".join(file_texts))
    else:
        print(tu.red_text("[IMPORT ERROR]"))
        print (' - ', answer_text, ' is not exist.')
        exit()

    print(tu.yellow_text("Check test cases"))
    # run test_cases
    check_all_green = True
    for i in range(len(output_strs)):
        print(run_command)
        timer    = time.perf_counter()
        with subprocess.Popen(run_command, shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE, universal_newlines=True) as pipe:
            try:
                out, err = pipe.communicate(input_strs[i], timeout = config.TLE_SECOND)
            except subprocess.TimeoutExpired as e:
                check_all_green = False
                print(" - Case " + tu.num2rainbow_text(i+1) + ": " + tu.red_text("TLE (5s)"))
                print(tu.red_text("Exit program"))
                exit()
            if(err!=""):
                check_all_green = False
                print(tu.red_text("[EXE ERROR]"))
                print(err)
                exit()
            else:
                exp_result = [s.split() for s in output_strs[i].splitlines()]
                usr_result = [s.split() for s in out           .splitlines()]
                check_result = exp_result == usr_result
                print(" - Case " + tu.num2rainbow_text(i+1) + ": " + result_text(check_result) + ' (' + str(int((time.perf_counter() - timer)*1000)).rjust(4) + ' ms)')
                if(not check_result):
                    check_all_green = False
                    print(tu.yellow_text("Input"))
                    print('\n'.join(input_strs[i].splitlines()))
                    print()
                    print(tu.yellow_text("Expected Answer"))
                    print('\n'.join(output_strs[0].splitlines()))
                    print()
                    print(tu.yellow_text("Your Answer"))
                    print('\n'.join(out.splitlines()))
                    print()

    print()
    print(tu.yellow_text("Result"))
    print(" -",result_text(check_all_green))
    print()

if __name__ == "__main__":
    main()
