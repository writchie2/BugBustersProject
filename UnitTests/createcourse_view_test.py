import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class CreateCourseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()


    def test_GetTemplate(self):
        response = self.client.get('/createcourse/')
        self.assertTemplateUsed(response, 'createcourse.html')

    def test_GetSessionVars(self):
        response = self.client.get('/createcourse/')
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at createcourse screen.")
        self.assertNotIn("selectedcourse", self.client.session,
                         "Session has selected course saved at createcourse screen.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section saved at createcourse screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to createcourse")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to createcourse")

    def test_PostLogout(self):
        response = self.client.post("/createcourse/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")


    def test_PostDirectory(self):
        response = self.client.post("/createcourse/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/createcourse/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostCancel(self):
        response = self.client.post("/createcourse/", {"navigation": "cancel"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_CreateCourseValid(self):
        response = self.client.post("/createcourse/",
                                    {"coursename": "Intro to Software Engineering",
                                     "department": "COMPCSI",
                                     "coursenumber": 361,
                                     "semester": "spring",
                                     "year": 2023,
                                     }, follow=True)
        newCourse = Course.objects.filter().first()
        self.assertEqual(newCourse.name, "Intro to Software Engineering", "Course saved with wrong name")
        self.assertEqual(newCourse.department, "COMPCSI", "Course saved with wrong department")
        self.assertEqual(newCourse.courseNumber, 361, "Course saved with wrong coursenumber")
        self.assertEqual(newCourse.semester, "spring", "User saved with wrong email")
        self.assertEqual(newCourse.year, 2023, "Course saved with wrong year")
        self.assertTemplateUsed(response, 'createcourse.html')


    def test_CreateCourseInvalid(self):
        response = self.client.post("/createcourse/",
                                    {"name": "",
                                     "department": "COMPCSI",
                                     "coursenumber": 361,
                                     "semester": "spring",
                                     "year": 2023,
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Please fill out all fields!",
                         "Error not played if nonunique usernames")