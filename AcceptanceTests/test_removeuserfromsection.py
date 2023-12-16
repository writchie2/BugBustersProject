import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section

from django.test import TestCase, Client, RequestFactory

class RemoveUserFromSectionTest(TestCase):

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session["selectedsection"] = 1
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
        self.section1 = Section(1, 100, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section1.save()
        self.swe.assignedUser.add(self.emma)
        self.swe.save()
        self.section1.assignedUser = self.emma
        self.section1.save()

    def test_RemoveUserFromSectionValid(self):
        response = self.client.post('/sectionpage/', {'removeuser': 'esonnen@uwm.edu'})
        section_response = Section.objects.get(id=1)
        self.assertEqual(section_response.assignedUser, None,
                         "User in section after being removed.")
        self.assertEqual(response.context['message'], "User removed successfully!",
                         "Success message does not play after user is removed.")

    def test_RemoveUserFromSectionDoubleRemove(self):
        response = self.client.post('/sectionpage/', {'removeuser': 'esonnen@uwm.edu'})
        section_response = Section.objects.get(id=1)
        self.assertEqual(section_response.assignedUser, None,
                         "User in section after being removed.")
        self.assertEqual(response.context['message'], "User removed successfully!",
                         "Success message does not play after user is removed.")
        response = self.client.post('/sectionpage/', {'removeuser': 'esonnen@uwm.edu'})
        self.assertEqual(section_response.assignedUser, None,
                      "User not in section after trying to be removed a second time.")
        self.assertEqual(response.context['message'], "User is not assigned to the section!",
                         "Error message does not play after user is removed double removed.")

    def test_RemoveUserNonexistantUser(self):
        response = self.client.post('/sectionpage/', {'removeuser': 'none@uwm.edu'})
        self.assertEqual(self.section1.assignedUser, self.emma,
                         "Nonexistant user removed actual user assigned to section.")
        self.assertEqual(response.context['message'], "User does not exist!",
                         "Error message does not play after removing nonexistant user from section.")

    def test_RemoveUserFromNonExistentSection(self):
        session = self.client.session
        session["selectedsection"] = 5
        session.save()
        response = self.client.post('/sectionpage/', {'removeuser': 'esonnen@uwm.edu'})
        self.assertEqual(response.context['message'], 'Section does not exist!',
                         "User added to nonexistant course.")


    def test_RemoveUserFromSectionAsTA(self):
        self.client = Client()
        session = self.client.session
        session["role"] = "ta"
        session["email"] = "writchie@uwm.edu"
        session["selectedcourse"] = 1
        session['selectedsection'] = 1
        session.save()
        response = self.client.post('/sectionpage/', {'removeuser': 'esonnen@uwm.edu'}, follow=True)
        self.assertEqual(self.emma, self.section1.assignedUser, "User removed from section when non-admin removes.")
        self.assertEqual(response.context['message'], "Only admins or instructors of the course can remove users from sections!",
                         "Error message does not play after non-admin or non-instructor tries to remove user from section.")


    def test_RemoveUserAsInstructorInAnotherCourse(self):
        self.client = Client()
        session = self.client.session
        session["role"] = "instructor"
        session["email"] = "writchie@uwm.edu"
        session["selectedcourse"] = 2
        session['selectedsection'] = 1
        session.save()
        response = self.client.post('/sectionpage/', {'removeuser': 'esonnen@uwm.edu'}, follow=True)
        self.assertEqual(self.emma, self.section1.assignedUser, "User removed from section when non-admin removes.")
        self.assertEqual(response.context['message'], "Only admins or instructors of the course can remove users from sections!",
                         "Error message does not play after non-admin tries to remove user from section.")
