import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class SectionPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session["selectedsection"] = 1
        session.save()
        self.swe = Course(1, "SWE", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section = Section(1, 100, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()

    def test_GetTemplate(self):
        response = self.client.get('/sectionpage/')
        self.assertTemplateUsed(response, 'sectionpage.html')

    def test_GetSessionVars(self):
        response = self.client.get('/sectionpage/')
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user saved at sectionpage screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when navigating to userpage")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when navigating to sectionpage")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when navigating to sectionpage")
    def test_PostLogout(self):
        response = self.client.post("/sectionpage/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/sectionpage/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/sectionpage/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/sectionpage/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at dashboard.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at dashboard.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at dashboard.")

    def test_PostEditSectionAdmin(self):
        response = self.client.post("/sectionpage/", {"navigation": "editsection"}, follow=True)
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to editsection")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to editsection")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when navigating to editsection")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when navigating to editsection")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at editsection.")

    def test_PostEditSectionNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session["selectedsection"] = 1
        session.save()
        response = self.client.post("/sectionpage/", {"navigation": "editsection"}, follow=True)
        self.assertTemplateUsed(response, 'sectionpage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to edit user")
        self.assertEqual(response.context["message"], "Only admins can edit sections!",
                         "Message not played if non-admin tries to edit section")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to edit section")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when non-admin tries to edit section")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when non-admin tries to edit section")
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user when non-admin tries to edit section.")


    def test_PostDeleteSectionAdmin(self):
        response = self.client.post("/sectionpage/", {"navigation": "deletesection"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when deleting section")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at coursepage.")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when deleting section")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section after deleting a section.")

    def test_PostDeleteSectionNotAdmin(self):
        session = self.client.session
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session["selectedsection"] = 1
        session.save()
        response = self.client.post("/sectionpage/", {"navigation": "deletesection"}, follow=True)
        self.assertTemplateUsed(response, 'sectionpage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to delete section")
        self.assertEqual(response.context["message"], "Only admins can delete sections!",
                         "Message not played if non-admin tries to delete user")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to delete section")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when non-admin tries to delete section")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when non-admin tries to delete section")
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user when non-admin tries to delete section.")