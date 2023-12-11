import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class CourseDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
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

    def test_DeleteCourseValid(self):
        response = self.client.post("/coursepage/", {'navigation': 'deletecourse'}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertNotIn(self.swe, Course.objects.all(), "Course not deleted")

        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when deleting course.")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when deleting course.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user when deleting course.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course when deleting course.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section when deleting course.")

    def test_DeletedCourseNotInList(self):
        response = self.client.post("/coursepage/", {'navigation': 'deletecourse'}, follow=True)
        displayed = any(course['title'] == "COMPSCI 361 Intro to Software Engineering" for course in response.context['list'])
        self.assertFalse(displayed, "Course not displayed in courselist page after deletion")

    def test_DeleteCourseNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post("/coursepage/", {"navigation": "deletecourse"}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertIn(self.swe, Course.objects.all(), "Course was deleted")
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
