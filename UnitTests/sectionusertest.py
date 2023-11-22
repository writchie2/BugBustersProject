import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_ValidateSectionNumber, func_ValidateLocation, func_ValidateDaysMeeting, func_ValidateStartAndEndTime
from django.test import TestCase, Client

class ValidateSectionNumberTest(TestCase):
    def setUp(self):
        self.newCourse = Course("Test", "Department", 100, "sp", 2023)
        self.newSection = Section(200, "se", "1020 Kenwood", "M", "15:00", "16:00", self.newCourse)
    def test_ValidNumber(self):
        result = func_ValidateSectionNumber(100)
        self.assertTrue(result, "Section number of 100 returns False (Invalid).")
        result = func_ValidateSectionNumber(1)
        self.assertTrue(result, "Section number of 1 returns False (Invalid).")
        result = func_ValidateSectionNumber(999)
        self.assertTrue(result, "Section number of 999 returns False (Invalid).")
    def test_NonUnique(self):
        result = func_ValidateSectionNumber(200)
        self.assertFalse(result, "Section number that is not unique returns True (Valid).")
    def test_Zero(self):
        result = func_ValidateSectionNumber(0)
        self.assertFalse(result, "Section number of 0 returns True (Valid).")
    def test_Negative(self):
        result = func_ValidateSectionNumber(-1)
        self.assertFalse(result, "Section number of -1 returns True (Valid).")
    def test_TenThousand(self):
        result = func_ValidateSectionNumber(10000)
        self.assertFalse(result, "Section number of 10000 returns True (Valid).")
    def test_invalidArg(self):
        with self.assertRaises(TypeError, msg="Non-Integer input does not raise TypeError."):
            result = func_ValidateSectionNumber("Bob")
            result = func_ValidateSectionNumber(2.5)

class ValidateLocationTest(TestCase):
    def test_Valid(self):
        result = func_ValidateLocation("1234 Kenwood")
        self.assertTrue(result, "1234 Kenwood returns False (Invalid).")
        result = func_ValidateLocation("1234 Architecture & Urban Planning")
        self.assertTrue(result, "1234 Architecture & Urban Planning returns False (Invalid).")
        result = func_ValidateLocation("Online")
        self.assertTrue(result, "Online returns False (Invalid).")
    def test_Empty(self):
        result = func_ValidateLocation("")
        self.assertFalse(result, "Empty Location returns True (Valid).")
    def test_OnlyNumbers(self):
        result = func_ValidateLocation("1234")
        self.assertFalse(result, "Location with only numbers returns True (Valid).")
    def test_NoNumbersNotOnline(self):
        result = func_ValidateLocation("Kenwood")
        self.assertFalse(result, "Location with no numbers returns True (Valid).")
    def test_IncorrectSpacing(self):
        result = func_ValidateLocation(" 1234 Kenwood")
        self.assertFalse(result, "Location with leading space returns True (Valid).")
        result = func_ValidateLocation("1234 Kenwood ")
        self.assertFalse(result, "Location with trailing space returns True (Valid).")
        result = func_ValidateLocation("1234  Kenwood")
        self.assertFalse(result, "Location with more than one inner space returns True (Valid).")

    def test_invalidArg(self):
        with self.assertRaises(TypeError, msg="Non-String input does not raise TypeError."):
            result = func_ValidateSectionNumber(1)
            result = func_ValidateSectionNumber(2.5)


class ValidateDaysMeetingTest(TestCase):
    def test_Valid(self):
        result = func_ValidateDaysMeeting("MW")
        self.assertTrue(result, "MW returns False (Invalid).")
        result = func_ValidateDaysMeeting("MWF")
        self.assertTrue(result, "MWF returns False (Invalid).")
        result = func_ValidateDaysMeeting("No Meeting Pattern")
        self.assertTrue(result, "MWF returns False (Invalid).")
    def test_OutOfOrder(self):
        result = func_ValidateDaysMeeting("WM")
        self.assertFalse(result, "WM returns True (Valid).")
        result = func_ValidateDaysMeeting("HT")
        self.assertFalse(result, "HT returns True (Valid).")
    def testEmpty(self):
        result = func_ValidateDaysMeeting("")
        self.assertFalse(result, "Empty input returns True (Valid).")
    def testMeetingDayAndAsync(self):
        result = func_ValidateDaysMeeting("MNo Meeting Pattern")
        self.assertFalse(result, "M and No Meeting Pattern returns True (Valid).")
    def test_invalidArg(self):
        with self.assertRaises(TypeError, msg="Non-String input does not raise TypeError."):
            result = func_ValidateDaysMeeting(1)
            result = func_ValidateDaysMeeting(2.5)


class ValidateStartAndEndTimeTest(TestCase):
    def test_Valid(self):
        result = func_ValidateStartAndEndTime("08:00", "08:50")
        self.assertTrue(result, "08:00-08:50 returns False (inValid).")
        result = func_ValidateStartAndEndTime("17:30", "19:20")
        self.assertTrue(result, "17:30-19:20 returns False (inValid).")
        result = func_ValidateStartAndEndTime("13:", "14:15")
        self.assertTrue(result, "08:00-08:50 returns False (inValid).")
    def test_EndBeforeStart(self):
        result = func_ValidateStartAndEndTime("16:00","15:00")
        self.assertFalse(result, "End Time Before Start Time returns True (Valid).")
    def test_StartBeforeEightAM(self):
        result = func_ValidateStartAndEndTime("07:55","09:00")
        self.assertFalse(result, "Start Time Before 8 returns True (Valid).")
    def test_StartSixPMOrLater(self):
        result = func_ValidateStartAndEndTime("18:00","19:00")
        self.assertFalse(result, "Start Time at 18:00 returns True (Valid).")
    def test_StartEqualsEnd(self):
        result = func_ValidateStartAndEndTime("09:00","09:00")
        self.assertFalse(result, "Equal Start and End Time returns True (Valid).")
    def test_EndEightPMorLater(self):
        result = func_ValidateStartAndEndTime("17:30", "20:00")
        self.assertFalse(result, "End Time at 20:00 returns True (Valid).")
    def test_invalidArg(self):
        with self.assertRaises(TypeError, msg="Non-String input does not raise TypeError."):
            result = func_ValidateStartAndEndTime(1,2)
            result = func_ValidateStartAndEndTime(1.0,2.0)
