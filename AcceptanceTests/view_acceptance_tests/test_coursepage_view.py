import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class CoursePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session.save()
        self.swe = Course(1, "SWE", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()
        self.emma = MyUser(2, "esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                           "Milwaukee", "WI", '53026', "admin")
        self.emma.save()
        self.swe.assignedUser.add(self.emma)
        self.swe.save()



    def test_GetTemplate(self):
        response = self.client.get('/coursepage/')
        self.assertTemplateUsed(response, 'coursepage.html')

    def test_GetSessionVars(self):
        response = self.client.get('/coursepage/')
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user saved at coursepage screen.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section saved at coursepage screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to coursepage")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when navigating to coursepage")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected user not saved when navigating to coursepage")
    def test_PostLogout(self):
        response = self.client.post("/coursepage/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/coursepage/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/coursepage/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/coursepage/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at dashboard.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at dashboard.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at dashboard.")

    def test_PostEditCourseAdmin(self):
        response = self.client.post("/coursepage/", {"navigation": "editcourse"}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to editcourse")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when navigating to editcourse")
        self.assertNotIn("selecteduse", self.client.session, "Session has selected course saved at editcourse.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at editcourse.")

    def test_PostEditCourseNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post("/coursepage/", {"navigation": "editcourse"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to edit course")
        self.assertEqual(response.context["message"], "Only admins can edit courses!",
                         "Message not played if non-admin tries to edit user")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to edit course")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected user not saved when non-admin tries to edit course")
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user when non-admin tries to edit course.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section when non-admin tries to edit course")

    def test_PostDeleteCourseAdmin(self):
        response = self.client.post("/coursepage/", {"navigation": "deletecourse"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when deleting course")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDeleteCourseNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post("/coursepage/", {"navigation": "deletecourse"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to delete course")
        self.assertEqual(response.context["message"], "Only admins can delete courses!",
                         "Message not played if non-admin tries to delete course")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to delete course")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when non-admin tries to delete course")
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user when non-admin tries to delete course.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section when non-admin tries to delete course")

    def test_PostCreateSectionAdmin(self):
        response = self.client.post("/coursepage/", {"navigation": "createsection"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to createsection")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to createsection")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when navigating to createsection")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at createsection.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at createsection.")

    def test_PostCreateSectionNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post("/coursepage/", {"navigation": "createsection"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to create section")
        self.assertEqual(response.context["message"], "Only admins can create sections!",
                         "Message not played if non-admin tries to create section")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to create section")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when non-admin tries to create section")
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user when non-admin tries to create section.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section when non-admin tries to create section")

    def test_PostAddUserAdmin(self):
        response = self.client.post("/coursepage/", {"adduser": "writchie@uwm.edu"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when adding user")
        self.assertEqual(response.context['message'], "User added successfully!",
                         "Success message does not play on user ass")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when adding user")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected user not saved when adding user")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected course saved when  adding user.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved when adding user.")

    def test_PostAddUserNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post("/coursepage/", {"adduser": "writchie@uwm.edu"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when nonadmin tries to add user")
        self.assertEqual(response.context['message'], "Only admins can add users to courses!",
                         "Error message does not play when nonadmin tries to add user")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when when nonadmin tries to add user")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected user not saved when when nonadmin tries to add user")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected course when nonadmin tries to add user.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved when nonadmin tries to add user.")

    def test_PostRemoveUserAdmin(self):
        response = self.client.post("/coursepage/", {"removeuser": "esonnen@uwm.edu"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when removing user")
        self.assertEqual(response.context['message'], "User removed successfully!",
                         "Success message does not play on user removed")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when removing user")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected user not saved when removing user")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected course when removing user.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved when removing user.")

    def test_PostRemoveUserNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post("/coursepage/", {"removeuser": "esonnen@uwm.edu"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when nonadmin tries to remove user")
        self.assertEqual(response.context['message'], "Only admins can remove users from courses!",
                         "Error message does not play when nonadmin tries to remove user")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when nonadmin tries to remove user")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected user not saved when nonadmin tries to remove user")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected course when nonadmin tries to remove user.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section when nonadmin tries to remove user.")

