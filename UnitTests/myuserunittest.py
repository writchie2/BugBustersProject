import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import  MyUser, Course, Section
from SchedulingApp.functions import func_ValidateEmail, func_ValidatePassword, func_ValidateFirstName, func_ValidateLastName, func_ValidatePhoneNumber, func_ValidateStreetAddress, func_ValidateCity, func_ValidateState, func_ValidateZipCode
from django.test import TestCase, Client

class ValidateEmailTest(TestCase):
    pass

class ValidatePasswordTest(TestCase):
    pass

class ValidateFirstNameTest(TestCase):
    pass

class ValidateLastNameTest(TestCase):
    pass

class ValidatePhoneNumberTest(TestCase):
    pass
class ValidateStreetAddressTest(TestCase):
    pass
class ValidateCityTest(TestCase):
    pass
class ValidateStateTest(TestCase):
    pass
class ValidateZipCodeTest(TestCase):
    pass