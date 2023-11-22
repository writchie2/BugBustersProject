import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import  MyUser, Course, Section
from SchedulingApp.functions import func_Logout
from django.test import TestCase, Client

class LogoutTest(TestCase):
    pass