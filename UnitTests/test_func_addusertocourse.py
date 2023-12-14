import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class AddUserToCourseTest(TestCase):

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session.save()
        self.emma = MyUser(1, "esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                 "Milwaukee", "WI", '53026', "admin")

        self.emma.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                   "Milwaukee", "WI", '53026', "admin")

        self.henry.save()
        self.sarah = MyUser(3, "scramer@uwm.edu", "password", "Sarah", "Cramer", "5555555555", "1234 main st",
                                  "Milwaukee", "WI", '53026', "admin")

        self.sarah.save()
        self.bob = MyUser(4, "ballen@uwm.edu", "password", "Bob", "Allen", "5555555555", "1234 main st",
                               "Milwaukee", "WI", '53026', "admin")

        self.bob.save()
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.ca = Course(2, "Computer Architecture", "COMPSCI", 451, "spring", 2023)
        self.ca.save()
        self.geo = Course(3, "Our Physical Environment", "GEOG", 120, "spring", 2023)
        self.geo.save()

    def test_AddUserValid(self):
        response = self.client.post('/coursepage/', {'adduser': 'esonnen@uwm.edu'})
        self.assertIn(self.emma, self.swe.assignedUser.all(), "User not added to course.")
        self.assertEqual(response.context['message'], "User added successfully!",
                         "Success message does not play after user is added.")

    def test_AddUserAlreadyIn(self):
        self.swe.assignedUser.add(self.emma)
        response = self.client.post('/coursepage/', {'adduser': 'esonnen@uwm.edu'})
        self.assertIn(self.emma, self.swe.assignedUser.all(),
                      "User not in course after trying to be added a second time.")
        self.assertEqual(response.context['message'], "User is already in the course!",
                         "Error message does not play after user is added double added.")

    def test_AddNonExistantUser(self):
        response = self.client.post('/coursepage/', {'adduser': 'none@uwm.edu'})
        self.assertNotIn(MyUser.objects.filter(email='none@uwm.edu').first(), self.swe.assignedUser.all(),
                      "Nonexistant user added to course.")
        self.assertEqual(response.context['message'], "User does not exist!",
                         "Error message does not play after adding nonexistant user.")

    def test_AddUserNonExistantCourse(self):
        session = self.client.session
        session["selectedcourse"] = 5
        session.save()
        with self.assertRaises(Exception):
            response = self.client.post('/coursepage/', {'adduser': 'esonnen@uwm.edu'})
        self.assertNotIn(self.emma, MyUser.objects.filter(course__id=5),
                         "User added to nonexistant course.")

    def test_AddUserNotAdmin(self):
        self.client = Client()
        session = self.client.session
        session["role"] = "ta"
        session["email"] = "writchie@uwm.edu"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post('/coursepage/', {'adduser': 'esonnen@uwm.edu'}, follow=True)
        self.assertNotIn(self.emma, self.swe.assignedUser.all(), "User added to course when non-admin adds.")
        self.assertEqual(response.context['message'], "Only admins can add users to courses!",
                         "Error message does not play after non-admin tries to add user.")