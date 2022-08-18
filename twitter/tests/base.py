import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse, resolve

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from project.tests.factories.user import UserFactory
from utils.browser import make_chrome_browser

MAX_WAIT = 20


class TestFunctionalBase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        self.wait = WebDriverWait(self.browser, 20)
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    @staticmethod
    def get_by_input_name(web_element, name):
        return web_element.find_element(
            By.XPATH, f'//input[@name="{name}"]'
        )

    @staticmethod
    def get_by_textarea_name(web_element, name):
        return web_element.find_element(
            By.XPATH, f'//textarea[@name="{name}"]'
        )

    def login(self, email='admin@admin.net', password='admin', is_superuser=False):
        form = self.browser.find_element(By.ID, 'login')

        user = UserFactory(email=email)
        user.set_password(password)
        if is_superuser:
            user.is_superuser = True
            user.is_staff = True
        user.save()

        username_field = self.get_by_input_name(form, 'username')
        username_field.send_keys(email)

        password_field = self.get_by_input_name(form, 'password')
        password_field.send_keys(password)

        submit = self.browser.find_element(By.ID, 'submit')
        submit.send_keys(Keys.ENTER)

        return user

    def wait_element_to_be_clickable(self, element_id):
        start_time = time.time()
        while True:
            try:
                self.browser.find_element(By.ID, element_id).click()
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.3)


class TestCustomBase(TestCase):
    def response_post(self, url, data=None, **kwargs):
        if data is None:
            data = {}
        return self.client.post(reverse(url, **kwargs), data)

    def response_get(self, url, **kwargs):
        return self.client.get(reverse(url, **kwargs))

    @staticmethod
    def get_view(url, **kwargs):
        return resolve(reverse(url, **kwargs))

    def login(self, email='admin@admin.net', password='admin', is_superuser=False):
        user = UserFactory(email=email)
        user.set_password(password)
        if is_superuser:
            user.is_superuser = True
            user.is_staff = True
        user.save()

        self.client.login(username=email, password=password)

        return user
