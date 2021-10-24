from environs import Env
from selenium import webdriver

from insta_home_page import InstaHomePage

env = Env()
env.read_env()

home_page = InstaHomePage(browser=webdriver.Firefox())
login_page = home_page.go_to_login_page()
login_page.login(username=env.str('USERNAME'),
                 password=env.str('PASSWORD'))
