import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import  MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client

class LoginTest(TestCase):
    pass