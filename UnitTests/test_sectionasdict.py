import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.Model_Classes.Template_Dicts_Functions import (
    func_SectionAsDict,
    func_CourseAsDict,
    func_UserAsDict,
    func_AlphabeticalMyUserList
)
from django.test import TestCase, Client

class SectionAsDictTest(TestCase):

    def setUp(self):
        self.swe = Course(1, "SWE", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section1 = Section(1, 100, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section1.save()

        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()
        self.section2 = Section(2, 200, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id, self.henry.id)
        self.section2.save()


    def test_DictionaryCreatedSectionNoUser(self):
        dict = func_SectionAsDict(1)
        self.assertEqual(dict.get("id"), self.section1.id, "id is not the same")
        self.assertEqual(dict.get("sectionnumber"), self.section1.sectionNumber, "title is not the same")
        self.assertEqual(dict.get("type"), self.section1.type.capitalize(), "name is not the same")
        self.assertEqual(dict.get("location"), self.section1.location, "department is not the same")
        self.assertEqual(dict.get("daysmeeting"), self.section1.daysMeeting, "coursenumber is not the same")
        self.assertEqual(dict.get("starttime"), self.section1.startTime + " AM", "semester is not the same")
        self.assertEqual(dict.get("endtime"), self.section1.endTime+ " AM", "year is not the same")
        self.assertEqual(dict.get("course"), func_CourseAsDict(self.swe.id), "course is not the same")


    def test_DictionaryCreatedSectionHasUser(self):
        dict = func_SectionAsDict(2)
        self.assertEqual(dict.get("id"), self.section2.id, "id is not the same")
        self.assertEqual(dict.get("sectionnumber"), self.section2.sectionNumber, "title is not the same")
        self.assertEqual(dict.get("type"), self.section2.type.capitalize(), "name is not the same")
        self.assertEqual(dict.get("location"), self.section2.location, "department is not the same")
        self.assertEqual(dict.get("daysmeeting"), self.section2.daysMeeting, "coursenumber is not the same")
        self.assertEqual(dict.get("starttime"), self.section2.startTime+ " AM", "semester is not the same")
        self.assertEqual(dict.get("endtime"), self.section2.endTime+ " AM", "year is not the same")
        self.assertEqual(dict.get("course"), func_CourseAsDict(self.swe.id), "course is not the same")
        self.assertEqual(dict.get("assigneduser"), func_UserAsDict('writchie@uwm.edu'), "user is not the same")

    def test_DictionaryNotCreatedCourse(self):
        with self.assertRaises(Exception):
            dict = func_CourseAsDict("itchie@uwm.edu")