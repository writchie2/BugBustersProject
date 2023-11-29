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

    def test_GetTemplate(self):
        response = self.client.get('/edituser/')
        self.assertTemplateUsed(response, 'edituser.html')

    def test_GetSessionVars(self):
        response = self.client.get('/edituser/')
        self.assertNotIn("selectedCourse", self.client.session,
                         "Session has selected course saved at edituser screen.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section saved at edituser screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to edituser")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when navigating to edituser")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when navigating to edituser")
    def test_PostLogout(self):
        response = self.client.post("/edituser/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/edituser/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/edituser/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to directory")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/edituser/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at dashboard.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at dashboard.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at dashboard.")

    def test_PostCancel(self):
        response = self.client.post("/edituser/", {"navigation": "cancel"}, follow=True)
        self.assertTemplateUsed(response, 'userpage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when edit cancel")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostEditFirstNameValid(self):
        response = self.client.post("/edituser/", {"firstname": "Nancy"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing firstname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing firstname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing firstname")
        self.assertEqual(response.context["message"], "First name changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditFirstNameInvalid(self):
        response = self.client.post("/edituser/", {"firstname": "nancy"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing firstname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing firstname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing firstname")
        self.assertEqual(response.context["message"], "Invalid first name. Must be capitalized and have only contain letters.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditLastNameValid(self):
        response = self.client.post("/edituser/", {"lastname": "Drew"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing lastname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing lastname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing lastname")
        self.assertEqual(response.context["message"], "Last name changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditLastNameInvalid(self):
        response = self.client.post("/edituser/", {"lastname": "drew"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing lastname")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing lastname")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing lastname")
        self.assertEqual(response.context["message"], "Invalid First Name. Must be capitalized and have only contain letters.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditPhoneNumberValid(self):
        response = self.client.post("/edituser/", {"phonenumber": "4145555555"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing phonenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing phonenumber")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing phonenumber")
        self.assertEqual(response.context["message"], "Phone number changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditPhoneNumberInvalid(self):
        response = self.client.post("/edituser/", {"phonenumber": "55555"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing phonenumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing phonenumber")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing phonenumber")
        self.assertEqual(response.context["message"], "Invalid phone number. Format is 123-456-7890",
                         "error message does not show for unsuccessful edit")

    def test_PostEditStreetAddressValid(self):
        response = self.client.post("/edituser/", {"streetaddress": "324 Maple rd"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing streetaddress")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing streetaddress")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing streetaddress")
        self.assertEqual(response.context["message"], "Street address changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditStreetAddressInvalid(self):
        response = self.client.post("/edituser/", {"streetaddress": "1234"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing streetaddress")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing streetaddress")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing streetaddress")
        self.assertEqual(response.context["message"], "Invalid street address.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditCityValid(self):
        response = self.client.post("/edituser/", {"city": "Chicago"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing city")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing city")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing city")
        self.assertEqual(response.context["message"], "City changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditCityInvalid(self):
        response = self.client.post("/edituser/", {"city": "chicago"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing city")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing city")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing city")
        self.assertEqual(response.context["message"], "Invalid city. Must be capitalized.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditStateValid(self):
        response = self.client.post("/edituser/", {"state": "IL"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing state")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing state")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing state")
        self.assertEqual(response.context["message"], "State changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditStateInvalid(self):
        response = self.client.post("/edituser/", {"state": "il"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing state")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing state")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing state")
        self.assertEqual(response.context["message"], "Invalid state. Two letter state code only.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditZipcodeValid(self):
        response = self.client.post("/edituser/", {"zipcode": "53022"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing zipcode")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing zipcode")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing zipcode")
        self.assertEqual(response.context["message"], "Zipcode changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditZipcodeInvalid(self):
        response = self.client.post("/edituser/", {"zipcode": "1234"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing zipcode")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing zipcode")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing zipcode")
        self.assertEqual(response.context["message"], "Invalid zipcode. Must be 5 digits long.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditRoleValid(self):
        response = self.client.post("/edituser/", {"role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing role")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing role")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing role")
        self.assertEqual(response.context["message"], "Role changed successfully!",
                         "success message does not show for successful edit")

    def test_PostEditRoleInvalid(self):
        response = self.client.post("/edituser/", {"role": "student"}, follow=True)
        self.assertTemplateUsed(response, 'edituser.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing role")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing role")
        self.assertEqual(self.client.session["selecteduser"], "esonnen@uwm.edu",
                         "selected user not saved when editing role")
        self.assertEqual(response.context["message"], "Invalid role. Can only be Admin, Instructor, or TA.",
                         "error message does not show for unsuccessful edit")
