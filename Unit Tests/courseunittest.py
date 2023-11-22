import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import  MyUser, Course, Section
from SchedulingApp.functions import func_ValidateCourseName, func_ValidateDepartment, func_ValidateCourseNumber, func_ValidateYear
from django.test import TestCase, Client

class ValidateCourseNameTest(TestCase):
    pass

class ValidateDepartment(TestCase):
    pass

class ValidateCourseNumberTest(TestCase):
    pass

class ValidateYearTest(TestCase):
    pass
