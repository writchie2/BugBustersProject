import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import Course
from SchedulingApp.functions import (
    func_ValidateCourseName,
    func_ValidateDepartment,
    func_ValidateCourseNumber,
    func_ValidateSemester,
    func_ValidateYear
)
from django.test import TestCase


class TestCreateCourse(TestCase):
    def setUp(self):
        self.validCourse = Course(
            name="Test",
            department="Department",
            courseNumber=101,
            semester="Spring",
            year=2024,
        )

        self.invalidCourse = Course(
            name="",
            department="Invalid",
            courseNumber=0,
            semester="Invalid",
            year=0,
        )

    def testCourseName(self):
        validName = func_ValidateCourseName(self.validCourse.name)
        self.assertTrue(validName, f"The name '{self.validCourse.name}' should be considered valid.")
        invalidName = func_ValidateCourseName(self.invalidCourse.name)
        self.assertFalse(invalidName, f"The name '{self.invalidCourse.name}' should be considered invalid.")

    def testDepartment(self):
        validDepartment = func_ValidateDepartment(self.validCourse.department)
        self.assertTrue(validDepartment, f"The department '{self.validCourse.department}' should be considered valid.")
        invalidDepartment = func_ValidateCourseName(self.invalidCourse.department)
        self.assertFalse(invalidDepartment,
                         f"The department '{self.invalidCourse.department}' should be considered invalid.")

    def testCourseNumber(self):
        validCourseNumber = func_ValidateCourseNumber(self.validCourse.courseNumber)
        self.assertTrue(validCourseNumber,
                        f"The course number'{self.validCourse.courseNumber}' should be considered valid.")
        invalidCourseNumber = func_ValidateCourseName(self.invalidCourse.courseNumber)
        self.assertFalse(invalidCourseNumber,
                         f"The course number '{self.invalidCourse.courseNumber}' should be considered invalid.")

    def testSemester(self):
        validSemester = func_ValidateSemester(self.validCourse.semester)
        self.assertTrue(validSemester, f"The semester '{self.validCourse.semester}' should be considered valid.")
        invalidSemester = func_ValidateSemester(self.invalidCourse.semester)
        self.assertFalse(invalidSemester, f"The semester '{self.invalidCourse.semester}' should be considered invalid.")

    def testYear(self):
        validYear = func_ValidateYear(self.validCourse.year)
        self.assertTrue(validYear, f"The year '{self.validCourse.year}' should be considered valid.")
        invalidYear = func_ValidateYear(self.invalidCourse.year)
        self.assertFalse(invalidYear, f"The year '{self.invalidCourse.year}' should be considered invalid.")
