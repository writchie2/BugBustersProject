import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory
class EditUserPageViewTest(TestCase):
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
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing firstname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing firstname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing firstname")
        self.assertEqual(self.emmaSonnen.firstName, "Nancy",
                         "firstname not edited in edituser when valid")
        self.assertEqual(response.context["message"], "First name changed successfully!",
                         "success message does not show for successful edit")

    def test_EditFirstNameInvalid(self):
        response = self.client.post("/edituser/", {"firstname": "nancy"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing firstname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing firstname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing firstname")
        self.assertEqual(self.emmaSonnen.firstName, "Emma",
                         "firstname is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid first name. Must be capitalized and have only contain letters.",
                         "error message does not show for unsuccessful edit")

    def test_EditLastNameValid(self):
        response = self.client.post("/edituser/", {"lastname": "Drew"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing lastname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing lastname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing lastname")
        self.assertEqual(self.emmaSonnen.lastName, "Drew",
                         "lastname not edited in lastname when valid")
        self.assertEqual(response.context["message"], "Last name changed successfully!",
                         "success message does not show for successful edit")

    def test_EditLastNameInvalid(self):
        response = self.client.post("/edituser/", {"lastname": "drew"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing lastname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing lastname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing lastname")
        self.assertEqual(self.emmaSonnen.lastName, "Sonnen",
                         "lastname is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid First Name. Must be capitalized and have only contain letters.",
                         "error message does not show for unsuccessful edit")

    def test_EditPhoneNumberValid(self):
        response = self.client.post("/edituser/", {"phonenumber": "4145555555"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing phonenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing phonenumber")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing phonenumber")
        self.assertEqual(self.emmaSonnen.phoneNumber, "4145555555",
                         "phonenumber not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Phone number changed successfully!",
                         "success message does not show for successful edit")

    def test_EditPhoneNumberInvalid(self):
        response = self.client.post("/edituser/", {"phonenumber": "55555"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing phonenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing phonenumber")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing phonenumber")
        self.assertEqual(self.emmaSonnen.phoneNumber, "5555555555",
                         "phonenumber is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid phone number. Format is 123-456-7890",
                         "error message does not show for unsuccessful edit")

    def test_EditStreetAddressValid(self):
        response = self.client.post("/edituser/", {"streetaddress": "324 Maple rd"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing streetaddress")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing streetaddress")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing streetaddress")
        self.assertEqual(self.emmaSonnen.streetAddress, "324 Maple rd",
                         "streetaddress not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Street address changed successfully!",
                         "success message does not show for successful edit")

    def test_EditStreetAddressInvalid(self):
        response = self.client.post("/edituser/", {"streetaddress": "1234"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing streetaddress")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing streetaddress")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing streetaddress")
        self.assertEqual(self.emmaSonnen.streetAddress, "1234 main st",
                         "streetaddress is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid street address.",
                         "error message does not show for unsuccessful edit")

    def test_EditCityValid(self):
        response = self.client.post("/edituser/", {"city": "Chicago"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing city")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing city")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing city")
        self.assertEqual(self.emmaSonnen.city, "Chicago",
                         "city not edited in edituser when valid")
        self.assertEqual(response.context["message"], "City changed successfully!",
                         "success message does not show for successful edit")

    def test_EditCityInvalid(self):
        response = self.client.post("/edituser/", {"city": "chicago"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing city")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing city")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing city")
        self.assertEqual(self.emmaSonnen.city, "Milwaukee",
                         "city is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid city. Must be capitalized.",
                         "error message does not show for unsuccessful edit")

    def test_EditStateValid(self):
        response = self.client.post("/edituser/", {"state": "IL"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing state")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing state")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing state")
        self.assertEqual(self.emmaSonnen.state, "IL",
                         "state not edited in edituser when valid")
        self.assertEqual(response.context["message"], "State changed successfully!",
                         "success message does not show for successful edit")

    def test_EditStateInvalid(self):
        response = self.client.post("/edituser/", {"state": "il"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing state")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing state")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing state")
        self.assertEqual(self.emmaSonnen.state, "WI",
                         "state is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid state. Two letter state code only.",
                         "error message does not show for unsuccessful edit")

    def test_EditZipcodeValid(self):
        response = self.client.post("/edituser/", {"zipcode": "53022"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing zipcode")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing zipcode")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing zipcode")
        self.assertEqual(self.emmaSonnen.zipcode, '53022',
                         "zipcode not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Zipcode changed successfully!",
                         "success message does not show for successful edit")

    def test_EditZipcodeInvalid(self):
        response = self.client.post("/edituser/", {"zipcode": "1234"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing zipcode")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing zipcode")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing zipcode")
        self.assertEqual(self.emmaSonnen.zipcode, '53026',
                         "zipcode is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid zipcode. Must be 5 digits long.",
                         "error message does not show for unsuccessful edit")

    def test_EditRoleValid(self):
        response = self.client.post("/edituser/", {"role": "ta"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing role")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing role")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing role")
        self.assertEqual(self.emmaSonnen.role, "ta",
                         "role not edited in edituser when valid")
        self.assertEqual(response.context["message"], "Role changed successfully!",
                         "success message does not show for successful edit")

    def test_EditRoleInvalid(self):
        response = self.client.post("/edituser/", {"role": "student"}, follow=True)
        self.emmaSonnen = MyUser.objects.filter(email="esonnen@uwm.edu").first()
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing role")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing role")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing role")
        self.assertEqual(self.emmaSonnen.role, "admin",
                         "role is edited in edituser when invalid")
        self.assertEqual(response.context["message"], "Invalid role. Can only be Admin, Instructor, or TA.",
                         "error message does not show for unsuccessful edit")
