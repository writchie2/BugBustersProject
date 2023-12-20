import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.henry = MyUser(1,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()

    def test_GetTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'login.html')
    def test_GetSessionVars(self):
        response = self.client.get('/')
        self.assertNotIn("email", self.client.session, "Session has email saved at login screen.")
        self.assertNotIn("role", self.client.session, "Session has role saved at login screen.")
    def test_PostValidLogin(self):
        response = self.client.post("/", {"email": "writchie@uwm.edu", "password": "password"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"], "Email not saved to the session.")
        self.assertEqual("admin", self.client.session["role"], "Role not saved to the session.")
    def test_PostWrongPassword(self):
        response = self.client.post("/", {"email": "writchie@uwm.edu", "password": "wrong"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Incorrect password.", response.context["message"],
                         "Incorrect Password does not return error message.")
    def test_PostBlankPassword(self):
        response = self.client.post("/", {"email": "writchie@uwm.edu", "password": ""}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Fields cannot be blank.", response.context["message"],
                         "Blank Password does not return error message.")
    def test_PostBlankEmail(self):
        response = self.client.post("/", {"email": "", "password": "pasword"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Fields cannot be blank.", response.context["message"],
                         "Blank Email does not return error message.")
    def test_PostBlankEmailAndPassword(self):
        response = self.client.post("/", {"email": "", "password": ""}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Fields cannot be blank.", response.context["message"],
                         "Blank Email and password does not return error message.")
    def test_PostNoUserWithUserName(self):
        response = self.client.post("/", {"email": "tchie@uwm.edu", "password": "password"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("That username does not exist.", response.context["message"],
                         "No MyUser associated with email does not return error message.")
