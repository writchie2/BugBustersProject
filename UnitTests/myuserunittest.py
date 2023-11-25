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
            self.fail(f"func_ValidateEmail raised an exception: {e}")

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
    valid_street = ["1234 South Main Street", "1234 E Main St",
                    "1234 W Main Street", "1234 North Main St",
                    "1234 Main Street", "1234 Main St",
                    "1234 South Rio Grande Avenue"]

    invalid_street = ["1st St", "South University st",
                      "1234 Avenue", "12 34 W Kenwood Blvd",
                      "5678 South", "North Ave",
                      "!2E4 East Washington Ave"]

    long_street = "1234567890 Soooooouth Rioooooooo Saladooooo Roooooooad"

    def test_no_address(self):
        func_ValidateStreetAddress("")

    def test_empty_address(self):
        func_ValidateStreetAddress(" ")

    def test_valid_address(self):
        try:
            for address in self.valid_street:
                func_ValidateStreetAddress(address)
        except Exception as e:
            self.fail(f"func_ValidatePhoneNumber raised an exception: {e}")

    def test_invalid_address(self):
        for address in self.invalid_street:
            with self.assertRaises(ValueError):
                func_ValidateStreetAddress(address)

    def test_long_address(self):
        with self.assertRaises(ValueError):
            func_ValidateStreetAddress(self.long_street)


class ValidateCityTest(TestCase):
    valid_city = ["Milwaukee", "Los Angeles", "Cleveland", "Orlando",
                  "Houston", "Seattle", "San Juan", "Chicago", "Mundelein",
                  "Miami", "San Francisco", "Phoenix", "Ponce de Leon",
                  "San Diego", "Puerto Penasco"]

    invalid_city = ["a", "L0s Ang3l3s", "Ch!c@go"]

    long_city = "A" * 20

    def test_no_city(self):
        func_ValidateCity("")

    def test_empty_city(self):
        func_ValidateCity(" ")

    def test_valid_city(self):
        try:
            for city in self.valid_city:
                func_ValidateCity(city)
        except Exception as e:
            self.fail(f"func_ValidateCity raised an exception: {e}")

    def test_invalid_city(self):
        for city in self.invalid_city:
            with self.assertRaises(ValueError):
                func_ValidateCity(city)

    def test_long_city(self):
        with self.assertRaises(ValueError):
            func_ValidateCity(self.long_city)


class ValidateStateTest(TestCase):
    valid_state = ["AL", "AK", "AZ", "AR",
                   "CA","CO", "CT","DC",
                   "DE", "FL", "GA","HI",
                   "ID", "IL","IN", "IA",
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
        func_ValidateState("")

    def test_empty_state(self):
        func_ValidateState(" ")

    def test_valid_state(self):
        try:
            for state in self.valid_state:
                func_ValidateState(state)
        except Exception as e:
            self.fail(f"func_ValidateState raised an exception: {e}")

    def test_invalid_state(self):
        for state in self.invalid_state:
            with self.assertRaises(ValueError):
                func_ValidateState(state)

class ValidateZipCodeTest(TestCase):
    valid_zip = [53206, 12345, 53220]
    invalid_zip = [53, 2, -53220]
    def test_no_zip(self):
        func_ValidateZipCode(0)

    def test_valid_zip(self):
        try:
            for zip_code in self.valid_zip:
                func_ValidateZipCode(zip_code)
        except Exception as e:
            self.fail(f"func_ValidateZipCode raised an exception: {e}")

    def test_invalid_zip(self):
        for zip_code in self.invalid_zip:
            with self.assertRaises(ValueError):
                func_ValidateState(zip_code)