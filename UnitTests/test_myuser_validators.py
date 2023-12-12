import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.Model_Classes.MyUser_Functions import (
    func_ValidateEmail,
    func_ValidatePassword,
    func_ValidateFirstName,
    func_ValidateLastName,
    func_ValidatePhoneNumber,
    func_ValidateStreetAddress,
    func_ValidateCity,
    func_ValidateState,
    func_ValidateZipCode,
    func_ValidateRole
)
from django.test import TestCase, Client


class ValidateEmailTest(TestCase):
    invalid_emails = ["invalid_email", "user@edu", "user@.edu", "a",
                      "user.edu", "@uwm.edu", "person 1@uwm.edu",
                      ".person@uwm.edu", "per..son@uwm.edu"]

    invalid_whitespace = [" user@uwm.edu", "user@uwm.edu ", " user@uwm.edu "]

    long_email = "aaaaaaaaaaaaaaaaa" + "@uwm.edu"

    valid_email = ["email@uwm.edu", "person2@uwm.edu", "some_body@uwm.edu"]

    def test_no_email(self):
        self.assertFalse(func_ValidateEmail(""), "Expected: False Actual: True")

    def test_empty_email(self):
        self.assertFalse(func_ValidateEmail(" "), "Expected: False Actual: True")

    def test_valid_email(self):
        for email in self.valid_email:
            self.assertTrue(func_ValidateEmail(email), "Expected: True Actual: False")

    def test_invalid_formats(self):
        for email in self.invalid_emails:
            result = bool(self.assertFalse(func_ValidateEmail(email), "Expected: False Actual: True"))

    def test_long_email(self):
        self.assertFalse(func_ValidateEmail(self.long_email), "Expected: False Actual: True")

    def test_whitespace(self):
        for email in self.invalid_whitespace:
            self.assertFalse(func_ValidateEmail(email), "Expected: False Actual: True")


class ValidatePasswordTest(TestCase):
    invalid_password = ["12345678", "password!2", "a", "abcd"]
    valid_password = ["P@assword2", "aN0ther_password", "g00d!pAss"]
    almost_matching = ["P@assword", "an0ther_password", "gO0d!pASs"]
    long_password = "L0ng#Passworddddddddd"

    def test_no_password(self):
        self.assertFalse(func_ValidatePassword("", ""), "Expected: False Actual: True")

    def test_empty_password(self):
        self.assertFalse(func_ValidatePassword(" ", " "), "Expected: False Actual: True")

    def test_invalid_password(self):
        for password in self.invalid_password:
            self.assertFalse(func_ValidatePassword(password, password), "Expected: False Actual: True")

    def test_valid_password(self):
        for password in self.valid_password:
            self.assertTrue(func_ValidatePassword(password, password), "Expected: True Actual: False")

    def test_mismatching_password(self):
        for password1, password2 in zip(self.valid_password, self.almost_matching):
            self.assertFalse(func_ValidatePassword(password1, password2), "Expected: False Actual True")

    def test_long_password(self):
        self.assertFalse(func_ValidatePassword(self.long_password, self.long_password), "Expected: False Actual: True")


class ValidateFirstNameTest(TestCase):
    invalid_names = ["a", "@d@m", "P3n3lop3", "R!ley", "Jak3"]
    long_name = "A" * 21
    valid_names = ["Adam", "Penelope", "Riley", "Jackson", "Aaaaaaaaaaaaaaaaaaaa",
                   "McDonald", "Edwards"]

    def test_no_name(self):
        self.assertFalse(func_ValidateFirstName(""), "Expected: False Actual: True")

    def test_empty_name(self):
        self.assertFalse(func_ValidateFirstName(" "), "Expected: False Actual: True")

    def test_valid_name(self):
        for name in self.valid_names:
            self.assertTrue(func_ValidateFirstName(name), "Expected: True Actual: False")

    def test_invalid_names(self):
        for name in self.invalid_names:
            self.assertFalse(func_ValidateFirstName(name), "Expected: False Actual: True")

    def test_long_name(self):
        self.assertFalse(func_ValidateFirstName(self.long_name), "Expected: False Actual: True")


class ValidateLastNameTest(TestCase):
    invalid_names = ["a", "@d@m", "P3n3lop3", "R!ley", "Jak3"]
    long_name = "A" * 21
    valid_names = ["Adam", "Penelope", "Riley", "Jackson", "Aaaaaaaaaaaaaaaaaaaa",
                   "McDonald", "Edwards"]

    def test_no_name(self):
        self.assertFalse(func_ValidateLastName(""), "Expected: False Actual: True")

    def test_empty_name(self):
        self.assertFalse(func_ValidateLastName(" "), "Expected: False Actual: True")

    def test_valid_name(self):
        for name in self.valid_names:
            self.assertTrue(func_ValidateLastName(name), "Expected: True Actual: False")

    def test_invalid_names(self):
        for name in self.invalid_names:
            self.assertFalse(func_ValidateLastName(name), "Expected: False Actual: True"+name)

    def test_long_name(self):
        self.assertFalse(func_ValidateLastName(self.long_name), "Expected: False Actual: True")


