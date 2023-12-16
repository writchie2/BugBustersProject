import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.henryRitchie = MyUser(1,"writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
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

    def test_PostCreateUserValid(self):
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
        self.assertTemplateUsed(response, 'createuser.html')
        self.assertEqual(response.context["message"], "User created successfully!",
                         "Message not played if successful user creation")

    def test_PostCreateUserInvalid(self):
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



