import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

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
        self.assertNotIn(self.emma, MyUser.objects.all(), "User not deleted")

        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when deleting section.")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when deleting user.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user when deleting user.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course when deleting user.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section when deleting user.")


    def test_DeleteUserNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session.save()
        response = self.client.post('/userpage/', {"navigation": "deleteuser"}, follow=True)
        self.assertTemplateUsed(response,'userpage.html')
        self.assertIn(self.emma, MyUser.objects.all(), "User was deleted")
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to delete section")
        self.assertEqual(response.context['message'], "Only admins can delete users!",
                             "Error does not show when non admin tries to delete")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to delete user")
        self.assertEqual(self.client.session["selecteduser"], 'esonnen@uwm.edu',
                         "selected user not saved when non-admin tries to delete user")
        self.assertNotIn("selectedcourse", self.client.session,
                         "Session has selected course when non-admin tries to delete user.")
        self.assertNotIn("selectedsection", self.client.session,
                         "Session has selected section when non-admin tries to delete user.")