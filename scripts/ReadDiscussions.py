__author__ = 'kocsenc'

from common.MyCourses import MyCourses


class ReadDiscussions(MyCourses):
    def __init__(self):
        my_courses = super().__init__()
        self.d = my_courses.driver
        self.w = my_courses.wait

    def run(self):
        self._read_discussions()

    def _read_discussions(self):
        input("Navigate to the discussion then press <ENTER>")

        threads_lis = self.d.find_element_by_xpath('//*[@id="threadDataList"]/ul').find_elements_by_tag_name("li")


if __name__ == "__main__":
    c = ReadDiscussions()
    c.run()
