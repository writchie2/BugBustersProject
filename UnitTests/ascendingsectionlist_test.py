import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_AscendingSectionList
from django.test import TestCase, Client, RequestFactory

class AscendingSectionListTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session.save()
        self.swe = Course(1, "SWE", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section1 = Section(1, 100, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section1.save()
        self.section2 = Section(2, 200, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section2.save()
        self.section3 = Section(3, 300, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section3.save()

    def test_List(self):
        sortedList = func_AscendingSectionList(Section.objects.all())
        self.assertEqual(sortedList[0].get("title"), "100 Lecture", "Incorrect Title")
        self.assertEqual(sortedList[0].get("id"), 1, "incorrect id")


        self.assertEqual(sortedList[1].get("title"), "200 Lecture", "Incorrect Title")
        self.assertEqual(sortedList[1].get("id"), 2, "incorrect id")


        self.assertEqual(sortedList[2].get("title"), "300 Lecture", "Incorrect Title")
        self.assertEqual(sortedList[2].get("id"), 3, "incorrect id")
