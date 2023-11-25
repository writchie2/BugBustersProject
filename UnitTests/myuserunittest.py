import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_ValidateEmail, func_ValidatePassword, func_ValidateFirstName, \
    func_ValidateLastName, func_ValidatePhoneNumber, func_ValidateStreetAddress, func_ValidateCity, func_ValidateState, \
    func_ValidateZipCode
from django.test import TestCase, Client


class ValidateEmailTest(TestCase):
    max_email_length = 20
    min_email_length = 9

    invalid_emails = ["invalid_email", "user@edu", "user@.edu", "a",
                      "user@uwm.com ", "user.edu", "@uwm.edu",
                      "person 1@uwm.edu", ".person@uwm.edu", "per..son@uwm.edu"]

    invalid_whitespace = [" user@uwm.edu", "user@uwm.edu ", " user@uwm.edu "]

    long_email = "a" * ((max_email_length - min_email_length) + 1) + "@uwm.edu"

    def test_no_email(self):
        with self.assertRaises(ValueError):
            func_ValidateEmail("")

    def test_empty_email(self):
        with self.assertRaises(ValueError):
            func_ValidateEmail(" ")

    def test_valid_email(self):
        email = "person@uwm.edu"
        try:
            func_ValidateEmail(email)
        except Exception as e:
            self.fail(f"func_Validate_email raised an exception: {e}")

    def test_invalid_formats(self):
        for email in self.invalid_emails:
            with self.assertRaises(ValueError):
                func_ValidateEmail(email)

    def test_long_email(self):
        with self.assertRaises(ValueError):
            func_ValidateEmail(self.long_email)

    def test_whitespace(self):
        for email in self.invalid_whitespace:
            with self.assertRaises(ValueError):
                func_ValidateEmail(email)


class ValidatePasswordTest(TestCase):
    pass


class ValidateFirstNameTest(TestCase):
    invalid_names = ["a", "@d@m", "P3n3lop3", "R!ley", "Jak3"]
    long_name = "A" * 21
    valid_names = ["Adam", "Penelope", "Riley", "Jackson", "Aaaaaaaaaaaaaaaaaaaa",
                   "McDonald", "Edwards"]

    def test_no_name(self):
        with self.assertRaises(ValueError):
            func_ValidateFirstName("")

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            func_ValidateFirstName(" ")

    def test_valid_name(self):
        try:
            for name in self.valid_names:
                func_ValidateFirstName(name)
        except Exception as e:
            self.fail(f"func_ValidateFirstName raised an exception: {e}")

    def test_invalid_names(self):
        for name in self.invalid_names:
            with self.assertRaises(ValueError):
                func_ValidateFirstName(name)

    def test_long_name(self):
        with self.assertRaises(ValueError):
            func_ValidateFirstName(self.long_name)


class ValidateLastNameTest(TestCase):
    invalid_names = ["a", "@d@m", "P3n3lop3", "R!ley", "Jak3"]
    long_name = "A" * 21
    valid_names = ["Adam", "Penelope", "Riley", "Jackson", "Aaaaaaaaaaaaaaaaaaaa",
                   "McDonald", "Edwards"]

    def test_no_name(self):
        with self.assertRaises(ValueError):
            func_ValidateLastName("")

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            func_ValidateLastName(" ")

    def test_valid_name(self):
        try:
            for name in self.valid_names:
                func_ValidateLastName(name)
        except Exception as e:
            self.fail(f"func_ValidateLastName raised an exception: {e}")

    def test_invalid_names(self):
        for name in self.invalid_names:
            with self.assertRaises(ValueError):
                func_ValidateLastName(name)

    def test_long_name(self):
        with self.assertRaises(ValueError):
            func_ValidateLastName(self.long_name)


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
        with self.assertRaises(ValueError):
            func_ValidatePhoneNumber("")

    def test_empty_number(self):
        with self.assertRaises(ValueError):
            func_ValidatePhoneNumber(" ")

    def test_valid_numbers(self):
        try:
            for number in self.valid_phone_numbers:
                func_ValidatePhoneNumber(number)
        except Exception as e:
            self.fail(f"func_ValidatePhoneNumber raised an exception: {e}")

    def test_invalid_numbers(self):
        for number in self.invalid_phone_numbers:
            with self.assertRaises(ValueError):
                func_ValidatePhoneNumber(number)

    def test_long_number(self):
        with self.assertRaises(ValueError):
            func_ValidatePhoneNumber(self.long_number)

    def test_whitespace(self):
        for number in self.invalid_whitespace:
            func_ValidatePhoneNumber(number)


class ValidateStreetAddressTest(TestCase):
    pass


class ValidateCityTest(TestCase):
    pass


class ValidateStateTest(TestCase):
    pass


class ValidateZipCodeTest(TestCase):
    pass
