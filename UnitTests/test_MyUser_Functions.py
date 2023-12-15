from django.test import TestCase
from SchedulingApp.models import MyUser

from SchedulingApp.Model_Classes.MyUser_Functions import (
    func_MyUserCreator, func_EditStreetAddress,
    func_EditZipcode, func_EditLastName, func_EditCity, func_EditRole,
    func_EditFirstName, func_EditPhoneNumber, func_EditState,
    func_MyUserDeleter, func_SaveBio, func_RemoveExcessNewLine)


class TestMyUserCreator(TestCase):

    def setUp(self):
        self.valid_user = func_MyUserCreator("email@uwm.edu",
                                             "Password!2",
                                             "Password!2",
                                             "First", "Last",
                                             "123-456-7890",
                                             "1234 Main St",
                                             "Milwaukee",
                                             "WI",
                                             "53206",
                                             "TA")

        self.bad_email = func_MyUserCreator("email@gmail.com",
                                            "Password!2",
                                            "Password!2",
                                            "First", "Last",
                                            "123-456-7890",
                                            "1234 Main St",
                                            "Milwaukee",
                                            "WI",
                                            "53206",
                                            "TA")

        self.bad_pass = func_MyUserCreator("email1@uwm.edu",
                                           "password",
                                           "password",
                                           "First", "Last",
                                           "123-456-7890",
                                           "1234 Main St",
                                           "Milwaukee",
                                           "WI",
                                           "53206",
                                           "TA")

        self.mismatching_pass = func_MyUserCreator("email2@uwm.edu",
                                                   "Password!2",
                                                   "Password!",
                                                   "First", "Last",
                                                   "123-456-7890",
                                                   "1234 Main St",
                                                   "Milwaukee",
                                                   "WI",
                                                   "53206",
                                                   "TA")

        self.bad_first = func_MyUserCreator("email3@uwm.edu",
                                            "Password!2",
                                            "Password!2",
                                            "f", "Last",
                                            "123-456-7890",
                                            "1234 Main St",
                                            "Milwaukee",
                                            "WI",
                                            "53206",
                                            "TA")

        self.bad_last = func_MyUserCreator("email4@uwm.edu",
                                           "Password!2",
                                           "Password!2",
                                           "First", "l",
                                           "123-456-7890",
                                           "1234 Main St",
                                           "Milwaukee",
                                           "WI",
                                           "53206",
                                           "TA")

        self.bad_num = func_MyUserCreator("email5@uwm.edu",
                                          "Password!2",
                                          "Password!2",
                                          "First", "Last",
                                          "123-456-7890123",
                                          "1234 Main St",
                                          "Milwaukee",
                                          "WI",
                                          "53206",
                                          "TA")

        self.bad_street = func_MyUserCreator("email6@uwm.edu",
                                             "Password!2",
                                             "Password!2",
                                             "First", "Last",
                                             "123-456-7890",
                                             "12 St",
                                             "Milwaukee",
                                             "WI",
                                             "53206",
                                             "TA")

        self.bad_city = func_MyUserCreator("email7@uwm.edu",
                                           "Password!2",
                                           "Password!2",
                                           "First", "Last",
                                           "123-456-7890",
                                           "1234 Main St",
                                           "a",
                                           "WI",
                                           "53206",
                                           "TA")

        self.bad_state = func_MyUserCreator("email8@uwm.edu",
                                            "Password!2",
                                            "Password!2",
                                            "First", "Last",
                                            "123-456-7890",
                                            "1234 Main St",
                                            "Milwaukee",
                                            "Wisconsin",
                                            "53206",
                                            "TA")

        self.bad_zip = func_MyUserCreator("email9@uwm.edu",
                                          "Password!2",
                                          "Password!2",
                                          "First", "Last",
                                          "123-456-7890",
                                          "1234 Main St",
                                          "Milwaukee",
                                          "WI",
                                          "5",
                                          "TA")

        self.bad_role = func_MyUserCreator("email10@uwm.edu",
                                           "Password!2",
                                           "Password!2",
                                           "First", "Last",
                                           "123-456-7890",
                                           "1234 Main St",
                                           "Milwaukee",
                                           "WI",
                                           "53206",
                                           "Professor")

    def test_valid_input(self):
        self.assertEqual(self.valid_user, "User created successfully!")
        self.assertTrue(MyUser.objects.filter(email="email@uwm.edu").exists(), "User with valid input was not created!")

    def test_invalid_email(self):
        self.assertEqual(self.bad_email, "Invalid email. Must be a UWM email.")

    def test_same_email(self):
        msg = func_MyUserCreator("email@uwm.edu",
                                 "Password!2",
                                 "Password!2",
                                 "First", "Last",
                                 "123-456-7890",
                                 "1234 Main St",
                                 "Milwaukee",
                                 "WI",
                                 "53206",
                                 "TA")
        self.assertEqual(msg, "Non-unique email. Please try again.")

    def test_invalid_pass(self):
        self.assertEqual(self.bad_pass, "Passwords must match and contain one lowercase letter, one uppercase letter,"
                                        " a digit, and a special character. Please try again.")

    def test_mismatching_pass(self):
        self.assertEqual(self.mismatching_pass,
                         "Passwords must match and contain one lowercase letter, one uppercase letter,"
                         " a digit, and a special character. Please try again.")

    def test_invalid_first(self):
        self.assertEqual(self.bad_first, "Invalid first name. Must be capitalized and have only contain letters.")

    def test_invalid_last(self):
        self.assertEqual(self.bad_last, "Invalid last name. Must be capitalized and have only contain letters.")

    def test_invalid_num(self):
        self.assertEqual(self.bad_num, "Invalid phone number. Format is 123-456-7890")

    def test_invalid_street(self):
        self.assertEqual(self.bad_street, "Invalid street address.")

    def test_invalid_city(self):
        self.assertEqual(self.bad_city, "Invalid city. Must be capitalized.")

    def test_invalid_state(self):
        self.assertEqual(self.bad_state, "Invalid state. Two letter state code only.")

    def test_invalid_zip(self):
        self.assertEqual(self.bad_zip, "Invalid zipcode. Must be 5 digits long")

    def test_invalid_role(self):
        self.assertEqual(self.bad_role, "Invalid role. Can only be Admin, Instructor, or TA.")


