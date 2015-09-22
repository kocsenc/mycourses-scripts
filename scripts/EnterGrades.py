#!/usr/bin/env python3

__author__ = 'kocsenc'

import MyCourses
import sys
import os.path
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class EnterGrades(MyCourses):
    """
    Script to enter grades
    """

    def __init__(self, grades_file):
        super().__init__()

        self.d = self.driver
        self.w = self.wait
        self.entries = self.get_grades_from_file(grades_file)
        # TODO: Check if we should skip feedback for performance
        self.skip_feedback = False
        self.run()

    def run(self):
        """
        prompts the user to navigate to page
        where you need to input grades and inputs them.
        User must submit manually before final input prompt.
        Final input prompt closes the browser.
        Driver closes at the end
        :param entries:
        :return:
        """
        self.d.get("http://www.mycourses.rit.edu")
        input("Please log in and navigate to grade entry page and press Enter")

        grade_textboxes = self.d.find_element_by_id("z_p").find_elements_by_class_name("d_edt")

        # check if textbox size == grade size
        if len(grade_textboxes) != len(self.entries):
            print("Double check your grades. It seems the list of grades is not matched with the amount of entries.")
            print("Size of grades: " + str(len(self.entries)))
            print("yon MyCourses: " + str(len(grade_textboxes)))
            super().terminate()
            sys.exit()

        for i in range(len(grade_textboxes)):
            # ############
            # Enter Grades
            # ############
            textbox = grade_textboxes[i]
            grade = self.entries[i].grade
            textbox.clear()
            textbox.send_keys(grade)
            time.sleep(0.3)

            # ############
            # Enter feedback
            # ############
            xpath = FeedbackXpath(i + 4).xpath
            feedback_button = self.w.until(EC.presence_of_element_located((By.XPATH, xpath)))
            feedback_button.click()

            if not self.skip_feedback:
                try:
                    # Dealing with iFrame and myCourses Modals
                    # Must switch to modal frame and then comment subframe.
                    # Submit button is in default_content frame.
                    self.w.until(EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="d2l_body"]/div[9]/div/div[1]/table/tbody/tr/td[1]/a[1]')))
                    self.w.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="d2l_form"]')))
                    feedback_frame = self.d.find_elements_by_tag_name('iframe')[1]
                    self.d.switch_to.frame(feedback_frame)

                    sub_frames = self.d.find_elements_by_tag_name('iframe')
                    student_comment_frame = sub_frames[0]
                    instructor_comment_frame = sub_frames[1]

                    self.d.switch_to.frame(student_comment_frame)
                    tbox = self.w.until(EC.presence_of_element_located((By.ID, "tinymce")))
                    tbox.clear()
                    tbox.send_keys(self.entries[i].feedback)
                    self.d.switch_to.default_content()
                    submit_btn = self.d.find_element_by_xpath(
                        '//*[@id="d2l_body"]/div[9]/div/div[1]/table/tbody/tr/td[1]/a[1]')
                    submit_btn.click()

                except Exception as e:
                    print("Error while trying to add comments, exiting...")
                    print("No grades were submitted or altered.")
                    print(e)
                    super().terminate()
                    sys.exit()

        input("Grades should be inputted, revise and submit manually; then press <ENTER>")
        super().terminate()

    def get_grades_from_file(self, filename):
        """
        Opens file named filename where each line is:
        grade'\t'feedback

        It is meant to parse direct copy/paste from any spreadsheet.

        :param filename:
        :return: entry array (i.e. [EntryObject1, EntryObject2, ...]
        """
        entries = []
        with open(filename) as f:
            lines = f.readlines()

        # For line array split on '\t' in the file
        for split in [x.strip().split('\t') for x in lines]:
            grade = split[0]
            if not self.is_number(grade.strip()):
                print("Grade not parsed correctly. Make sure to have grades and comments tab delimited")
                sys.exit()

            if len(split) >= 2:
                feedback = split[1]
            else:
                feedback = ""

            entry = GradeEntry(grade, feedback)
            entries.append(entry)

        return entries

    @staticmethod
    def is_number(s):
        """
        Simple helper to check if number
        :param s:
        :return:
        """
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata

            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


class FeedbackXpath:
    """
    Class to build an xpath for a feedback button
    """

    def __init__(self, elm):
        self.elm = str(elm)
        self.part_one = '//*[@id="z_p"]/tbody/tr['
        self.part_two = ']/td[6]/a'
        self.xpath = self.part_one + self.elm + self.part_two


class GradeEntry:
    """
    Simple Generic Grade entry, has a grade and feedback
    """

    def __init__(self, grade, feedback):
        self.grade = str(grade).strip()
        self.feedback = str(feedback).strip()


if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) < 2:
        print("Usage: \n./EnterGrades.py grade_file.txt")
        sys.exit()

    elif not os.path.isfile(arguments[1]):
        pass
    else:
        c = EnterGrades(arguments[1])
        c.run()
