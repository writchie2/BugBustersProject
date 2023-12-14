from django.test import TestCase

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

    def test_invalid_email(self):
        self.assertEqual(self.bad_email, "Invalid email. Must be a UWM email.")

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
        msg = func_EditFirstName("N1chole", "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid first name. Must be capitalized and have only contain letters.")

    def test_non_letters(self):
        msg = func_EditFirstName("Er!k", "erik@uwm.edu")
        self.assertEqual(msg, "Invalid first name. Must be capitalized and have only contain letters.")

    def test_no_capital(self):
        msg = func_EditFirstName("henry", "henry@uwm.edu")
        self.assertEqual(msg, "Invalid first name. Must be capitalized and have only contain letters.")

    def test_valid_input(self):
        msg = func_EditFirstName("Kevin", "kevin@uwm.edu")
        self.assertEqual(msg, "First name changed successfully!")


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
        msg = func_EditLastName("Ch6im", "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid last name. Must be capitalized and have only contain letters.")

    def test_non_letters(self):
        msg = func_EditLastName("Sh#n", "erik@uwm.edu")
        self.assertEqual(msg, "Invalid last name. Must be capitalized and have only contain letters.")

    def test_no_capital(self):
        msg = func_EditLastName("ritchie", "henry@uwm.edu")
        self.assertEqual(msg, "Invalid last name. Must be capitalized and have only contain letters.")

    def test_valid_input(self):
        msg = func_EditLastName("Santamaria", "kevin@uwm.edu")
        self.assertEqual(msg, "Last name changed successfully!")


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
        # should assert the number changed?

    def test_no_input(self):
        new_number = ""
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")

    def test_empty_input(self):
        new_number = " "
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")

    def test_num_too_long(self):
        new_number = "41498765432"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")

    def test_num_too_short(self):
        new_number = "4149876"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")

    def test_alpha_in_num(self):
        new_number = "4I49876543"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")

    def test_invalid_char_in_num(self):
        new_number = "414_987_6543"
        msg = func_EditPhoneNumber(new_number, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid phone number. Format is 123-456-7890")


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

    def test_no_street(self):
        street = ""
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")

    def test_empty_street(self):
        street = ""
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")

    def test_only_building_number(self):
        street = "12345"
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")

    def test_no_street_type(self):
        street = "12345 Main"
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")

    def test_invalid_char(self):
        street = "1234 M@ain St"
        msg = func_EditStreetAddress(street, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid street address.")


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

    def test_no_city(self):
        city = ""
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")

    def test_empty_city(self):
        city = " "
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")

    def test_no_capital(self):
        city = "milwaukee"
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")

    def test_too_short(self):
        city = "A"
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")

    def test_too_long(self):
        city = "Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        msg = func_EditCity(city, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid city. Must be capitalized.")


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

    def test_no_input(self):
        state = ""
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")

    def test_empty_input(self):
        state = " "
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")

    def test_full_state_name(self):
        state = "Wisconsin"
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")

    def test_non_existing_state(self):
        state = "DQ"
        msg = func_EditState(state, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid state. Two letter state code only.")


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

    def test_empty(self):
        zipcode = ""
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")

    def test_no_input(self):
        zipcode = " "
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")

    def test_alpha_in_zip(self):
        zipcode = "abdce"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")

    def test_invalid_char_in_zip(self):
        zipcode = "532$0"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")

    def test_zip_too_short(self):
        zipcode = "5432"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")

    def test_zip_too_long(self):
        zipcode = "123456"
        msg = func_EditZipcode(zipcode, "nichole@uwm.edu")
        self.assertEqual(msg, "Invalid zipcode. Must be 5 digits long.")
