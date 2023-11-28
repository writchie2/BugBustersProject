import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class DirectoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.emmaSonnen = MyUser(1,"esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                     "Milwaukee", "WI", 53026, "admin")

        self.emmaSonnen.save()
        self.henryRitchie = MyUser(2,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                       "Milwaukee", "WI", 53026, "admin")

        self.henryRitchie.save()
        self.sarahCramer = MyUser(3,"scramer@uwm.edu", "password", "Sarah", "Cramer", "5555555555", "1234 main st",
                                      "Milwaukee", "WI", 53026, "instructor")

        self.sarahCramer.save()
        self.bobAllen = MyUser(4,"ballen@uwm.edu", "password", "Bob", "Allen", "5555555555", "1234 main st",
                                   "Milwaukee", "WI", 53026, "ta")

        self.bobAllen.save()
    def test_GetTemplate(self):
        response = self.client.get('/directory/')
        self.assertTemplateUsed(response, 'directory.html')

    def test_GetSessionVars(self):
        response = self.client.get('/directory/')
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at dashboard screen.")
        self.assertNotIn("selectedCourse", self.client.session,
                         "Session has selected course saved at dashboard screen.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section saved at dashboard screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
    def test_GetUserList(self):
        response = self.client.get('/directory/')
        userList = response.context["list"]
        self.assertEqual(userList[0].get("lastname"), "Allen", "First alphabetical last name is not Allen")
        self.assertEqual(userList[0].get("fullname"), "Bob Allen", "First alphabetical name is not Bob Allen")
        self.assertEqual(userList[0].get("email"), "ballen@uwm.edu", "First alphabetical email is not ballen@uwm.edu")
        self.assertEqual(userList[0].get("role"), "Ta", "First alphabetical role is not ta")

        self.assertEqual(userList[1].get("lastname"), "Cramer", "First alphabetical last name is not Cramer")
        self.assertEqual(userList[1].get("fullname"), "Sarah Cramer", "First alphabetical name is not Sarah Cramer")
        self.assertEqual(userList[1].get("email"), "scramer@uwm.edu", "First alphabetical email is not scramer@uwm.edu")
        self.assertEqual(userList[1].get("role"), "Instructor", "First alphabetical role is not instructor")

        self.assertEqual(userList[2].get("lastname"), "Ritchie", "First alphabetical last name is not Ritchie")
        self.assertEqual(userList[2].get("fullname"), "Henry Ritchie", "First alphabetical name is not Henry Ritchie")
        self.assertEqual(userList[2].get("email"), "writchie@uwm.edu", "First alphabetical email is not writchie@uwm.edu")
        self.assertEqual(userList[2].get("role"), "Admin", "First alphabetical role is not admin")

        self.assertEqual(userList[3].get("lastname"), "Sonnen", "First alphabetical last name is not Sonnen")
        self.assertEqual(userList[3].get("fullname"), "Emma Sonnen", "First alphabetical name is not Emma Sonnen")
        self.assertEqual(userList[3].get("email"), "esonnen@uwm.edu", "First alphabetical email is not esonnen@uwm.edu")
        self.assertEqual(userList[3].get("role"), "Admin", "First alphabetical role is not admin")

    def test_PostLogout(self):
        response = self.client.post("/directory/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/directory/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/directory/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to directory")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/directory/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at dashboard.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at dashboard.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at dashboard.")

    def test_PostSelectedUser(self):
        response = self.client.post("/directory/", {"selecteduser": "scramer@uwm.edu"}, follow=True)
        self.assertTemplateUsed(response, 'userpage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertEqual(self.client.session["selecteduser"], "scramer@uwm.edu", "Selected user not saved to session")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostCreateUserAdmin(self):
        response = self.client.post("/directory/", {"navigation": "createuser"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to createuser")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to createuser")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at createuser.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at createuser.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at createuser.")

    def test_PostCreateUserNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session.save()
        response = self.client.post("/directory/", {"navigation": "createuser"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(response.context["message"], "Only admins can create users!",
                         "Message not played if non-admin tries to create user")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when navigating to createuser")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at createuser.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at createuser.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at createuser.")

