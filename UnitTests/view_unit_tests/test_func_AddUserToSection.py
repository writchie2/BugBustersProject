import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_AddUserToCourse
from django.test import TestCase, Client, RequestFactory

class AddUserToSectionTest(TestCase):

    def setUp(self):
        pass

    def test_AddUserValid(self):
        pass
    def test_AddUserAlreadyIn(self):
        pass

    def test_AddNonExistantUser(self):
        pass

    def test_AddUserNonExistantCourse(self):
        pass

    def test_AddUserNotAdmin(self):
        pass