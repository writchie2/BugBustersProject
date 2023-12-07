import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_AddUserToCourse
from django.test import TestCase, Client, RequestFactory


class AddUserToCourseTest(TestCase):

    def setUp(self):
        self.client = Client()
        session = self.client.session

    def test_AddUserValid(self):
        pass

    def test_AddUserAlreadyIn(self):
        pass

    def test_AddNonExistentUser(self):
        pass

    def test_AddUserNonExistentSection(self):
        pass

    def test_AddUserNotAdmin(self):
        pass

    def test_SectionNotInCourse(self):
        pass
