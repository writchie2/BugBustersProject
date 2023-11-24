import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class UserPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selecteduser"] = "esonnen@uwm.edu"
        session.save()
        self.henryRitchie = MyUser("writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                       "Milwaukee", "WI", 53026, "instructor")
        self.henryRitchie.save()
        self.emmaSonnen = MyUser("esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                 "Milwaukee", "WI", 53026, "admin")

        self.emmaSonnen.save()

    def test_GetTemplate(self):
        response = self.client.get('/userpage/')
        self.assertTemplateUsed(response, 'userpage.html')

    def test_GetSessionVars(self):
        response = self.client.get('/userpage/')
        self.assertNotIn("selectedCourse", self.client.session,
                         "Session has selected course saved at userpage screen.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section saved at userpage screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when navigating to userpage")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when navigating to userpage")
    def test_PostLogout(self):
        response = self.client.post("/userpage/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/userpage/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/userpage/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/userpage/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostEditUserAdmin(self):
        response = self.client.post("/userpage/", {"navigation": "edituser"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to createuser")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when navigating to useredit")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at createuser.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at createuser.")

    def test_PostEditUserNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selecteduser"] = "writchie@uwm.edu"
        session.save()
        response = self.client.post("/userpage/", {"navigation": "edituser"}, follow=True)
        self.assertTemplateUsed(response, 'userpage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to edit user")
        self.assertEqual(response.context["message"], "Only admins can edit users!",
                         "Message not played if non-admin tries to edit user")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to edit user")
        self.assertEqual(self.client.session["selecteduser"], "writchie@uwm.edu",
                         "selected user not saved when non-admin tries to edit user")
        self.assertNotIn("selectedCourse", self.client.session,
                         "Session has selected course when non-admin tries to edit user.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section when non-admin tries to edit user")

    def test_PostDeleteUserAdmin(self):
        response = self.client.post("/userpage/", {"navigation": "deleteuser"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when deleting user")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at createuser.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at createuser.")

    def test_PostEditUserNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selecteduser"] = "writchie@uwm.edu"
        session.save()
        response = self.client.post("/userpage/", {"navigation": "deleteuser"}, follow=True)
        self.assertTemplateUsed(response, 'userpage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to delete user")
        self.assertEqual(response.context["message"], "Only admins can delete users!",
                         "Message not played if non-admin tries to delete user")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to delete user")
        self.assertEqual(self.client.session["selecteduser"], "writchie@uwm.edu",
                         "selected user not saved when non-admin tries to delete user")
        self.assertNotIn("selectedCourse", self.client.session,
                         "Session has selected course when non-admin tries to delete user.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section when non-admin tries to delete user")