# -*- coding: utf-8 -*-

import os

import urlparse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


USERNAME = 'technopark36'
PASSWORD = os.environ['PASSWORD']


class Page(object):
    BASE_URL = 'https://ok.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        print(url)
        self.driver.maximize_window()
        self.driver.get(url)

    @property
    def top_menu(self):
        return TopMenu(self.driver)


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)


class OnlinePage(Page):
    PATH = '/online'
    AVATAR = '//a[@class="photoWrapper"]'
    OVERLAY = '//div[@class=__auto]'

    def first_person(self):

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element_located((By.ID, 'pointerOverlay')))
        # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'photoWrapper')))

        self.driver.find_element_by_xpath(self.AVATAR).click()

        url = self.driver.find_element_by_xpath(self.AVATAR).get_attribute('href').split('/')

        return PersonPage(self.driver, url[len(url) - 1])


class PersonPage(Page):
    PATH = '/profile'
    AVATAR = '//a[@class="card_wrp"]'
    COUNTER = '//a[@data-l="t,stats"]'
    ALL = '//a[@href="/feed"][@class="al"]'

    def __init__(self, driver, login):
        Page.__init__(self, driver)
        self.PATH += '/' + login

    @property
    def avatar(self):
        return Avatar(self.driver)

    def open_counter(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-l="t,stats"]')))

        ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(self.COUNTER)).perform()

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.al[href="/feed"]')))
        ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(self.ALL)).click().perform()


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class Mark(Component):
    MARK = '//a[contains(@class,"marks-new_ic")][contains(text(),"{}")]'
    RESULT = '//span[@class="marks-new_ic"]'

    def set_mark(self, mark=5):
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.marks-new_ic')))
        except TimeoutException:
            return 0
        self.driver.find_element_by_xpath(self.MARK.format(mark)).click()

    def check_mark(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.marks-new_ic')))
        return self.driver.find_element_by_css_selector('span.marks-new_ic').text


class AuthForm(Component):
    LOGIN = '//input[@name="st.email"]'
    PASSWORD = '//input[@name="st.password"]'
    SUBMIT = '//input[@data-l="t,loginButton"]'

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class Avatar(Component):
    AVATAR = '//a[@class="card_wrp"]'

    def open(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element_located((By.ID, 'pointerOverlay')))

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.card_wrp')))

        self.driver.find_element_by_xpath(self.AVATAR).click()

    @property
    def marks(self):
        return MarksModal(self.driver)


class TopMenu(Component):
    DROPDOWN = '//div[@class="toolbar_dropdown_w h-mod"]'
    LOGOUT = '//a[@data-l="t,logoutCurrentUser"]'
    LOGOUT_CONFIRM = '//input[@data-l="t,confirm"]'

    def open(self):
        #wait = WebDriverWait(self.driver, 10)
        #wait.until(EC.invisibility_of_element_located((By.ID, 'popLayer_mo')))
        self.driver.find_element_by_xpath(self.DROPDOWN).click()

    def logout(self):
        self.driver.find_element_by_xpath(self.LOGOUT).click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-l="t,confirm"]')))
        self.driver.find_element_by_xpath(self.LOGOUT_CONFIRM).click()


class MarksModal(Component):
    MARK_VALUE = '//a[contains(text(), "{}")]/../../span/span/span[@class="marks-new_ic __ac"]'

    def check_mark(self, expected_value, username):

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, self.MARK_VALUE.format(username))))
        value = int(self.driver.find_element_by_xpath(self.MARK_VALUE.format(username)).text)

        return value == expected_value

