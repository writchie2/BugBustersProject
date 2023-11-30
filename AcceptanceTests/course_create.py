import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class CourseCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()

    def test_GetCourseCreateNonAdmin(self):
        session = self.client.session
        session["email"] = "tballen@uwm.edu"
        session["role"] = "ta"
        session.save()

        response = self.client.get("/createcourse/", follow=True)
        self.assertTemplateUsed(response,'courselist.html', 'Non-admin able to access createcourse')

    def test_CourseCreateValid(self):
        response = self.client.post("/createcourse/",
                                {"coursename": "Intro to Software Engineering",
                                 "department": "COMPSCI",
                                 "coursenumber": 361,
                                 "semester": "spring",
                                 "year": 2023,
                                 }, follow=True)
        newCourse = Course.objects.filter().first()
        self.assertEqual(newCourse.name, "Intro to Software Engineering", "Course saved with wrong name")
        self.assertEqual(newCourse.department, "COMPSCI", "Course saved with wrong department")
        self.assertEqual(newCourse.courseNumber, 361, "Course saved with wrong coursenumber")
        self.assertEqual(newCourse.semester, "spring", "User saved with wrong email")
        self.assertEqual(newCourse.year, 2023, "Course saved with wrong year")
        self.assertTemplateUsed(response, 'createcourse.html')


    def test_CourseCreatedIsDisplayed(self):
        response = self.client.post("/createcourse/",
                                {"coursename": "Intro to Software Engineering",
                                 "department": "COMPSCI",
                                 "coursenumber": 361,
                                 "semester": "spring",
                                 "year": 2023,
                                 }, follow=True)
        response = self.client.get('/courselist', follow=True)
        displayed = any(course['title'] == "COMPSCI 361 Intro to Software Engineering" for course in response.context['list'])
        self.assertTrue(displayed, "New course not displayed in courselist page")

    def test_CourseCreateBlankField(self):
        response = self.client.post("/createcourse/",
                                {
                                 "department": "COMPSCI",
                                 "coursenumber": 361,
                                 "semester": "spring",
                                 "year": 2023,
                                 }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Please fill out all fields!",
                     "Error not played if not all fields filled out")
        self.assertEqual(Course.objects.first(), None, "Course created when invalid")

    def test_CourseCreateInvalidName(self):
        response = self.client.post("/createcourse/",
                                {"coursename": "software engineering",
                                 "department": "COMPSCI",
                                 "coursenumber": 361,
                                 "semester": "spring",
                                 "year": 2023,
                                 }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Invalid Course Name. Only letters and single spaces are allowed.",
                     "Error not played invalid name")
        self.assertEqual(Course.objects.filter(name='software engineering').first(), None,
                         "Course made with invalid name")

    def test_CourseCreateInvalidDepartment(self):
        response = self.client.post("/createcourse/",
                                {"coursename": "Software Engineering",
                                 "department": "COMP SCI",
                                 "coursenumber": 361,
                                 "semester": "spring",
                                 "year": 2023,
                                 }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Invalid Department. All Departments come from the UWM course cataloge.",
                     "Error not played invalid department")
        self.assertEqual(Course.objects.filter(department='COMP SCI').first(), None,
                         "Course made with invalid department")

    def test_CourseCreateInvalidCourseNumber(self):
        response = self.client.post("/createcourse/",
                                {"coursename": "Software Engineering",
                                 "department": "COMPSCI",
                                 "coursenumber": 99,
                                 "semester": "spring",
                                 "year": 2023,
                                 }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Invalid Course Number. Must be between 100 and 999 and unique.",
                     "Error not played if invalid course number")
        self.assertEqual(Course.objects.filter(courseNumber=99).first(), None,
                         "Course made with invalid course number")

    def test_CourseCreateInvalidSemester(self):
        response = self.client.post("/createcourse/",
                                {"coursename": "Software Engineering",
                                 "department": "COMPSCI",
                                 "coursenumber": 200,
                                 "semester": "autumn",
                                 "year": 2023,
                                 }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Invalid Semester. Acceptable values are fall, spring, winter, and summer",
                     "Error not played if invalid semester")
        self.assertEqual(Course.objects.filter(semester='autumn').first(), None,
                         "Course made with invalid semester")

    def test_CourseCreateInvalidYear(self):
        response = self.client.post("/createcourse/",
                                {"coursename": "Software Engineering",
                                 "department": "COMPSCI",
                                 "coursenumber": 200,
                                 "semester": "spring",
                                 "year": 2027,
                                 }, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Invalid Year. Must be later than 1956 and cannot be greater than 2025",
                     "Error not played if invalid year")
        self.assertEqual(Course.objects.filter(year=2027).first(), None,
                         "Course made with invalid year")