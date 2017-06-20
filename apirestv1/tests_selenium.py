# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
import selenium.webdriver.support.ui as ui


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super(MySeleniumTests, self).setUpClass()

        self.host = 'http://127.0.0.1:8000'

        if 'TRAVIS' in os.environ:
            desired_cap = {
                'os': 'Windows', 'os_version': '10', 'browser': 'IE',
                'browser_version': '11', 'browserstack.local': True,
                'browserstack.debug': True}
            self.driver = webdriver.Remote(
                command_executor=os.environ['BROWSERSTACK_AUTH'],
                desired_capabilities=desired_cap,
            )
        else:
            self.driver = webdriver.Chrome('drivers/chromedriver')

        self.driver.implicitly_wait(10)
        self.wait = ui.WebDriverWait(self.driver, 10)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(MySeleniumTests, self).tearDownClass()

    def test_navigation(self):

        message = 'los illuminatis'

        self.driver.get(self.host)

        def domReady(driver):
            try:
                self.driver.find_element_by_xpath('//button[@type="submit"]')
            except:
                return False
            return True

        self.wait.until(domReady)

        text_input = self.driver.find_element_by_name("text")
        text_input.send_keys(message)

        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

        def uriReady(driver):
            uri = self.driver.find_element_by_id('text-unsafe').text
            return uri.lower().startswith('http')

        self.wait.until(uriReady)

        uri = self.driver.find_element_by_id('text-unsafe').text
        self.driver.get(uri)

        def messageReady(driver):
            m = self.driver.find_element_by_id('text-safe').text
            return m == message

        self.wait.until(messageReady)

        self.driver.refresh()

        def linkReady(driver):
            try:
                driver.find_element_by_xpath('//a')
            except:
                return False
            return True

        self.wait.until(linkReady)

        self.driver.find_element_by_xpath('//a').click()
