import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class CreateCourseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()


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

    def test_PostCreateCourseValid(self):
        response = self.client.post("/createcourse/",
                                    {"coursename": "Intro to Software Engineering",
                                     "department": "COMPSCI",
                                     "coursenumber": 361,
                                     "semester": "spring",
                                     "year": 2023,
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Course created successfully!",
                         "Error message not displayed after course creation failure")

    def test_PostCreateCourseInvalidCourseNumber(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '0', "coursename": 'Our Physical Geography',
                                     "department": 'GEO SCI',
                                     "semester": 'fall', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"], "Invalid Course Number. Must be between 100 and 999 and unique.",
                         "Error message not displayed after course creation failure")

    def test_PostCreateCourseInvalidCourseName(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": '0ur Phys1cal Ge0graphy',
                                     "department": 'GEOSCI',
                                     "semester": 'fall', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"],
                         "Invalid Course Name. Only letters and single spaces are allowed.",
                         "Error message not displayed after course creation failure")

    def test_PostCreateCourseInvalidDepartment(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": 'Our Physical Geography',
                                     "department": 'geosci',
                                     "semester": 'fall', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"],
                         "Invalid Department. All Departments come from the UWM course cataloge.",
                         "Error message not displayed after course creation failure")


    def test_PostCreateCourseInvalidSemester(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": 'Our Physical Geography',
                                     "department": 'GEO SCI',
                                     "semester": 'autumn', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"],
                         "Invalid Semester. Acceptable values are fall, spring, winter, and summer",
                         "Error message not displayed after course creation failure")


    def test_PostCreateCourseInvalidYear(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": 'Our Physical Geography',
                                     "department": 'GEO SCI',
                                     "semester": 'fall', "year": "1940"}, follow=True)
        self.assertEqual(response.context["message"],
                         "Invalid Year. Must be later than 1956 and cannot be greater than 2025",
                         "Error message not displayed after course creation failure")