class ValidatePhoneNumberTest(TestCase):
    valid_phone_numbers = ["414-123-4567", "(414)123-4567",
                           "4141234567", "(414)1234567"]

    invalid_phone_numbers = ["414-123-456", "123-4567",
                             "1", "(414)", "1234",
                             "(414)12E-4567", "414-123-$567",
                             "414 123 4567"]

    invalid_whitespace = [" (414)123-4567", "(414)123-4567 ", " (414)123-4567 "]

    long_number = 123456789012345678901

    def test_no_number(self):
        self.assertFalse(func_ValidatePhoneNumber(""), "Expected: False Actual: True")

    def test_empty_number(self):
        self.assertFalse(func_ValidatePhoneNumber(" "), "Expected: False Actual: True")

    def test_valid_numbers(self):
        for number in self.valid_phone_numbers:
            self.assertTrue(func_ValidatePhoneNumber(number), "Expected: True Actual: False")

    def test_invalid_numbers(self):
        for number in self.invalid_phone_numbers:
            self.assertFalse(func_ValidatePhoneNumber(number), "Expected: False Actual: True")

    def test_long_number(self):
        self.assertFalse(func_ValidateState(self.long_number), "Expected: False Actual: True")

    def test_whitespace(self):
        for number in self.invalid_whitespace:
            self.assertFalse(func_ValidatePhoneNumber(number), "Expected: False Actual: True")


class ValidateStreetAddressTest(TestCase):
    valid_street = ["1234 S Main Street", "1234 E Main St",
                    "1234 W Main Street", "1234 N Main St",
                    "1234 Main Street", "1234 Main St",
                    "1234 S Rio Grande Avenue"]

    invalid_street = ["1st St", "South University st",
                      "1234 Avenue",
                      "5678 South", "North Ave",
                      "!2E4 East Washington Ave"]


    def test_no_address(self):
        self.assertFalse(func_ValidateStreetAddress(""), "Expected: False Actual: True")

    def test_empty_address(self):
        self.assertFalse(func_ValidateStreetAddress(" "), "Expected: False Actual: True")

    def test_valid_address(self):
        for address in self.valid_street:
            self.assertTrue(func_ValidateStreetAddress(address), "Expected: True Actual: False "+address)

    def test_invalid_address(self):
        for address in self.invalid_street:
            result = bool(self.assertFalse(func_ValidateStreetAddress(address), "Expected: False Actual: True"+address))




class ValidateCityTest(TestCase):
    valid_city = ["Milwaukee", "Los Angeles", "Cleveland", "Orlando",
                  "Houston", "Seattle", "San Juan", "Chicago", "Mundelein",
                  "Miami", "San Francisco", "Phoenix", "Ponce de Leon",
                  "San Diego", "Puerto Penasco"]

    invalid_city = ["a", "L0s Ang3l3s", "Ch!c@go", "appleton"]

    long_city = "AAAAAAAAAAAAAAAAAAAAAAAAAA"

    def test_no_city(self):
        self.assertFalse(func_ValidateCity(""), "Expected: False Actual: True")

    def test_empty_city(self):
        self.assertFalse(func_ValidateCity(" "), "Expected: False Actual: True")

    def test_valid_city(self):
        for city in self.valid_city:
            self.assertTrue(func_ValidateCity(city), "Expected: True Actual: False")

    def test_invalid_city(self):
        for city in self.invalid_city:
            self.assertFalse(func_ValidateCity(city), "Expected: False Actual: True")

    def test_long_city(self):
        self.assertFalse(func_ValidateCity(self.long_city), "Expected: False Actual: True")


class ValidateStateTest(TestCase):
    valid_state = ["AL", "AK", "AZ", "AR",
                   "CA", "CO", "CT", "DC",
                   "DE", "FL", "GA", "HI",
                   "ID", "IL", "IN", "IA",
                   "KS", "KY", "LA", "ME",
                   "MD", "MA", "MI", "MN",
                   "MS", "MO", "MT", "NE",
                   "NV", "NH", "NJ", "NM",
                   "NY", "NC", "ND", "OH",
                   "OK", "OR", "PA", "RI",
                   "SC", "SD", "TN", "TX",
                   "UT", "VT", "VA", "WA",
                   "WV", "WI", "WY"]

    invalid_state = ["Wisconsin", "Wi", "i",
                     "IDWICA"]

    invalid_whitespace = [" WI", "WI ", " WI "]

    def test_no_state(self):
        self.assertFalse(func_ValidateState(""), "Expected: False Actual: True")

    def test_empty_state(self):
        self.assertFalse(func_ValidateState(" "), "Expected: False Actual: True")

    def test_valid_state(self):
        for state in self.valid_state:
            self.assertTrue(func_ValidateState(state), "Expected: True Actual: False")

    def test_invalid_state(self):
        for state in self.invalid_state:
            self.assertFalse(func_ValidateState(state), "Expected: False Actual: True")


class ValidateZipCodeTest(TestCase):
    valid_zip = ['53206', '12345', '53220']
    invalid_zip = ['53', '2', '-53220']

    def test_no_zip(self):
        self.assertFalse(func_ValidateZipCode(0), "Expected: False Actual: True")

    def test_valid_zip(self):
        for zip_code in self.valid_zip:
            self.assertTrue(func_ValidateZipCode(zip_code), "Expected: True Actual: False")

    def test_invalid_zip(self):
        for zip_code in self.invalid_zip:
            self.assertFalse(func_ValidateZipCode(zip_code), "Expected: False Actual: True")


class ValidateRoleTest(TestCase):
    ROLE_CHOICES = ["admin", "Admin",
                    "instructor", "Instructor",
                    "ta", "TA"]

    invalid_role = ["user", "Teacher", "Professor",
                    "DR", "PHD"]

    def test_no_role(self):
        self.assertFalse(func_ValidateRole(""), "Expected: False Actual: True")

    def test_empty_role(self):
        self.assertFalse(func_ValidateRole(" "), "Expected: False Actual: True")

    def test_valid_role(self):
        for role in self.ROLE_CHOICES:
            self.assertTrue(func_ValidateRole(role), "Expected: True Actual: False")

    def test_invalid_role(self):
        for role in self.invalid_role:
            self.assertFalse(func_ValidateState(role), "Expected: False Actual: True")
