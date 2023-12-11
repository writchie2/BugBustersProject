import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_AddUserToCourse
from django.test import TestCase, Client, RequestFactory


class AddUserToSectionTest(TestCase):

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "adminK@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 205
        session["selectedsection"] = 101
        session.save()

        self.chris = MyUser(10, "coropeza@uwm.edu", "password", "Christian", "Oropeza", "1111111111", "1234 main st",
                           "Milwaukee", "WI", '53026', "admin")
        self.chris.save()

        '''
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "2222222222", "1234 main st",
                            "Milwaukee", "WI", '53026', "admin")
        self.henry.save()

        self.ismael = MyUser(3, "iovalle@uwm.edu", "password", "Ismael", "Ovalle", "3333333333", "1234 main st",
                            "Milwaukee", "WI", '53026', "admin")
        self.ismael.save()

        self.aaron = MyUser(4, "aoropeza@uwm.edu", "password", "Aaron", "Oropeza", "4444444444", "1234 main st",
                          "Milwaukee", "WI", '53026', "admin")
        self.aaron.save()
        '''
        self.math = Course(205, "Finite Math", "MATH", 205, "fall", 2023)
        self.math.save()

        self.mathSection1 = Section(101, 101, 'Lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.math.id)
        self.mathSection1.save()

        '''
        self.mathSection2 = Section(2, 201, 'Lab', "EMS 210", "TH", "13:45", "15:30", self.math.id)
        self.mathSection2.save()
        
        self.ca = Course(2, "Computer Architecture", "COMPSCI", 458, "spring", 2024)
        self.ca.save()
        self.ethics = Course(3, "Information Technology Ethics", "INFOST", 120, "spring", 2023)
        self.ethics.save()
        '''

    def test_AddUserValid(self):
        response = self.client.post('/sectionpage/', {'adduser': 'coropeza@uwm.edu'})
        self.assertEqual(self.chris, self.mathSection1.assignedUser, "User not added to section.")
        self.assertEqual(response.context['message'], "User added successfully!",
                         "Success message does not play after user is added.")

    def test_AddUserAlreadyIn(self):
        pass

    def test_AddNonExistentUser(self):
        pass

    def test_AddUserNotAdminOrInstructor(self):
        pass

    def test_instructorNotInCourse(self):
        pass

