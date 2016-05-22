# -*- coding: utf-8 -*-
import os
import sys
port = 8080

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

lib_path = os.path.join(CURRENT_PATH, "lib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
lib_path = os.path.join(CURRENT_PATH, "lib/PIL")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
lib_path = os.path.join(CURRENT_PATH, "mylib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# print(CURRENT_PATH)
# CURRENT_PATH = os.path.dirname(CURRENT_PATH)
# print(CURRENT_PATH)

HDL_DIR = ["managehdl","sitehdl","publichdl"]
UPLOAD_DIR = os.path.join(CURRENT_PATH, 'upload')
UPLOAD_MAX_SIZE = 3   #MB

web_server = {
    'login_url': '/login',
    'template_path': os.path.join(CURRENT_PATH, 'views/tmplts'),
    'static_path': os.path.join(CURRENT_PATH, 'views/static'),
    # 'static_path':  'views/static',
    'tmp_path': os.path.join(CURRENT_PATH, 'tmp'),
    'xsrf_cookies': True,
    'cookie_secret': "jjhfu8489582366$@%^@#!*()^GTG",
    'cookie_expires': 86400,
    'autoescape': None,
    'debug': True,
}
# print(web_server)
session_settings = {
    'cookie_name': 'sessionid',
    'secret_key': 'jjfKJuUJLJi87&y67YUhUIh7y7y7hH&ohuhlH7jjff&',
    'invalid_days': 1, # 1 * 24 means 1 days
    'cookie_expires_days': 30,
}

db = {
    'name': 'mydb',
    'host':'127.0.0.1',
    'port':27017,
}

CPTCH_STR = {
    'cpth_len':[3], # 字符位数4,5,6
    'cpth_type':[2], # 字符类型1,2,3
    'filte_char':['o','O','0'], #排除字符
}
INK = "red", "black", "green", "blue", "gray", "purple", "chocolate", "deeppink", "blueviolet", "royalblue", "olivedrab", "firebrick", "seagreen", "darkslateblue", "darkslategray", "darkolivegreen", "darkgoldenrod", "deepskyblue", "darkcyan", "darkorchid" # 字符颜色
CPTCH = {'text': "",
    'size': 36, # 字体大小
    'bkground': '#999', # 背景颜色
    'font_color': '', # 字体颜色  random.choice(INK)
    'addWidth': 60, # 图片宽度
    'addHeight': 8 # 图片高度
}

VERIFY_TEXT_SALT = "KDJFk**^$(_+hjhHHHY7789hhg^$#"
PASSWORD_SALT = "KDDJKKJI*&^^&7jkdfjhu)((__I?>"
