import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory


class AddUserToSectionTest(TestCase):

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "adminK@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 205
        session["selectedsection"] = 1
        session.save()

        self.chris = MyUser(10, "coropeza@uwm.edu", "password", "Christian", "Oropeza", "1111111111", "1234 main st",
                           "Milwaukee", "WI", '53026', "instructor")
        self.chris.save()


        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "2222222222", "1234 main st",
                            "Milwaukee", "WI", '53026', "instructor")
        self.henry.save()

        self.ismael = MyUser(3, "iovalle@uwm.edu", "password", "Ismael", "Ovalle", "3333333333", "1234 main st",
                            "Milwaukee", "WI", '53026', "ta")
        self.ismael.save()

        self.aaron = MyUser(4, "aoropeza@uwm.edu", "password", "Aaron", "Oropeza", "4444444444", "1234 main st",
                          "Milwaukee", "WI", '53026', "ta")
        self.aaron.save()

        self.math = Course(205, "Finite Math", "MATH", 205, "fall", 2023)
        self.math.save()
        self.math.assignedUser.add(self.henry, self.aaron, self.ismael)

        self.mathSection1 = Section(1, 101, 'Lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.math.id)
        self.mathSection1.save()

        self.mathSection2 = Section(2, 201, 'Lab', "EMS 210", "TH", "13:45", "15:30", self.math.id)
        self.mathSection2.save()
        self.mathSection2.assignedUser = self.aaron
        self.mathSection2.save()


    def test_AddUserAdmin(self):
        response = self.client.post('/sectionpage/', {'adduser': 'writchie@uwm.edu'},follow=True)
        section = Section.objects.get(id=1)
        self.assertEqual(self.henry, section.assignedUser, "User not added to section.")
        self.assertEqual(response.context['message'], "User added successfully!",
                         "Success message does not play after user is added.")

    def test_AddUserInstructorOfCourse(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "instructor"
        session["selectedcourse"] = 205
        session["selectedsection"] = 1
        session.save()
        response = self.client.post('/sectionpage/', {'adduser': 'aoropeza@uwm.edu'},follow=True)
        section = Section.objects.get(id=1)
        self.assertEqual(self.aaron, section.assignedUser, "User not added to section.")
        self.assertEqual(response.context['message'], "User added successfully!",
                         "Success message does not play after user is added.")

    def test_AddUserAlreadyIn(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "adminK@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 205
        session["selectedsection"] = 2
        session.save()
        response = self.client.post('/sectionpage/', {'adduser': 'aoropeza@uwm.edu'}, follow=True)
        section = Section.objects.get(id=2)
        self.assertEqual(self.aaron, section.assignedUser, "User removed even if they are double added.")
        self.assertEqual(response.context['message'], "User is already assigned to the section!",
                         "Error message does not play after user is double added.")

    def test_AddNonExistentUser(self):
        response = self.client.post('/sectionpage/', {'adduser': 'nope@uwm.edu'}, follow=True)
        section = Section.objects.get(id=1)
        self.assertEqual(None, section.assignedUser, "A user is added to the section when the user does not exist")
        self.assertEqual(response.context['message'], "User does not exist!",
                         "Error message does not play after non-existant user is added.")

    def test_AddUserOtherUserAlreadyIn(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "adminK@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 205
        session["selectedsection"] = 2
        session.save()
        response = self.client.post('/sectionpage/', {'adduser': 'iovalle@uwm.edu'}, follow=True)
        section = Section.objects.get(id=2)
        self.assertEqual(self.aaron, section.assignedUser, "User removed even when trying to assign to someone else.")
        self.assertEqual(response.context['message'], "There is already someone assigned to the section!",
                         "Error message does not play after user is double added.")

    def test_AddUserNotInCourse(self):
        response = self.client.post('/sectionpage/', {'adduser': 'coropeza@uwm.edu'},follow=True)
        section = Section.objects.get(id=1)
        self.assertEqual(None, section.assignedUser, "User is added to section when they are not in the course.")
        self.assertEqual(response.context['message'], "That user is not in this course!",
                         "Error message does not play when user that is not in the course is added.")

    def test_AddUserTA(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "adminK@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 205
        session["selectedsection"] = 1
        session.save()
        response = self.client.post('/sectionpage/', {'adduser': 'iovalle@uwm.edu'}, follow=True)
        section = Section.objects.get(id=1)
        self.assertEqual(None, section.assignedUser, "User added to section when ta adds to section.")
        self.assertEqual(response.context['message'], "Only admins or instructors of the course can add users to sections!",
                         "Success message does not play after user is added.")

    def test_InstructorButNotInCourse(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "coropeza@uwm.edu"
        session["role"] = "instructor"
        session["selectedcourse"] = 205
        session["selectedsection"] = 1
        session.save()
        response = self.client.post('/sectionpage/', {'adduser': 'iovalle@uwm.edu'}, follow=True)
        section = Section.objects.get(id=1)
        self.assertEqual(None, section.assignedUser, "User added to section when ta adds to section.")
        self.assertEqual(response.context['message'],
                         "Only admins or instructors of the course can add users to sections!",
                         "Success message does not play after user is added.")

