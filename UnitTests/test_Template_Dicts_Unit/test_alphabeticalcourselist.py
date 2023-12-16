import sys

from SchedulingApp.Model_Classes.Template_Dicts_Functions import func_AlphabeticalCourseList

sys.path.append('../../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.Model_Classes.Template_Dicts_Functions import func_AlphabeticalCourseList

from django.test import TestCase, Client
class AlphabeticalCourseListTest(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.ca = Course(2, "Computer Architecture", "COMPSCI", 451, "spring", 2023)
        self.ca.save()
        self.geo = Course(3, "Our Physical Environment", "GEOG", 120, "spring", 2023)
        self.geo.save()

    def test_List(self):
        sortedList = func_AlphabeticalCourseList(Course.objects.all())
        self.assertEqual(sortedList[0].get("title"), "COMPSCI 361 Software Engineering", "Incorrect Title")
        self.assertEqual(sortedList[0].get("id"), 1, "incorrect id")
        self.assertEqual(sortedList[0].get("semester"), "Spring", "incorrect semester")
        self.assertEqual(sortedList[0].get("year"), 2023, "incorrect year")

        self.assertEqual(sortedList[1].get("title"), "COMPSCI 451 Computer Architecture", "Incorrect Title")
        self.assertEqual(sortedList[1].get("id"), 2, "incorrect id")
        self.assertEqual(sortedList[1].get("semester"), "Spring", "incorrect semester")
        self.assertEqual(sortedList[1].get("year"), 2023, "incorrect year")

        self.assertEqual(sortedList[2].get("title"), "GEOG 120 Our Physical Environment", "Incorrect Title")
        self.assertEqual(sortedList[2].get("id"), 3, "incorrect id")
        self.assertEqual(sortedList[2].get("semester"), "Spring", "incorrect semester")
        self.assertEqual(sortedList[2].get("year"), 2023, "incorrect year")
