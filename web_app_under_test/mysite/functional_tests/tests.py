import sys

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


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
        proxy_url = 'localhost:8080'
        # Uncomment the browser you'd like to use.
        # Phantom will not use proxy if proxy is running on 127.0.1.1
        #   - https://github.com/ariya/phantomjs/issues/11342
        #   - https://github.com/ariya/phantomjs/issues/12407
        # self.browser = phantomjs(proxy_url)
        self.browser = firefox(proxy_url)
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

    def test_can_contact_us(self):
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

        self.browser.find_element_by_css_selector('#contact-form-link').click()

        name_input = self.browser.find_element_by_css_selector('#id_name')
        message_input = self.browser.find_element_by_css_selector('#id_message')
        name_input.send_keys('Tim')
        message_input.send_keys("The site isn't working.")
        self.browser.find_element_by_css_selector('input[type="submit"]').click()

        self.assertEqual(self.browser.current_url, '{}{}'.format(self.server_url, reverse('thanks')))



def firefox(proxy_url=None):
    # Proxy setup varies depending on browser, see:
    # http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#using-a-proxy
    if proxy_url:
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy_url,
            'ftpProxy': proxy_url,
            'sslProxy': proxy_url ,
            'noProxy': '' # set this value as desired
        })
        return webdriver.Firefox(proxy=proxy)
    return webdriver.Firefox()


def phantomjs(proxy_url=None):
    # http://stackoverflow.com/questions/14699718/how-do-i-set-a-proxy-http://stackoverflow.com/questions/14699718/how-do-i-set-a-proxy-for-phantomjs-ghostdriver-in-python-webdriverfor-phantomjs-ghostdriver-in-python-webdriver
    if proxy_url:
        service_args = [
            '--proxy={}'.format(proxy_url),
            '--proxy-type=http',
        ]
        return webdriver.PhantomJS(service_args=service_args)
    return webdriver.PhantomJS()
