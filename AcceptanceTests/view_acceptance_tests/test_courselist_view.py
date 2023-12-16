import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class CourseListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.swe = Course(1,"Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.ca = Course(2,"Computer Architecture", "COMPSCI", 451, "spring", 2023)
        self.ca.save()
        self.geo = Course(3,"Our Physical Environment", "GEOG", 120, "spring", 2023)
        self.geo.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()
    def test_GetTemplate(self):
        response = self.client.get('/courselist/')
        self.assertTemplateUsed(response, 'courselist.html')

    def test_GetSessionVars(self):
        response = self.client.get('/courselist/')
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist screen.")
        self.assertNotIn("selectedCourse", self.client.session,
                         "Session has selected course saved at courselist screen.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section saved at courselist screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
    def test_GetCourseList(self):
        response = self.client.get('/courselist/')
        courseList = response.context["list"]
        self.assertEqual(courseList[0].get("title"), self.swe.__str__(), "Title displayed does not match stored value")
        self.assertEqual(courseList[0].get("id"), self.swe.id, "ID displayed doesn't match stored value ")
        self.assertEqual(courseList[0].get("semester"), self.swe.semester.capitalize(), "Semester displayed doesn't match stored value")
        self.assertEqual(courseList[0].get("year"), self.swe.year, "Year displayed doesn't match stored value")

        self.assertEqual(courseList[1].get("title"), self.ca.__str__(), "Title displayed does not match stored value")
        self.assertEqual(courseList[1].get("id"), self.ca.id, "ID displayed doesn't match stored value ")
        self.assertEqual(courseList[1].get("semester"), self.ca.semester.capitalize(),
                         "Semester displayed doesn't match stored value")
        self.assertEqual(courseList[1].get("year"), self.ca.year, "Year displayed doesn't match stored value")

        self.assertEqual(courseList[2].get("title"), self.geo.__str__(), "Title displayed does not match stored value")
        self.assertEqual(courseList[2].get("id"), self.geo.id, "ID displayed doesn't match stored value ")
        self.assertEqual(courseList[2].get("semester"), self.geo.semester.capitalize(),
                         "Semester displayed doesn't match stored value")
        self.assertEqual(courseList[2].get("year"), self.geo.year, "Year displayed doesn't match stored value")

    def test_PostLogout(self):
        response = self.client.post("/courselist/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/courselist/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/courselist/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to directory")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/courselist/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at dashboard.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at dashboard.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at dashboard.")

    def test_PostSelectedCourse(self):
        response = self.client.post("/courselist/", {"selectedcourse": self.swe.id}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to coursepage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to coursepage")
        self.assertEqual(self.client.session["selectedcourse"], str(self.swe.id), "Selected course not saved to session")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at coursepage.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at coursepage.")

    def test_PostCreateCourseAdmin(self):
        response = self.client.post("/courselist/", {"navigation": "createcourse"}, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to createcourse")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to createcourse")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at createcourse.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at createcourse.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at createcourse.")

    def test_PostCreateCourseNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session.save()
        response = self.client.post("/courselist/", {"navigation": "createcourse"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when navigating to createuser")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at createuser.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at createuser.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at createuser.")
