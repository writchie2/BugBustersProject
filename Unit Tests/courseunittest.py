import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_ValidateCourseName, func_ValidateDepartment, func_ValidateCourseNumber, \
    func_ValidateYear
from django.test import TestCase, Client


class ValidateCourseNameTest(TestCase):
    def testValidCourseName(self):
        pass

    def testInvalidCourseName(self):
        pass


class ValidateDepartmentTest(TestCase):
    def testValidDepartment(self):
        pass

    def testInvalidDepartment(self):
        pass


class ValidateCourseNumberTest(TestCase):
    def testValidCourseNumber(self):
        pass

    def testInvalidCourseNumber(self):
        pass


class ValidateYearTest(TestCase):
    def testValidYear(self):
        pass

    def testInvalidYear(self):
        pass

#Commit test 3.0