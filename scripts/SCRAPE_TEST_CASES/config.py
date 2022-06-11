import os

# user file
import rsa
from ..LIB import text_utils as tu

PS_CNCT = tu.PS_CNCT

# Used for encoding password
CFG_FOLDER     = os.path.dirname(__file__) + PS_CNCT + 'cfg'
KEY_PATH       = CFG_FOLDER + PS_CNCT + '.key.pem'
USERNAME_PATH  = CFG_FOLDER + PS_CNCT + '.usr'
PASSWORD_PATH  = CFG_FOLDER + PS_CNCT + '.pswd'

# Be careful not to expose this file if you set USERNAME or PASSWORD directly.
USERNAME, PASSWORD = rsa.ecd_msg(KEY_PATH, USERNAME_PATH, PASSWORD_PATH)
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

# Used for scraping
ATCODER_TOP_URL = 'https://atcoder.jp'
LOGIN_URL       = 'https://atcoder.jp/login'

# Used for generating testcase
TEST_CASE_HOME  = './answer'
