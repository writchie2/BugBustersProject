import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.Model_Classes.Template_Dicts_Functions import func_AlphabeticalMyUserList
from django.test import TestCase, Client
class AlphabeticalMyUserListTest(TestCase):
    def setUp(self):
        self.emmaSonnen = MyUser(1,"esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                               "Milwaukee", "WI", '53026', "admin")

        self.emmaSonnen.save()
        self.henryRitchie = MyUser(2,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                               "Milwaukee", "WI", '53026', "admin")

        self.henryRitchie.save()
        self.sarahCramer = MyUser(3,"scramer@uwm.edu", "password", "Sarah", "Cramer", "5555555555", "1234 main st",
                               "Milwaukee", "WI", '53026', "admin")

        self.sarahCramer.save()
        self.bobAllen = MyUser(4,"ballen@uwm.edu", "password", "Bob", "Allen", "5555555555", "1234 main st",
                               "Milwaukee", "WI", '53026', "admin")

        self.bobAllen.save()
    def test_List(self):
        sortedList = func_AlphabeticalMyUserList(MyUser.objects.all())
        self.assertEqual(sortedList[0].get("fullname"), "Bob Allen", "Full name is not Bob Allen")
        self.assertEqual(sortedList[0].get("lastname"), "Allen", "Last name is not Allen")
        self.assertEqual(sortedList[0].get("email"), "ballen@uwm.edu", "email is not ballen@uwm.edu")
        self.assertEqual(sortedList[0].get("role"), "Admin", "Role is not admin")

        self.assertEqual(sortedList[1].get("fullname"), "Sarah Cramer", "Full name is not Sarah Cramer")
        self.assertEqual(sortedList[1].get("lastname"), "Cramer", "Last name is not Cramer")
        self.assertEqual(sortedList[1].get("email"), "scramer@uwm.edu", "email is not scramer@uwm.edu")
        self.assertEqual(sortedList[1].get("role"), "Admin", "Role is not admin")

        self.assertEqual(sortedList[2].get("fullname"), "Henry Ritchie", "Full name is not Henry Ritchie")
        self.assertEqual(sortedList[2].get("lastname"), "Ritchie", "Last name is not Ritchie")
        self.assertEqual(sortedList[2].get("email"), "writchie@uwm.edu", "email is not writchie@uwm")
        self.assertEqual(sortedList[2].get("role"), "Admin", "Role is not admin")

        self.assertEqual(sortedList[3].get("fullname"), "Emma Sonnen", "Full name is not Emma Sonnen")
        self.assertEqual(sortedList[3].get("lastname"), "Sonnen", "Last name is not Sonnen")
        self.assertEqual(sortedList[3].get("email"), "esonnen@uwm.edu", "email is not esonnen@uwm.edu")
        self.assertEqual(sortedList[3].get("role"), "Admin", "Role is not admin")