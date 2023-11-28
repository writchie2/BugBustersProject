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
            courseNumber=000,
            semester="Invalid",
            year=1000,
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

class ValidateCourseNameTest(TestCase):
    def test_Valid(self):
        result = func_ValidateCourseName("Intro To Software Engineering")
        self.assertTrue(result, "Intro To Software Engineering returns False (Invalid).")
        result = func_ValidateCourseName("Computer Architecture")
        self.assertTrue(result, "Computer Architecture returns False (Invalid).")
        result = func_ValidateCourseName("Survey Of College Math")
        self.assertTrue(result, "Survey of College Math returns False (Invalid).")

    def test_Empty(self):
        result = func_ValidateCourseName("")
        self.assertFalse(result, "Empty name returns True (Valid).")

    def test_HasNumbers(self):
        result = func_ValidateCourseName("12 Computer")
        self.assertFalse(result, "Name with only numbers returns True (Valid).")



    def test_IncorrectSpacing(self):
        result = func_ValidateCourseName(" Math 101")
        self.assertFalse(result, "Name with leading space returns True (Valid).")
        result = func_ValidateCourseName("Computer Science ")
        self.assertFalse(result, "Name with trailing space returns True (Valid).")
        result = func_ValidateCourseName("Computers   Yay")
        self.assertFalse(result, "Name with more than one inner space returns True (Valid).")

    def test_invalidArg(self):
        result = func_ValidateCourseName(1)
        self.assertFalse(result, "Name that is a string returns True (Valid).")
        result = func_ValidateCourseName(2.5)
        self.assertFalse(result, "Name number that is a float returns True (Valid).")


class ValidateDepartmentTests(TestCase):
    def test_Valid(self):
        result = func_ValidateDepartment("COMPSCI")
        self.assertTrue(result, "COMPSCI returns False (Invalid).")
        result = func_ValidateDepartment("ANTHRO")
        self.assertTrue(result, "ANTHRO returns False (Invalid).")
        result = func_ValidateDepartment("PHYSICS")
        self.assertTrue(result, "PHYSICS returns False (Invalid).")

    def test_Empty(self):
        result = func_ValidateDepartment("")
        self.assertFalse(result, "Empty department returns True (Valid).")

    def test_HasNumbers(self):
        result = func_ValidateDepartment("12COMPSCI")
        self.assertFalse(result, "Department with numbers returns True (Valid).")
    def test_HasLowerCase(self):
        result = func_ValidateDepartment("compsci")
        self.assertFalse(result, "Department with lowercase letters returns True (Valid).")

    def test_IncorrectSpacing(self):
        result = func_ValidateDepartment(" MATH")
        self.assertFalse(result, "Department with leading space returns True (Valid).")
        result = func_ValidateDepartment("COMPSCI ")
        self.assertFalse(result, "Department with trailing space returns True (Valid).")
        result = func_ValidateDepartment("GEO  SCI")
        self.assertFalse(result, "Department with more than one inner space returns True (Valid).")

    def test_invalidArg(self):
        result = func_ValidateDepartment(1)
        self.assertFalse(result, "Department that is a string returns True (Valid).")
        result = func_ValidateDepartment(2.5)
        self.assertFalse(result, "Department number that is a float returns True (Valid).")

class ValidateCourseNumberTests:
    pass

class ValidateSemesterTests:
    pass
class ValidateYearTests:
    pass
