import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory
class EditCourseTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session.save()
        self.swe = Course(1, "Intro to Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_GetEditCourseNotAdmin(self):
        session = self.client.session
        session["email"] = "tballen@uwm.edu"
        session["role"] = "ta"
        session.save()

        response = self.client.get("/editcourse/", follow=True)
        self.assertTemplateUsed(response, 'courselist.html', 'Non-admin able to access createcourse')

    def test_EditNameValid(self):
        response = self.client.post("/editcourse/", {"coursename": "Programming Languages"}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing name")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing name")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing name")
        self.assertEqual(self.swe.name, "Programming Languages",
                         "Name not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Course Name edited successfully!",
                         "success message does not show for successful edit")

    def test_EditNameInvalid(self):
        response = self.client.post("/editcourse/", {"coursename": ""}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing name")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing name")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing name")
        self.assertEqual(self.swe.name, "Intro to Software Engineering",
                         "Name edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Course Name. Only letters and single spaces are allowed.",
                         "error message does not show for unsuccessful edit")
    def test_EditDepartmentValid(self):
        response = self.client.post("/editcourse/", {"department": "ENGLISH"}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing department")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing department")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing department")
        self.assertEqual(self.swe.department, "ENGLISH",
                         "Department not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Department edited successfully!",
                         "success message does not show for successful edit")

    def test_EditDepartmentInvalid(self):
        response = self.client.post("/editcourse/", {"department": ""}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing department")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing department")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing department")
        self.assertEqual(self.swe.department, "COMPSCI",
                         "Department edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Department. All Departments come from the UWM course cataloge.",
                         "error message does not show for unsuccessful edit")

    def test_EditCourseNumberValid(self):
        response = self.client.post("/editcourse/", {"coursenumber": '200'}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing coursenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing coursenumber")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing coursenumber")
        self.swe = Course.objects.filter(id=1).first()
        self.assertEqual(self.swe.courseNumber, 200,
                         "Course Number not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Course Number edited successfully!",
                         "success message does not show for successful edit")

    def test_EditCourseNumberInvalid(self):
        response = self.client.post("/editcourse/", {"coursenumber": -100}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing coursenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing coursenumber")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing coursenumber")
        self.assertEqual(self.swe.courseNumber, 361,
                         "Course Number edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Course Number. Must be between 100 and 999 and unique.",
                         "error message does not show for unsuccessful edit")

    def test_EditSemesterValid(self):
        response = self.client.post("/editcourse/", {"semester": "fall"}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing semester")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing semester")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing semester")
        self.assertEqual(self.swe.semester, 'fall',
                         "Semester not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Semester edited successfully!",
                         "success message does not show for successful edit")

    def test_EditSemesterInvalid(self):
        response = self.client.post("/editcourse/", {"semester": 'autumn'}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing semester")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing semester")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing semester")
        self.assertEqual(self.swe.semester, "spring",
                         "Semester edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Semester. Acceptable values are fall, spring, winter, and summer",
                         "error message does not show for unsuccessful edit")

    def test_EditYearValid(self):
        response = self.client.post("/editcourse/", {"year": 2024}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing year")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing year")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing year")
        self.assertEqual(self.swe.year, 2024,
                         "Year not edited in editcourse when valid")
        self.assertEqual(response.context["message"], "Year edited successfully!",
                         "success message does not show for successful edit")

    def test_EditYearInvalid(self):
        response = self.client.post("/editcourse/", {"year": -1}, follow=True)
        self.swe = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing year")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing year")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing year")
        self.assertEqual(self.swe.year, 2023,
                         "Year edited in editcourse when invalid")
        self.assertEqual(response.context["message"], "Invalid Year. Must be later than 1956 and cannot be greater than 2025",
                         "error message does not show for unsuccessful edit")

    def test_EditCourseNotAdmin(self):
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

    def test_EditCourseNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.get("/editcourse/", follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to edit course")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to edit course")
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user when non-admin tries to edit course.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section when non-admin tries to edit course")