class TestEditFirstName(TestCase):

    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nicole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

        self.erik = func_MyUserCreator("erik@uwm.edu", "Password!1234",
                                       "Password!1234", "Eric",
                                       "Shen", "4141234568", "4321 Main St",
                                       "Milwaukee", "WI", "53220", "Admin")

        self.henry = func_MyUserCreator("henry@uwm.edu", "Password!12345",
                                        "Password!12345", "Henri",
                                        "Ritchie", "4141234569", "2134 Main St",
                                        "Milwaukee", "WI", "53220", "TA")

        self.kevin = func_MyUserCreator("kevin@uwm.edu", "Password!123456",
                                        "Password!123456", "Kevyn",
                                        "Santamaria", "4141234560", "4231 Main St",
                                        "Milwaukee", "WI", "53220", "Admin")

    def test_numbers(self):
        og_first = MyUser.objects.get(email="nichole@uwm.edu").firstName
        msg = func_EditFirstName("N1chole", "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid first name. Must be capitalized and have only contain letters.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").firstName, og_first)

    def test_non_existing_user(self):
        msg = func_EditFirstName("Nichole", "nonexisting@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_non_letters(self):
        og_first = MyUser.objects.get(email="erik@uwm.edu").firstName
        msg = func_EditFirstName("Er!k", "erik@uwm.edu")
        self.assertEqual(msg, "Invalid first name. Must be capitalized and have only contain letters.")
        self.assertEqual(MyUser.objects.get(email="erik@uwm.edu").firstName, og_first)

    def test_no_capital(self):
        og_first = MyUser.objects.get(email="henry@uwm.edu").firstName
        msg = func_EditFirstName("henry", "henry@uwm.edu")
        self.assertEqual(msg, "Invalid first name. Must be capitalized and have only contain letters.")
        self.assertEqual(MyUser.objects.get(email="henry@uwm.edu").firstName, og_first)

    def test_valid_input(self):
        first = "Kevin"
        msg = func_EditFirstName(first, "kevin@uwm.edu")
        self.assertEqual(msg, "First name changed successfully!")
        self.assertEqual(MyUser.objects.get(email="kevin@uwm.edu").firstName, first)


class TestEditLastName(TestCase):

    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chain", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

        self.erik = func_MyUserCreator("erik@uwm.edu", "Password!1234",
                                       "Password!1234", "Erik",
                                       "Shein", "4141234568", "4321 Main St",
                                       "Milwaukee", "WI", "53220", "Admin")

        self.henry = func_MyUserCreator("henry@uwm.edu", "Password!12345",
                                        "Password!12345", "Henry",
                                        "Ritchy", "4141234569", "2134 Main St",
                                        "Milwaukee", "WI", "53220", "TA")

        self.kevin = func_MyUserCreator("kevin@uwm.edu", "Password!123456",
                                        "Password!123456", "Kevin",
                                        "Santomaria", "4141234560", "4231 Main St",
                                        "Milwaukee", "WI", "53220", "Admin")

    def test_numbers(self):
        og_last = MyUser.objects.get(email="nichole@uwm.edu").lastName
        msg = func_EditLastName("Ch6im", "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid last name. Must be capitalized and have only contain letters.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").lastName, og_last)

    def test_non_existing_user(self):
        msg = func_EditLastName("Chaim", "nonexisting@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_non_letters(self):
        og_last = MyUser.objects.get(email="erik@uwm.edu").lastName
        msg = func_EditLastName("Sh#n", "erik@uwm.edu")
        self.assertEqual(msg, "Invalid last name. Must be capitalized and have only contain letters.")
        self.assertEqual(MyUser.objects.get(email="erik@uwm.edu").lastName, og_last)

    def test_no_capital(self):
        og_last = MyUser.objects.get(email="henry@uwm.edu").lastName
        msg = func_EditLastName("ritchie", "henry@uwm.edu")
        self.assertEqual(msg, "Invalid last name. Must be capitalized and have only contain letters.")
        self.assertEqual(MyUser.objects.get(email="henry@uwm.edu").lastName, og_last)

    def test_valid_input(self):
        last = "Santamaria"
        msg = func_EditLastName(last, "kevin@uwm.edu")
        self.assertEqual(msg, "Last name changed successfully!")
        self.assertEqual(MyUser.objects.get(email="kevin@uwm.edu").lastName, last)


class TestEditPhoneNumber(TestCase):

    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

    def test_num_valid_input(self):
        new_number = "4149876543"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Phone number changed successfully!")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").phoneNumber, new_number)

    def test_non_existing_user(self):
        new_number = "4149876543"
        msg = func_EditPhoneNumber(new_number, "nonexistinge@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_no_input(self):
        og_number = MyUser.objects.get(email="nichole@uwm.edu").phoneNumber
        new_number = ""
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").phoneNumber, og_number)

    def test_empty_input(self):
        og_number = MyUser.objects.get(email="nichole@uwm.edu").phoneNumber
        new_number = " "
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").phoneNumber, og_number)

    def test_num_too_long(self):
        og_number = MyUser.objects.get(email="nichole@uwm.edu").phoneNumber
        new_number = "41498765432"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").phoneNumber, og_number)

    def test_num_too_short(self):
        og_number = MyUser.objects.get(email="nichole@uwm.edu").phoneNumber
        new_number = "4149876"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").phoneNumber, og_number)

    def test_alpha_in_num(self):
        og_number = MyUser.objects.get(email="nichole@uwm.edu").phoneNumber
        new_number = "4I49876543"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").phoneNumber, og_number)

    def test_invalid_char_in_num(self):
        og_number = MyUser.objects.get(email="nichole@uwm.edu").phoneNumber
        new_number = "414_987_6543"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").phoneNumber, og_number)


class TestEditStreetAddress(TestCase):
    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

    def test_valid_street(self):
        street = "1111 Kenwood Blvd"
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Street address changed successfully!")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").streetAddress, street)

    def test_non_existing_user(self):
        street = "1111 Kenwood Blvd"
        msg = func_EditStreetAddress(street, "nonexisting@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_no_street(self):
        og_street = MyUser.objects.get(email="nichole@uwm.edu").streetAddress
        street = ""
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").streetAddress, og_street)

    def test_empty_street(self):
        og_street = MyUser.objects.get(email="nichole@uwm.edu").streetAddress
        street = ""
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").streetAddress, og_street)

    def test_only_building_number(self):
        og_street = MyUser.objects.get(email="nichole@uwm.edu").streetAddress
        street = "12345"
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").streetAddress, og_street)

    def test_no_street_type(self):
        og_street = MyUser.objects.get(email="nichole@uwm.edu").streetAddress
        street = "12345 Main"
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").streetAddress, og_street)

    def test_invalid_char(self):
        og_street = MyUser.objects.get(email="nichole@uwm.edu").streetAddress
        street = "1234 M@ain St"
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").streetAddress, og_street)


class TestEditCity(TestCase):
    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

    def test_valid_city(self):
        city = "Greenfield"
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "City changed successfully!")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").city, city)

    def test_non_existing_user(self):
        city = "Greenfield"
        msg = func_EditCity(city, "nonexisting@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_no_city(self):
        og_city = MyUser.objects.get(email="nichole@uwm.edu").city
        city = ""
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").city, og_city)

    def test_empty_city(self):
        og_city = MyUser.objects.get(email="nichole@uwm.edu").city
        city = " "
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").city, og_city)

    def test_no_capital(self):
        og_city = MyUser.objects.get(email="nichole@uwm.edu").city
        city = "milwaukee"
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").city, og_city)

    def test_too_short(self):
        og_city = MyUser.objects.get(email="nichole@uwm.edu").city
        city = "A"
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").city, og_city)

    def test_too_long(self):
        og_city = MyUser.objects.get(email="nichole@uwm.edu").city
        city = "Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").city, og_city)


