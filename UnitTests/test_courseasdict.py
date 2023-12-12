import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.Model_Classes.Template_Dicts_Functions import (
    func_CourseAsDict,
    func_AscendingSectionList,
    func_AlphabeticalMyUserList
)
from django.test import TestCase, Client

class CourseAsDictTest(TestCase):

    def setUp(self):
        self.swe = Course(1, "SWE", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_DictionaryCreatedCourse(self):
        dict = func_CourseAsDict(1)
        self.assertEqual(dict.get("id"), self.swe.id, "id is not the same")
        self.assertEqual(dict.get("title"), self.swe.__str__(), "title is not the same")
        self.assertEqual(dict.get("name"), self.swe.name, "name is not the same")
        self.assertEqual(dict.get("department"), self.swe.department, "department is not the same")
        self.assertEqual(dict.get("coursenumber"), self.swe.courseNumber, "coursenumber is not the same")
        self.assertEqual(dict.get("semester"), self.swe.semester.capitalize(), "semester is not the same")
        self.assertEqual(dict.get("year"), self.swe.year, "year is not the same")
        self.assertEqual(dict.get("users"), func_AlphabeticalMyUserList(MyUser.objects.filter(course__id=self.swe.id)), "users are not the same")
        self.assertEqual(dict.get("sections"), func_AscendingSectionList(Section.objects.filter(course=self.swe.id)), "sections are not the same")
    def test_DictionaryNotCreatedCourse(self):
        with self.assertRaises(Exception):
            dict = func_CourseAsDict("email")
            dict = func_CourseAsDict()
            dict = func_CourseAsDict(2)