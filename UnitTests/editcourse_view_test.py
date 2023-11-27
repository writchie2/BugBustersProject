import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory
class EditUserPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session.save()
        self.swe = Course(1, "SWE", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_GetTemplate(self):
        response = self.client.get('/editcourse/')
        self.assertTemplateUsed(response, 'editcourse.html')

    def test_GetSessionVars(self):
        response = self.client.get('/editcourse/')
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user saved at editcourse screen.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section saved at edituser screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to edituser")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when navigating to edituser")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when navigating to editcourse")
    def test_PostLogout(self):
        response = self.client.post("/editcourse/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/editcourse/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/editcourse/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to directory")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/editcourse/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at dashboard.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at dashboard.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at dashboard.")

    def test_PostCancel(self):
        response = self.client.post("/editcourse/", {"navigation": "cancel"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when edit cancel")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at coursepage.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at coursepage.")

    def test_PostEditNameValid(self):
        response = self.client.post("/editcourse/", {"name": "Programming Languages"}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing name")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing name")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing name")
        self.assertEqual(self.swe.name, "Programming Languages",
                         "Name not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Name changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditNameInvalid(self):
        response = self.client.post("/editcourse/", {"name": ""}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing name")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing name")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing name")
        self.assertEqual(self.swe.name, "SWE",
                         "Name edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Name, Please try again.",
                         "error message does not show for unsuccessful edit")
    def test_PostEditDepartmentValid(self):
        response = self.client.post("/editcourse/", {"department": "ENGLISH"}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing department")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing department")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing department")
        self.assertEqual(self.swe.department, "ENGLISH",
                         "Department not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Department changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditDepartmentInvalid(self):
        response = self.client.post("/editcourse/", {"department": ""}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing department")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing department")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing department")
        self.assertEqual(self.swe.department, "COMPSCI",
                         "Department edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Department, Please try again.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditCourseNumberValid(self):
        response = self.client.post("/editcourse/", {"coursenumber": 200}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing coursenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing coursenumber")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing coursenumber")
        self.assertEqual(self.swe.courseNumber, 200,
                         "Course Number not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Course Number changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditCourseNumberInvalid(self):
        response = self.client.post("/editcourse/", {"coursenumber": -100}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing coursenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing coursenumber")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing coursenumber")
        self.assertEqual(self.swe.courseNumber, 361,
                         "Course Number edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Course Number, Please try again.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditSemesterValid(self):
        response = self.client.post("/editcourse/", {"semester": "fall"}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing semester")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing semester")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing semester")
        self.assertEqual(self.swe.semester, 'fall',
                         "Semester not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Semester changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditSemesterInvalid(self):
        response = self.client.post("/editcourse/", {"semester": 'autumn'}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing semester")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing semester")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing semester")
        self.assertEqual(self.swe.semester, "spring",
                         "Semester edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Semester, Please try again.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditYearValid(self):
        response = self.client.post("/editcourse/", {"year": 2024}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing year")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing year")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing year")
        self.assertEqual(self.swe.year, 2024,
                         "Year not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Year changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditYearInvalid(self):
        response = self.client.post("/editcourse/", {"year": -1}, follow=True)
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing year")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing year")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing year")
        self.assertEqual(self.swe.year, 2023,
                         "Year edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Year, Please try again.",
                         "error message does not show for unsuccessful edit")

