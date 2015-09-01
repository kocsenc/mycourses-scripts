__author__ = 'kocsenc'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyCourses:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(d, 10)  # Waiting mechanism

        self.driver.get("http://www.mycourses.rit.edu")
        input("Please log in and press ENTER")
