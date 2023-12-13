import sys

from SchedulingApp.Model_Classes.Course_Functions import func_ValidateCourseName, func_ValidateDepartment, \
    func_ValidateCourseNumber, func_ValidateSemester, func_ValidateYear

sys.path.append('../SchedulingApp')
from SchedulingApp.models import Course

from django.test import TestCase


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


class ValidateCourseNumberTests(TestCase):
    def test_Valid(self):
        result = func_ValidateCourseNumber(101, "AMLLC")
        self.assertTrue(result, "AMLLC 101 returns False (Invalid).")
        result = func_ValidateCourseNumber(458, "BIO SCI")
        self.assertTrue(result, "BIO SCI 458 returns False (Invalid).")
        result = func_ValidateCourseNumber(205, "CELTIC")
        self.assertTrue(result, "CELTIC 205 returns False (Invalid).")

    def test_InvalidTooShort(self):
        result = func_ValidateCourseNumber(99, "DANCE")
        self.assertFalse(result, "DANCE 99 returns True (Valid).")
        result = func_ValidateCourseNumber(13, "ECON")
        self.assertFalse(result, "ECON 13 returns True (Valid).")
        result = func_ValidateCourseNumber(54, "FILM")
        self.assertFalse(result, "FILM 54 returns True (Valid).")

    def test_InvalidTooLong(self):
        result = func_ValidateCourseNumber(1000, "GREEK")
        self.assertFalse(result, "GREEK 1000 returns True (Valid).")
        result = func_ValidateCourseNumber(9999, "HMONG")
        self.assertFalse(result, "HMONG 9999 returns True (Valid).")
        result = func_ValidateCourseNumber(1945, "INFOST")
        self.assertFalse(result, "INFOST 1945 returns True (Valid).")

    def test_InvalidDepartment(self):
        result = func_ValidateCourseNumber(101, "GAMES")
        self.assertFalse(result, "GAMES 101 returns True (Valid).")
        result = func_ValidateCourseNumber(420, "FOOD")
        self.assertFalse(result, "FOOD 420 returns True (Valid).")
        result = func_ValidateCourseNumber(182, "PYTHON")
        self.assertFalse(result, "PYTHON 182 returns True (Valid).")

    def test_InvalidNonNumericValue(self):
        invalid_test_cases = [
            ("A101", "JAMS"),
            ("101A", "KOREAN"),
            ("10A1", "LACUSL"),
        ]
        for courseNumber, department in invalid_test_cases:
            with self.subTest(course_number=courseNumber, department=department):
                result = func_ValidateCourseNumber(courseNumber, department)
                self.assertFalse(result,
                                 f"{department} {courseNumber} returns True (Valid).")

    def test_InvalidParameters(self):
        invalid_test_cases = [
            (91, "SCI"),
            (1023, "THEOREMS"),
            ("1O0", "MKE"),
        ]
        for courseNumber, department in invalid_test_cases:
            with self.subTest(course_number=courseNumber, department=department):
                result = func_ValidateCourseNumber(courseNumber, department)
                self.assertFalse(result,
                                 f"{department} {courseNumber} returns True (Valid).")


class ValidateSemesterTests(TestCase):
    def test_Valid(self):
        valid_semesters = ["spring", "summer", "fall", "winter"]
        for semester in valid_semesters:
            with self.subTest(semester=semester):
                result = func_ValidateSemester(semester)
                self.assertTrue(result, f"{semester} should be considered a valid semester.")

    def test_InvalidEmpty(self):
        result = func_ValidateSemester("")
        self.assertFalse(result, "Empty semester returns True (Valid).")

    def test_InvalidNonexistent(self):
        result = func_ValidateSemester("Autumn")
        self.assertFalse(result, "Autumn returns True (Valid).")
        result = func_ValidateSemester("Break")
        self.assertFalse(result, "Break returns True (Valid).")

    def test_InvalidInvalidSpacing(self):
        result = func_ValidateSemester(" Fall")
        self.assertFalse(result, "Semester with leading space returns True (Valid).")
        result = func_ValidateSemester("Spring ")
        self.assertFalse(result, "Semester with trailing space returns True (Valid).")
        result = func_ValidateSemester("Summer   ")
        self.assertFalse(result, "Semester with more than one inner space returns True (Valid).")

    def test_invalidArg(self):
        result = func_ValidateSemester(1)
        self.assertFalse(result, "Integer as an argument returns True (Valid).")
        result = func_ValidateSemester(2.5)
        self.assertFalse(result, "Float as an argument returns True (Valid).")


class ValidateYearTests(TestCase):
    def test_Valid(self):
        self.assertTrue(func_ValidateYear(1957), "1956 should be considered a valid year.")
        self.assertTrue(func_ValidateYear(2000), "2000 should be considered a valid year.")
        self.assertTrue(func_ValidateYear(2025), "2025 should be considered a valid year.")

    def test_OutOfRange(self):
        self.assertFalse(func_ValidateYear(1956), "1955 should be considered an invalid year.")
        self.assertFalse(func_ValidateYear(2026), "2026 should be considered an invalid year.")
        self.assertFalse(func_ValidateYear(3000), "3000 should be considered an invalid year.")

    def test_InvalidType(self):
        self.assertFalse(func_ValidateYear("abc"), "String 'abc' should be considered invalid.")
        self.assertFalse(func_ValidateYear(2000.5), "Float 2000.5 should be considered invalid.")
        self.assertFalse(func_ValidateYear(True), "Boolean True should be considered invalid.")
