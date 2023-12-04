import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.henryRitchie = MyUser(1,"writchie@uwm.edu", "Password!", "Henry", "Ritchie", "5555555555", "1234 main st",
                                       "Milwaukee", "WI", 53026, "admin")

        self.henryRitchie.save()

    def test_CreateUserValid(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        newUser = MyUser.objects.filter(email="new@uwm.edu").first()
        self.assertEqual(newUser.email, "new@uwm.edu", "User saved with wrong email")
        self.assertEqual(newUser.firstName, "First", "User saved with wrong email")
        self.assertEqual(newUser.lastName, "Last", "User saved with wrong email")
        self.assertEqual(newUser.phoneNumber, "5555555555", "User saved with wrong email")
        self.assertEqual(newUser.streetAddress, "1234 Street rd", "User saved with wrong email")
        self.assertEqual(newUser.city, "Milwaukee", "User saved with wrong email")
        self.assertEqual(newUser.state, "WI", "User saved with wrong email")
        self.assertEqual(newUser.zipcode, '53026', "User saved with wrong email")
        self.assertEqual(newUser.role, "ta", "User saved with wrong email")
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"], "User created successfully!",
                         "Message not played if successful user creation")

    def test_CreatedUserIsDisplayed(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        response = self.client.get('/directory', follow=True)
        displayed = any(user['fullname'] == "First Last" for user in response.context['list'])
        self.assertTrue(displayed, "New user not displayed in directory page")

    def test_CreateUserInvalidEmail(self):
        response = self.client.post("/createuser/",
                                    {"email": "writchie",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"], "Invalid email. Must be a UWM email.",
                         "Error not played if nonunique usernames")
        self.assertEqual(MyUser.objects.filter(email='writchie').first(), None,
                         "User made with invalid email")

    def test_CreateUserInvalidPassword(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "pass",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"], "Passwords must match and contain one lowercase letter, one uppercase letter,"
                " a digit, and a special character. Please try again.",
                         "Error not played if not matching passwords")
        self.assertEqual(MyUser.objects.filter(password='password').first(), None,
                         "User made with invalid password")

    def test_CreateUserInvalidFirstName(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password1!",
                                     "confirmpassword": "Password1!",
                                     "firstname": "first",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid first name. Must be capitalized and have only contain letters.",
                         "Error not played if invalid firstname")
        self.assertEqual(MyUser.objects.filter(firstName='first').first(), None,
                         "User made with invalid first name")

    def test_CreateUserInvalidLastName(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid last name. Must be capitalized and have only contain letters.",
                         "Error not played if invalid lastname")
        self.assertEqual(MyUser.objects.filter(lastName='last').first(), None,
                         "User made with invalid last name")

    def test_CreateUserInvalidPhoneNumber(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "123-456-789",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid phone number. Format is 123-456-7890",
                         "Error not played if invalid phonenumber")
        self.assertEqual(MyUser.objects.filter(phoneNumber='123-456-789').first(), None,
                         "User made with invalid phone number")

    def test_CreateUserInvalidStreetAddress(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid street address.",
                         "Error not played if invalid address")
        self.assertEqual(MyUser.objects.filter(streetAddress='1234').first(), None,
                         "User made with invalid phone number")

    def test_CreateUserInvalidCity(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid city. Must be capitalized.",
                         "Error not played if invalid city")
        self.assertEqual(MyUser.objects.filter(city='milwaukee').first(), None,
                         "User made with invalid city")

    def test_CreateUserInvalidState(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "W",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid state. Two letter state code only.",
                         "Error not played if invalid state")
        self.assertEqual(MyUser.objects.filter(state='W').first(), None,
                         "User made with invalid state")

    def test_CreateUserInvalidZipcode(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "5302",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid zipcode. Must be 5 digits long",
                         "Error not played if invalid zipcode")
        self.assertEqual(MyUser.objects.filter(zipcode=5302).first(), None,
                         "User made with invalid zipcode")

    def test_CreateUserInvalidRole(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "student"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid role. Can only be Admin, Instructor, or TA.",
                         "Error not played if invalid role")
        self.assertEqual(MyUser.objects.filter(role='student').first(), None,
                         "User made with invalid role")