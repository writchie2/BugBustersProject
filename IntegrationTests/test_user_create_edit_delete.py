import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class CreatUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.henry = MyUser(1,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                       "Milwaukee", "WI", 53026, "admin")

        self.henry.save()

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

    def test_CreateUserInvalidEmail(self):
        response = self.client.post("/createuser/",
                                    {"email": "writchie@uwm.edu",
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
        self.assertEqual(response.context["message"], "Non-unique email. Please try again.",
                         "Error not played if nonunique usernames")

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

    def test_CreateUserInvalidPhoneNumber(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "Password!1",
                                     "confirmpassword": "Password!1",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid phone number. Format is 123-456-7890",
                         "Error not played if invalid phonenumber")

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


class EditUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selecteduser"] = "esonnen@uwm.edu"
        session.save()
        self.henryRitchie = MyUser(1,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                       "Milwaukee", "WI", 53026, "instructor")
        self.henryRitchie.save()
        self.emmaSonnen = MyUser(2,"esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                 "Milwaukee", "WI", 53026, "admin")

        self.emmaSonnen.save()

    def test_EditFirstNameValid(self):
        response = self.client.post("/edituser/", {"firstname": "Nancy"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.firstName, "Nancy",
                         "firstname not edited in edituser when valid")
        self.assertEqual(response.context["message"], "First name changed successfully!",
                         "success message does not show for successful edit")

    def test_EditFirstNameInvalid(self):
        response = self.client.post("/edituser/", {"firstname": "nancy"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.firstName, "Emma",
                         "firstname is edited in edituser when invalid")
        self.assertEqual(response.context["message"],
                         "Invalid first name. Must be capitalized and have only contain letters.",
                         "error message does not show for unsuccessful edit")

    def test_EditLastNameValid(self):
        response = self.client.post("/edituser/", {"lastname": "Drew"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.lastName, "Drew",
                         "lastname not edited in lastname when valid")
        self.assertEqual(response.context["message"], "Last name changed successfully!",
                         "success message does not show for successful edit")

    def test_EditLastNameInvalid(self):
        response = self.client.post("/edituser/", {"lastname": "drew"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.lastName, "Sonnen",
                         "lastname is edited in edituser when invalid")
        self.assertEqual(response.context["message"],
                         "Invalid last name. Must be capitalized and have only contain letters.",
                         "error message does not show for unsuccessful edit")

    def test_EditPhoneNumberValid(self):
        response = self.client.post("/edituser/", {"phonenumber": "4145555555"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.phoneNumber, "4145555555",
                         "phonenumber not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Phone number changed successfully!",
                         "success message does not show for successful edit")

    def test_EditPhoneNumberInvalid(self):
        response = self.client.post("/edituser/", {"phonenumber": "55555"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.phoneNumber, "5555555555",
                         "phonenumber is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid phone number. Format is 123-456-7890",
                         "error message does not show for unsuccessful edit")

    def test_EditStreetAddressValid(self):
        response = self.client.post("/edituser/", {"streetaddress": "324 Maple rd"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.streetAddress, "324 Maple rd",
                         "streetaddress not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Street address changed successfully!",
                         "success message does not show for successful edit")

    def test_EditStreetAddressInvalid(self):
        response = self.client.post("/edituser/", {"streetaddress": "1234"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.streetAddress, "1234 main st",
                         "streetaddress is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid street address.",
                         "error message does not show for unsuccessful edit")

    def test_EditCityValid(self):
        response = self.client.post("/edituser/", {"city": "Chicago"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.city, "Chicago",
                         "city not edited in edituser when valid")
        self.assertEqual(response.context["message"], "City changed successfully!",
                         "success message does not show for successful edit")

    def test_EditCityInvalid(self):
        response = self.client.post("/edituser/", {"city": "chicago"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.city, "Milwaukee",
                         "city is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid city. Must be capitalized.",
                         "error message does not show for unsuccessful edit")

    def test_EditStateValid(self):
        response = self.client.post("/edituser/", {"state": "IL"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.state, "IL",
                         "state not edited in edituser when valid")
        self.assertEqual(response.context["message"], "State changed successfully!",
                         "success message does not show for successful edit")

    def test_EditStateInvalid(self):
        response = self.client.post("/edituser/", {"state": "il"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.state, "WI",
                         "state is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid state. Two letter state code only.",
                         "error message does not show for unsuccessful edit")

    def test_EditZipcodeValid(self):
        response = self.client.post("/edituser/", {"zipcode": "53022"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.zipcode, '53022',
                         "zipcode not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Zipcode changed successfully!",
                         "success message does not show for successful edit")

    def test_EditZipcodeInvalid(self):
        response = self.client.post("/edituser/", {"zipcode": "1234"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.zipcode, '53026',
                         "zipcode is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid zipcode. Must be 5 digits long.",
                         "error message does not show for unsuccessful edit")

    def test_EditRoleValid(self):
        response = self.client.post("/edituser/", {"role": "ta"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.role, "ta",
                         "role not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Role changed successfully!",
                         "success message does not show for successful edit")

    def test_EditRoleInvalid(self):
        response = self.client.post("/edituser/", {"role": "student"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual(self.emmaSonnen.role, "admin",
                         "role is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid role. Can only be Admin, Instructor, or TA.",
                         "error message does not show for unsuccessful edit")

class DeleteUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selecteduser"] = "esonnen@uwm.edu"
        session.save()
        self.henry = MyUser(1,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                       "Milwaukee", "WI", 53026, "instructor")
        self.henry.save()
        self.emma = MyUser(2,"esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                 "Milwaukee", "WI", 53026, "admin")

        self.emma.save()

    def test_DeleteUserSuccess(self):
        response = self.client.post('/userpage/', {"navigation": "deleteuser"}, follow=True)
        self.assertTemplateUsed(response,'directory.html')
        self.assertEqual(MyUser.objects.filter(email='esonnen@uwm.edu').first(), None, "User not deleted from database when valid")

    def test_DeleteUserNotAdmin(self):
        session = self.client.session
        session['role'] = 'ta'
        session.save()
        response = self.client.post('/userpage/', {"navigation": "deleteuser"}, follow=True)
        self.assertTemplateUsed(response,'userpage.html')
        self.assertEqual(MyUser.objects.filter(email='esonnen@uwm.edu').first(), self.emma, "User is deleted from database when non admin tries to delete")
        self.assertEqual(response.context['message'], "Only admins can delete users!",
                             "Error does not show when non admin tries to delete")