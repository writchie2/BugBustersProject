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
        self.swe = Course(1, "Introduction to Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_CreateCourseValid(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": 'Our Physical Geography', "department": 'GEO SCI',
                                     "semester": 'fall', "year": "2023"}, follow=True)
        self.assertTemplateUsed(response, 'createcourse.html')
        self.assertEqual(response.context["message"], "Course created successfully!",
                         "Success message not displayed after course creation")

        newCourse = Course.objects.filter(courseNumber=120).first()
        self.assertNotEqual(None, newCourse, "Course not added to database.")
        self.assertEqual(newCourse.courseNumber, 120, "Course created with incorrect number")
        self.assertEqual(newCourse.name, "Our Physical Geography", "Course created with incorrect name")
        self.assertEqual(newCourse.department, "GEO SCI", "Course created with incorrect department")
        self.assertEqual(newCourse.semester, "fall", "Course created with incorrect semester")
        self.assertEqual(newCourse.year, 2023, "Course created with incorrect year")

    def test_CreateCourseInvalidCourseNumber(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '0', "coursename": 'Our Physical Geography',
                                     "department": 'GEO SCI',
                                     "semester": 'fall', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"], "Invalid Course Number. Must be between 100 and 999 and unique.",
                     "Error message not displayed after course creation failure")
        self.assertEqual(None, Course.objects.filter(courseNumber=0).first(), "Course added to database after invalid creation.")

    def test_CreateCourseInvalidCourseName(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": '0ur Phys1cal Ge0graphy',
                                     "department": 'GEOSCI',
                                     "semester": 'fall', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"], "Invalid Course Name. Only letters and single spaces are allowed.",
                     "Error message not displayed after course creation failure")
        self.assertEqual(None, Course.objects.filter(courseNumber=0).first(), "Course added to database after invalid creation.")

    def test_CreateCourseInvalidDepartment(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": 'Our Physical Geography',
                                     "department": 'geosci',
                                     "semester": 'fall', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"], "Invalid Department. All Departments come from the UWM course cataloge.",
                     "Error message not displayed after course creation failure")
        self.assertEqual(None, Course.objects.filter(courseNumber=0).first(), "Course added to database after invalid creation.")

    def test_CreateCourseInvalidSemester(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": 'Our Physical Geography',
                                     "department": 'GEO SCI',
                                     "semester": 'autumn', "year": "2023"}, follow=True)
        self.assertEqual(response.context["message"], "Invalid semester. Acceptable values are fall, spring, winter, and summer",
                     "Error message not displayed after course creation failure")
        self.assertEqual(None, Course.objects.filter(courseNumber=0).first(), "Course added to database after invalid creation.")

    def test_CreateCourseInvalidYear(self):
        response = self.client.post('/createcourse/',
                                    {"coursenumber": '120', "coursename": 'Our Physical Geography',
                                     "department": 'GEO SCI',
                                     "semester": 'fall', "year": "1940"}, follow=True)
        self.assertEqual(response.context["message"], "Invalid Year. Must be later than 1956 and cannot be greater than 2025",
                     "Error message not displayed after course creation failure")
        self.assertEqual(None, Course.objects.filter(courseNumber=0).first(), "Course added to database after invalid creation.")


class SectionEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        self.swe = Course(1, "Introduction to Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        session["selectedcourse"] = self.swe.id
        session.save()

    def test_EditNameValid(self):
        response = self.client.post('/editcourse/', {"coursename": "Computer Architecture"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.name, "Computer Architecture", "Course Name not edited")
        self.assertEqual(response.context['message'], "Course Name edited successfully!")

    def test_EditNameInvalid(self):
        response = self.client.post('/editcourse/', {"coursename":"Computer 4rchitecture"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.name, "Introduction to Software Engineering", "Course Name edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Course Name. Only letters and single spaces are allowed.")

    def test_EditDepartmentValid(self):
        response = self.client.post('/editcourse/', {"department": "GEO SCI"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.department, "GEO SCI", "Department not edited")
        self.assertEqual(response.context['message'], "Department edited successfully!")

    def test_EditDepartmentInvalid(self):
        response = self.client.post('/editcourse/', {"department": "geosci"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.department, "COMPSCI", "Course Name edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Department. All Departments come from the UWM course cataloge.")

    def test_EditCourseNumberValid(self):
        response = self.client.post('/editcourse/', {"coursenumber": "300"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.courseNumber, 300, "Course Number not edited")
        self.assertEqual(response.context['message'], "Course Number edited successfully!")

    def test_EditCourseNumberInvalid(self):
        response = self.client.post('/editcourse/', {"coursenumber":"22"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.courseNumber, 361, "Course Number edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Course Number. Must be between 100 and 999 and unique.")

    def test_EditSemesterValid(self):
        response = self.client.post('/editcourse/', {"semester": "fall"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.semester, "fall", "Semester not edited")
        self.assertEqual(response.context['message'], "Semester edited successfully!")

    def test_EditSemesterInvalid(self):
        response = self.client.post('/editcourse/', {"semester":"Computer 4rchitecture"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.semester, 'spring', "Semester edited when invalid")
        self.assertEqual(response.context['message'], "Invalid semester. Acceptable values are fall, spring, winter, and summer")

    def test_EditYearValid(self):
        response = self.client.post('/editcourse/', {"year": "2024"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.year, 2024, "Yesr not edited")
        self.assertEqual(response.context['message'], "Year edited successfully!")

    def test_EditYearInvalid(self):
        response = self.client.post('/editcourse/', {"year":"1904"}, follow=True)
        editCourse = Course.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editcourse.html')
        self.assertEqual(editCourse.year, 2023, "Year edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Year. Must be later than 1956 and cannot be greater than 2025")

class CourseDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        self.swe = Course(1, "Introduction to Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section = Section(2, 100, 'lecture', "180 Chemistry BLDG", "TH", "09:30", "10:20", self.swe.id)
        self.section.save()
        session["selectedcourse"] = self.swe.id
        session["selectedsection"] = self.section.id
        session.save()

    def test_DeleteCourseSuccess(self):
        response = self.client.post('/coursepage/', {"navigation": "deletecourse"}, follow=True)
        self.assertTemplateUsed(response,'courselist.html')
        self.assertEqual(Course.objects.filter(id=self.swe.id).first(), None,
                             "Course not deleted from database when valid")
        self.assertEqual(Section.objects.filter(id=self.section.id).first(), None, "Section tied to course not deleted from database when valid")

    def test_DeleteCourseNotAdmin(self):
        session = self.client.session
        session['role'] = 'ta'
        session.save()
        response = self.client.post('/coursepage/', {"navigation": "deletecourse"}, follow=True)
        self.assertTemplateUsed(response,'coursepage.html')
        self.assertEqual(Course.objects.filter(id=self.swe.id).first(), self.swe,
                             "Course is deleted from database when non admin tries to delete")
        self.assertEqual(Section.objects.filter(id=self.section.id).first(), self.section,
                             "Section is deleted from database when non admin tries to delete")
        self.assertEqual(response.context['message'], "Only admins can delete courses!",
                             "Error does not show when non admin tries to delete")
