import requests
import sys
import os
from bs4 import BeautifulSoup
import time

# user file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LIB import text_utils as tu
import config

PS_CNCT = tu.PS_CNCT

# Global var
ATCODER_TOP_URL = config.ATCODER_TOP_URL
LOGIN_URL       = config.LOGIN_URL
TEST_CASE_HOME  = config.TEST_CASE_HOME
CONTEST_TOP_URL = 'full path (https://...) <- args[1]'
HEADERS         = config.HEADERS
test_num        = 0

# Get test case from tsk_url (= contest question page)
def generate_test_case(tsk_url, session):
    # global HEADERS
    # global TEST_CASE_HOME
    try:
        top_page    = session.get(tsk_url, headers = HEADERS)
    except requests.exceptions.RequestException as e:
        print (tu.red_text('ERROR'),'could NOT access to', tsk_url)
        print(e)
        return False
    else:
        bs_task     = BeautifulSoup(top_page.text, "lxml")
        lng_ja      = bs_task.find('span', class_ = 'lang-ja').find_all('pre')
        global test_num
        test_letter = str(test_num)
        test_num   += 1
        splitted_url = tsk_url.split('_')
        if(len(splitted_url) > 1):
            test_letter = tsk_url.split('_')[len(splitted_url)-1]
        if (not os.path.isdir(TEST_CASE_HOME)):
            os.mkdir(TEST_CASE_HOME)
        test_case_path       = TEST_CASE_HOME + '/' + test_letter + '.txt'
        test_case_path_print = TEST_CASE_HOME + '/' + tu.yellow_text(test_letter) + '.txt'
        print('generating', test_case_path_print)
        lf = ''
        f = open(test_case_path, 'w')
        for i in range(len(lng_ja)):
            if (lng_ja[i].find('var') is not None):
                continue
            f.write(lf + '\n'.join(lng_ja[i].text.splitlines())+'\n')
            lf = '\n'
        f.close()
        print (" -", tu.green_text("success!"))
    return True

# Get all question page from task_top_url (= contest task list page)
def generate_test_cases(task_top_url, session):
    # global ATCODER_TOP_URL
    print (tu.yellow_text("Get url of questions"))
    try:
        task_top_page = session.get(task_top_url, headers = HEADERS)
        bs_task_top   = BeautifulSoup(task_top_page.text, "lxml")
    except requests.exceptions.RequestException as e:
        print (tu.red_text('ERROR'),'could NOT access to', task_top_url)
        print(e)
        return False
    else:
        task_tbody_a  = bs_task_top.find('tbody').find_all('a')
        task_urls     = {el.get('href') for el in task_tbody_a}
        print (" -",tu.green_text("success!"))
        print (tu.yellow_text("Begin to generate test case texts"))
        for tsk_url in task_urls:
            if  (tsk_url.find('submit')>=0):
                # print("@debug")
                continue
            generate_test_case(ATCODER_TOP_URL + tsk_url, session)
            # Sleep for 1 sec to reduce load on the server
            time.sleep(1)
        print (tu.green_text("All test case texts are generated!"))
    return True

# Login (required to access real-time contest)
def login(login_url, session): 
    print(tu.yellow_text('Login to ' + login_url))
    login_page   = session.get(login_url, headers = HEADERS)
    login_lxml   = BeautifulSoup(login_page.text, 'lxml')
    csrf_token   = login_lxml.find(attrs={'name': 'csrf_token'}).get('value')
    login_info   = {
        "csrf_token": csrf_token,
        "username"  : config.USERNAME,
        "password"  : config.PASSWORD
    }
    login_result = session.post(login_url, data = login_info, headers = HEADERS)
    if (login_result.url != login_url):
        print(" -", tu.green_text("success!"))
        return session
    else:
        print(" -", tu.red_text("failure"))
        print("    -", tu.yellow_text("Please execution python " + os.path.dirname(__file__) + PS_CNCT + "config.py"))
        return None
    return session

# Main
def main():
    args = sys.argv
    # Show help when len(args) == 1 (i.e. without args)
    if (len(args)==1):
        # Set contest url as https://atcoder.jp/contests/[current directory folder name]'
        folder = os.path.split(os.getcwd())
        index = len(folder) - 1
        if(folder[index]==""):
            index-=1
        CONTEST_TOP_URL = ATCODER_TOP_URL + '/contests/' + folder[index]
    else:
        # Set contest url
        CONTEST_TOP_URL     = args[1]
    print(CONTEST_TOP_URL)
    # Session start
    session      = requests.Session()
    # Login phase
    session = login(LOGIN_URL, session)
    # Sleep for 1 sec to reduce load on the server
    time.sleep(1)
    if(session == None):
        exit()
    if(not generate_test_cases(CONTEST_TOP_URL + '/tasks', session)):
        exit()

if __name__ == "__main__":
    main()
