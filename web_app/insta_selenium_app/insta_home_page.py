import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, *, browser):
        self.browser: webdriver = browser

    def wait(self, second):
        self.browser.implicitly_wait(second)

    def login(self, *, username, password):
        self.wait(10)
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        self.wait(10)
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        self.browser.find_element(By.XPATH,
                                  "//button[contains(text(), 'Сохранить данные')]").click()
        time.sleep(1)
        self.browser.find_element(By.XPATH,
                                  "//button[contains(text(), 'Не сейчас')]").click()


class InstaHomePage:

    def __init__(self, *, browser):
        self.browser = browser
        self.browser.get('https://www.instagram.com')

    def go_to_login_page(self):
        return LoginPage(browser=self.browser)
