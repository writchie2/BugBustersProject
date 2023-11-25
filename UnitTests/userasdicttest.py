import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_UserAsDict
from django.test import TestCase, Client

class UserAsDictTest(TestCase):

    def setUp(self):
        self.henry = MyUser("writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                   "Milwaukee", "WI", 53026, "admin")
        self.henry.save()

    def test_DictionaryCreatedUser(self):
        dict = func_UserAsDict("writchie@uwm.edu")
        self.assertEqual(dict.get("email"), self.henry.email, "email is not the same")
        self.assertEqual(dict.get("firstname"), self.henry.firstName, "firstname is not the same")
        self.assertEqual(dict.get("lastname"), self.henry.lastName, "lastname is not the same")
        self.assertEqual(dict.get("phonenumber"), self.henry.phoneNumber, "phonenumber is not the same")
        self.assertEqual(dict.get("streetaddress"), self.henry.streetAddress, "streetaddress is not the same")
        self.assertEqual(dict.get("city"), self.henry.city, "city is not the same")
        self.assertEqual(dict.get("state"), self.henry.state, "state is not the same")
        self.assertEqual(dict.get("zipcode"), self.henry.zipcode, "zipcode is not the same")
        self.assertEqual(dict.get("role"), self.henry.role, "role is not the same")
        self.assertEqual(dict.get("fullname"), self.henry.__str__(), "fullname is not the same")
    def test_DictionaryUnCreatedUser(self):
        with self.assertRaises(Exception):
            dict = func_UserAsDict("itchie@uwm.edu")

