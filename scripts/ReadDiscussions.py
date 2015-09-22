#!/usr/bin/env python3
__author__ = 'kocsenc'

import MyCourses

from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint


class ReadDiscussions(MyCourses):
    def __init__(self):
        super().__init__()
        self.d = self.driver
        self.w = self.wait

    def run(self):
        while input("Navigate to the discussion then press <ENTER> or q to quit") != 'q':
            self._read_discussions()
        super().terminate()

    def _read_discussions(self):
        """
        Actually read the discussion posts
        :return:
        """
        threads = self.d.find_element_by_xpath('//*[@id="threadDataList"]/ul').find_elements_by_class_name("d2l-inline")
        title = threads[0].find_element_by_tag_name('a')
        if title.is_displayed():
            title.click()

        for i in range(len(threads)):
            try:
                text = self.d.find_element_by_xpath('//*[@id="threadContentsPlaceholder"]/div/div[1]/div[1]/p').text
            except NoSuchElementException:
                text = ""

            num_words = len(text.split(' '))
            wpm = randint(200, 250)
            sleep_time = (num_words * 60) / wpm
            print("Reading %d words at %d wpm. Approx: %d seconds" % (num_words, wpm, sleep_time))
            sleep(sleep_time)

            next_button = self.d.find_element_by_xpath(
                '/html/body/div[9]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/a[2]')
            if next_button.is_enabled():
                next_button.click()
            else:
                print("All done?")
                break


if __name__ == "__main__":
    c = ReadDiscussions()
    c.run()
