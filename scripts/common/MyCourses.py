__author__ = 'kocsenc'

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os.path

USER_CONFIG_FILE_NAME = "../user.config"


class MyCourses:
    def __init__(self):
        """
        Instantiate Selenium driver. All scripts should inherit from this.
        :return:
        """
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)  # Waiting mechanism

        self.driver.get("http://www.mycourses.rit.edu")

        if os.path.isfile(USER_CONFIG_FILE_NAME):
            with open(USER_CONFIG_FILE_NAME) as f:
                user = f.readlines()
            self.login(user[0].strip(), user[1].strip())
        else:
            print(
                "Did you know you can have a '%s' file with user info to automatically login?" % USER_CONFIG_FILE_NAME)
            input("Please log in and press <ENTER>")

    def login(self, user, password):
        """
        Logs in given user + password
        :param user:
        :param password:
        """
        username = self.driver.find_element_by_xpath('//*[@id="login_box"]/form/div[1]/div[2]/input')
        username.send_keys(user)

        pass_field = self.driver.find_element_by_xpath('//*[@id="login_box"]/form/div[2]/div[2]/input')
        pass_field.send_keys(password)

        pass_field.submit()

    def terminate(self):
        """
        Close driver and finish w/ exit code 0
        :return:
        """
        self.driver.close()
        print('bye bye!')
        exit(0)
