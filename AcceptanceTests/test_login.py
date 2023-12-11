import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.henry = MyUser(1,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()

    def test_Template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'login.html')
    def test_SessionVars(self):
        response = self.client.get('/')
        self.assertNotIn("email", self.client.session, "Session has email saved at login screen.")
        self.assertNotIn("role", self.client.session, "Session has role saved at login screen.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at login screen.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at login screen.")

    def test_ValidLogin(self):
        response = self.client.post("/", {"email": "writchie@uwm.edu", "password": "password"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"], "Email not saved to the session.")
        self.assertEqual("admin", self.client.session["role"], "Role not saved to the session.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved after login.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved after login.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved after login.")

    def test_WrongPassword(self):
        response = self.client.post("/", {"email": "writchie@uwm.edu", "password": "wrong"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Incorrect password.", response.context["message"],
                         "Incorrect Password does not return error message.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved after invalid login.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved after invalid login.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved after invalid login.")

    def test_BlankPassword(self):
        response = self.client.post("/", {"email": "writchie@uwm.edu", "password": ""}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Fields cannot be blank.", response.context["message"],
                         "Blank Password does not return error message.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved after invalid login.")
        self.assertNotIn("selectedcourse", self.client.session,
                         "Session has selected course saved after invalid login.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section saved after invalid login.")

    def test_BlankEmail(self):
        response = self.client.post("/", {"email": "", "password": "pasword"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Fields cannot be blank.", response.context["message"],
                         "Blank Email does not return error message.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved after invalid login.")
        self.assertNotIn("selectedcourse", self.client.session,
                         "Session has selected course saved after invalid login.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section saved after invalid login.")

    def test_BlankEmailAndPassword(self):
        response = self.client.post("/", {"email": "", "password": ""}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("Fields cannot be blank.", response.context["message"],
                         "Blank Email and password does not return error message.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved after invalid login.")
        self.assertNotIn("selectedcourse", self.client.session,
                         "Session has selected course saved after invalid login.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section saved after invalid login.")

    def test_NoUserWithUserName(self):
        response = self.client.post("/", {"email": "tchie@uwm.edu", "password": "password"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after invalid login.")
        self.assertNotIn("role", self.client.session, "Session has role after invalid login.")
        self.assertEqual("That username does not exist.", response.context["message"],
                         "No MyUser associated with email does not return error message.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved after invalid login.")
        self.assertNotIn("selectedcourse", self.client.session,
                         "Session has selected course saved after invalid login.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section saved after invalid login.")

    def test_ByPassLogin(self):
        response = self.client.get("/dashboard/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to dashboard")

        response = self.client.get("/directory/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to directory")

        response = self.client.get("/userpage/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to userpage")

        response = self.client.get("/createuser/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to createuser")

        response = self.client.get("/edituser/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to edituser")

        response = self.client.get("/courselist/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to courselist")

        response = self.client.get("/coursepage/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to coursepage")

        response = self.client.get("/createcourse/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to createcourse")

        response = self.client.get("/editcourse/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to editcourse")

        response = self.client.get("/createsection/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to createsection")

        response = self.client.get("/sectionpage/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to sectionpage")

        response = self.client.get("/editsection/",follow=True)
        self.assertTemplateUsed(response, 'login.html', "User sucessfully bypassed login to get to editsection")
