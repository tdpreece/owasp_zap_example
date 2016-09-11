import sys
import unittest

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import safestring

from selenium import webdriver


class TestLogin(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url:
            super().tearDownClass()

    def setUp(self):
        # self.browser = webdriver.PhantomJS()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_login(self):
        username = 'john'
        email = 'lennon@thebeatles.com'
        password = 'johnpassword'
        User.objects.create_user(username, email, password)
        url = '{}{}'.format(self.server_url, reverse('login'))
        self.browser.get(url)
        username_input = self.browser.find_element_by_css_selector('#id_username')
        password_input = self.browser.find_element_by_css_selector('#id_password')
        username_input.send_keys(username)
        password_input.send_keys(password)
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        self.browser.find_element_by_css_selector('#home')