class TestEditState(TestCase):
    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

    def test_valid_State(self):
        state = "IL"
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "State changed successfully!")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").state, state)

    def test_non_existing_user(self):
        state = "IL"
        msg = func_EditState(state, "nonexisting@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_no_input(self):
        og_state = MyUser.objects.get(email="nichole@uwm.edu").state
        state = ""
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").state, og_state)

    def test_empty_input(self):
        og_state = MyUser.objects.get(email="nichole@uwm.edu").state
        state = " "
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").state, og_state)

    def test_full_state_name(self):
        og_state = MyUser.objects.get(email="nichole@uwm.edu").state
        state = "Wisconsin"
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").state, og_state)

    def test_non_existing_state(self):
        og_state = MyUser.objects.get(email="nichole@uwm.edu").state
        state = "DQ"
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").state, og_state)


class TestEditZipcode(TestCase):
    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

    def test_valid_input(self):
        zipcode = "53206"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Zipcode changed successfully!")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").zipcode, zipcode)

    def test_non_existing_user(self):
        zipcode = "53206"
        msg = func_EditZipcode(zipcode, "nonexisting@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_empty(self):
        og_zip = MyUser.objects.get(email="nichole@uwm.edu").zipcode
        zipcode = ""
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").zipcode, og_zip)

    def test_no_input(self):
        og_zip = MyUser.objects.get(email="nichole@uwm.edu").zipcode
        zipcode = " "
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").zipcode, og_zip)

    def test_alpha_in_zip(self):
        og_zip = MyUser.objects.get(email="nichole@uwm.edu").zipcode
        zipcode = "abdce"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").zipcode, og_zip)

    def test_invalid_char_in_zip(self):
        og_zip = MyUser.objects.get(email="nichole@uwm.edu").zipcode
        zipcode = "532$0"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").zipcode, og_zip)

    def test_zip_too_short(self):
        og_zip = MyUser.objects.get(email="nichole@uwm.edu").zipcode
        zipcode = "5432"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").zipcode, og_zip)

    def test_zip_too_long(self):
        og_zip = MyUser.objects.get(email="nichole@uwm.edu").zipcode
        zipcode = "123456"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").zipcode, og_zip)


class TestEditRole(TestCase):
    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

    def test_valid_input(self):
        role = "Admin"
        msg = func_EditRole(role, "nichole@uwm.edu")
        self.assertEqual(msg, "Role changed successfully!")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").role, role)

    def test_nonexisting_user(self):
        role = "Instructor"
        msg = func_EditRole(role, "nonexisting@uwm.edu")
        self.assertEqual(msg, "User does not exist!")

    def test_empty_role(self):
        og_role = MyUser.objects.get(email="nichole@uwm.edu").role
        role = ""
        msg = func_EditRole(role, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid role. Can only be Admin, Instructor, or TA.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").role, og_role)

    def test_no_role(self):
        og_role = MyUser.objects.get(email="nichole@uwm.edu").role
        role = " "
        msg = func_EditRole(role, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid role. Can only be Admin, Instructor, or TA.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").role, og_role)

    def test_invalid_role(self):
        og_role = MyUser.objects.get(email="nichole@uwm.edu").role
        role = "Prof"
        msg = func_EditRole(role, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid role. Can only be Admin, Instructor, or TA.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").role, og_role)

    def test_num_in_role(self):
        og_role = MyUser.objects.get(email="nichole@uwm.edu").role
        role = "Adm1n"
        msg = func_EditRole(role, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid role. Can only be Admin, Instructor, or TA.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").role, og_role)

    def test_bad_char_in_role(self):
        og_role = MyUser.objects.get(email="nichole@uwm.edu").role
        role = "T@"
        msg = func_EditRole(role, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid role. Can only be Admin, Instructor, or TA.")
        self.assertEqual(MyUser.objects.get(email="nichole@uwm.edu").role, og_role)


class TestMyUserDeleter(TestCase):
    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

        self.erik = func_MyUserCreator("erik@uwm.edu", "Password!1234",
                                       "Password!1234", "Erik",
                                       "Shen", "4141234568", "4321 Main St",
                                       "Milwaukee", "WI", "53220", "Admin")

        self.henry = func_MyUserCreator("henry@uwm.edu", "Password!12345",
                                        "Password!12345", "Henry",
                                        "Ritchie", "4141234569", "2134 Main St",
                                        "Milwaukee", "WI", "53220", "TA")

        self.kevin = func_MyUserCreator("kevin@uwm.edu", "Password!123456",
                                        "Password!123456", "Kevin",
                                        "Santamaria", "4141234560", "4231 Main St",
                                        "Milwaukee", "WI", "53220", "Admin")

    def test_delete(self):
        msg = func_MyUserDeleter("nichole@uwm.edu")
        self.assertEqual(msg, "User deleted successfully")
        self.assertFalse(MyUser.objects.filter(email="nichole@uwm.edu").exists(), "User: Nichole was not deleted!")
        self.assertTrue(MyUser.objects.filter(email="erik@uwm.edu").exists(), "Wrong user: Erik was deleted!")
        self.assertTrue(MyUser.objects.filter(email="henry@uwm.edu").exists(), "Wrong user: Henry was deleted!")
        self.assertTrue(MyUser.objects.filter(email="kevin@uwm.edu").exists(), "Wrong user: Kevin was deleted!")

    def test_delete_non_existing_user(self):
        msg = func_MyUserDeleter("non-existing@uwm.edu")
        self.assertEqual(msg, "User does not exist!")
        self.assertTrue(MyUser.objects.filter(email="nichole@uwm.edu").exists(), "Wrong user: Nichole was deleted!")
        self.assertTrue(MyUser.objects.filter(email="erik@uwm.edu").exists(), "Wrong user: Erik was deleted!")
        self.assertTrue(MyUser.objects.filter(email="henry@uwm.edu").exists(), "Wrong user: Henry was deleted!")
        self.assertTrue(MyUser.objects.filter(email="kevin@uwm.edu").exists(), "Wrong user: Kevin was deleted!")


class TestSaveBio(TestCase):

    def setUp(self):
        self.nichole = func_MyUserCreator("nichole@uwm.edu", "Password!123",
                                          "Password!123", "Nichole",
                                          "Chaim", "4141234567", "1234 Main St",
                                          "Milwaukee", "WI", "53220", "TA")

    def test_change_bio(self):
        bio = func_RemoveExcessNewLine("I would rather be playing Baldur's Gate 3")
        func_SaveBio("nichole@uwm.edu", bio)
        self.assertEqual(bio, MyUser.objects.get(email="nichole@uwm.edu").bio)


class TestRemoveExcessNewLine(TestCase):
    def test_remove_excess_newline(self):
        input_string = "Hello\r\n\r\nWorld\r\n"
        expected_output = "Hello\r\nWorld\r\n"
        result = func_RemoveExcessNewLine(input_string)
        self.assertEqual(result, expected_output)

    def test_remove_excess_newline_empty_string(self):
        input_string = ""
        expected_output = ""
        result = func_RemoveExcessNewLine(input_string)
        self.assertEqual(result, expected_output)

    def test_remove_excess_newline_no_newline(self):
        input_string = "NoNewline"
        expected_output = "NoNewline\r\n"
        result = func_RemoveExcessNewLine(input_string)
        self.assertEqual(result, expected_output)

    def test_remove_excess_newline_multiple_empty_lines(self):
        input_string = "Line1\r\n\r\n\r\nLine2\r\n\r\n"
        expected_output = "Line1\r\nLine2\r\n"
        result = func_RemoveExcessNewLine(input_string)
        self.assertEqual(result, expected_output)

    def test_remove_excess_newline_whitespace_lines(self):
        input_string = "   \r\n  \r\n\t\r\n"
        expected_output = "   \r\n  \r\n\t\r\n"
        result = func_RemoveExcessNewLine(input_string)
        self.assertEqual(result, expected_output)
