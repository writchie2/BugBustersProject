import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class CreateSectionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session.save()
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()


    def test_GetTemplate(self):
        response = self.client.get('/createsection/')
        self.assertTemplateUsed(response, 'createsection.html')

    def test_GetSessionVars(self):
        response = self.client.get('/createsection/')
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at createsection screen.")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selectedcourse  not saved when navigating to createsection")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section saved at createsection screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to createsection")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to createsection")

    def test_PostLogout(self):
        response = self.client.post("/createsection/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")


    def test_PostDirectory(self):
        response = self.client.post("/createsection/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/createsection/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostCancel(self):
        response = self.client.post("/createsection/", {"navigation": "cancel"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selectedcourse  not saved when canceling section creation")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostCreateSectionValid(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Section created successfully!",
                         "Error not played if nonunique usernames")

    def test_PostCreateSectionInvalid(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": -100,
                                     "type": "lecture",
                                     "location": "Chemistry BLDG 180",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "Error not played if nonunique usernames")