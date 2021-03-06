#!/usr/bin/env python3
import sys

__author__ = 'kocsenc'

from time import sleep
from random import randint

from selenium.common.exceptions import NoSuchElementException

# noinspection PyUnresolvedReferences
from common.MyCourses import MyCourses


class ReadDiscussions(MyCourses):
    def __init__(self, sleep_time):
        super().__init__()
        self.d = self.driver
        self.w = self.wait
        self.sleep_time_per_post = sleep_time

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
            if self.sleep_time_per_post:
                sleep_time = self.sleep_time_per_post
                print("Reading %d words in %d seconds." % (num_words, sleep_time))
            else:
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
    args = sys.argv
    if len(args) >= 2 and args[1].isdigit():
        read_time = int(args[1])
    else:
        read_time = None

    c = ReadDiscussions(read_time)
    c.run()
