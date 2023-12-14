import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory


class LoginTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.henry = MyUser(1,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st", "Milwaukee", "WI", 53026, "ad")
        self.henry.save()
    def test_ValidLogin(self):
        response = func_Login(self.factory.post("/", {"email":"writchie@uwm.edu","password":"password"}, follow=True))
        self.assertEqual(response,"success.",
                          "Valid Login does not return success message")
    def test_WrongPassword(self):
        response = func_Login(self.factory.post("/", {"email": "writchie@uwm.edu", "password": "pass"}, follow=True))
        self.assertEqual(response, "Incorrect password.",
                          "Wrong Password does not return Incorrect password.")
    def test_BlankPassword(self):
        response = func_Login(self.factory.post("/", {"email": "writchie@uwm.edu", "password": ""}, follow=True))
        self.assertEqual(response, "Fields cannot be blank.",
                         "Blank Password does not return Fields cannot be blank.")
    def test_BlankEmail(self):
        response = func_Login(self.factory.post("/", {"email": "", "password": "password"}, follow=True))
        self.assertEqual(response, "Fields cannot be blank.",
                         "Blank email does not return Fields cannot be blank.")
    def test_BlankEmailAndPassword(self):
        response = func_Login(self.factory.post("/", {"email": "", "password": ""}, follow=True))
        self.assertEqual(response, "Fields cannot be blank.",
                         "Blank email and password does not return Fields cannot be blank.")
    def test_NoUserWithUsername(self):
        response = func_Login(self.factory.post("/", {"email": "Notcreated@uwm.edu", "password": "password"}, follow=True))
        self.assertEqual(response, "That username does not exist.",
                         "No MyUser associated with email does not return That username does not exist.")
