import os
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import getpass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# user file
from LIB import text_utils as tu

PS_CNCT = tu.PS_CNCT

DEF_CFG_FOLDER = os.path.dirname(__file__) + PS_CNCT + 'cfg'
KEY_PATH       = DEF_CFG_FOLDER + PS_CNCT + '.key.pem'
USERNAME_PATH  = DEF_CFG_FOLDER + PS_CNCT + '.usr'
PASSWORD_PATH  = DEF_CFG_FOLDER + PS_CNCT + '.pswd'

def gen_config_files(cfg_folder = DEF_CFG_FOLDER):
    print("Generate setting files")
    # Get username and password file
    print('- type your username...')
    user = input('username: ')
    print('- type your password....')
    password = getpass.getpass('password: ')
    key     = RSA.generate(2048)
    prv_key = key
    pub_key = key.publickey()
    cipher_rsa = PKCS1_OAEP.new(pub_key)

    if not os.path.isdir(cfg_folder):
        os.mkdir(cfg_folder)

    key_path      = cfg_folder + PS_CNCT + '.key.pem'
    username_path = cfg_folder + PS_CNCT + '.usr'
    password_path = cfg_folder + PS_CNCT + '.pswd'

    # Save key and messages
    f = open(username_path,'wb')
    f.write(cipher_rsa.encrypt(user.encode()))
    f.close()

    f = open(password_path,'wb')
    f.write(cipher_rsa.encrypt(password.encode()))
    f.close()

    f = open(key_path,'w')
    f.write(prv_key.export_key().decode())
    f.close()

    # Generate .gitignore
    if (not os.path.isfile(os.path.dirname(cfg_folder) + PS_CNCT + '.gitignore')):
        f = open(os.path.dirname(cfg_folder) + PS_CNCT + '.gitignore','w')
        f.write('/' + os.path.basename(cfg_folder))
        f.close()

def get_word(path):
    if (not os.path.isfile(path)):
        return ''
    f   = open(path, 'rb')
    txt =  f.read()
    f.close()
    return txt

def ecd_msg(key_path = KEY_PATH, username_path = USERNAME_PATH, password_path = PASSWORD_PATH):
    prv_key  = get_word(key_path)
    username = get_word(username_path)
    password = get_word(password_path)

    # When fail to get key or message
    if prv_key == '' or username == '' or password == '':
        print("Failed to open setting files...")
        # Make key and message files
        gen_config_files()
        prv_key  = get_word(KEY_PATH)
        username = get_word(USERNAME_PATH)
        password = get_word(PASSWORD_PATH)
    msgs = []
    decipher_rsa = PKCS1_OAEP.new(RSA.import_key(prv_key))
    msg_list = [username, password]
    for msg in msg_list:
        msgs.append(decipher_rsa.decrypt(msg).decode())
    return msgs
