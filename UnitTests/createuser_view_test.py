import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class CreatUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.henryRitchie = MyUser("writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                       "Milwaukee", "WI", 53026, "admin")

        self.henryRitchie.save()

    def test_GetTemplate(self):
        response = self.client.get('/createuser/')
        self.assertTemplateUsed(response, 'createuser.html')

    def test_GetSessionVars(self):
        response = self.client.get('/createuser/')
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at dashboard screen.")
        self.assertNotIn("selectedCourse", self.client.session,
                         "Session has selected course saved at dashboard screen.")
        self.assertNotIn("selectedSection", self.client.session,
                         "Session has selected section saved at dashboard screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")

    def test_PostLogout(self):
        response = self.client.post("/createuser/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/createuser/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/createuser/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/createuser/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_PostCancel(self):
        response = self.client.post("/createuser/", {"navigation": "cancel"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedCourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedSection", self.client.session, "Session has selected section saved at directory.")

    def test_CreateUserValid(self):
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
        self.assertEqual(newUser.zipcode, "53026", "User saved with wrong email")
        self.assertEqual(newUser.role, "ta", "User saved with wrong email")
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"], "User created successfully!",
                         "Message not played if successful user creation")

    def test_CreateUserInvalid(self):
        response = self.client.post("/createuser/",
                                    {"email": "writchie@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "WI",
                                     "zipcode": "53026",
                                     "role": "ta"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"], "Non-unique username. Please try again.",
                         "Error not played if nonunique usernames")
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
        self.assertEqual(response.context["message"], "Passwords do not match. Please try again.",
                         "Error not played if not matching passwords")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
                         "Invalid first name. Must start with a capital and have no spaces. Please try again.",
                         "Error not played if invalid firstname")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
                         "Invalid last name. Must start with a capital and have no spaces. Please try again.",
                         "Error not played if invalid lastname")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
                         "Invalid phone number. Must be 9 numbers 0-9. Please try again.",
                         "Error not played if invalid phonenumber")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
                         "Invalid street address. Please try again.",
                         "Error not played if invalid address")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
                         "Invalid city. Please try again.",
                         "Error not played if invalid city")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
                         "Invalid state. Please try again.",
                         "Error not played if invalid state")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
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
                         "Invalid zipcode. Please try again.",
                         "Error not played if invalid zipcode")
        response = self.client.post("/createuser/",
                                    {"email": "new@uwm.edu",
                                     "password": "password",
                                     "confirmpassword": "password",
                                     "firstname": "First",
                                     "lastname": "Last",
                                     "phonenumber": "5555555555",
                                     "streetaddress": "1234 Street rd",
                                     "city": "Milwaukee",
                                     "state": "W",
                                     "zipcode": "53026",
                                     "role": "student"}, follow=True)
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"],
                         "Invalid role. Please try again.",
                         "Error not played if invalid role")



