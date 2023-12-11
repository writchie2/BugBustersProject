import sys
sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.henry = MyUser(1,"writchie@uwm.edu", "Password!", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()
        self.session = self.client.session
        self.session["email"] = 'writchie@uwm.edu'
        self.session["role"] = 'admin'
        self.session["selecteduser"] = 'writchie@uwm.edu'
        self.session["selectedcourse"] = 1
        self.session["selectedsection"] = 1
        self.session.save()


    def test_Logout(self):
        view_list = ['/dashboard/', '/directory/', '/createuser/', '/userpage/', '/edituser/', '/courselist/', '/createcourse/', '/coursepage/','/editcourse/', '/createsection/', '/sectionpage/', '/editsection/']
        for view in view_list:
            response = self.client.post(view, {"navigation": "logout"}, follow=True)
            self.assertTemplateUsed(response, 'login.html')
            self.assertNotIn("email", self.client.session, "Session has email after logout." + "-" + view)
            self.assertNotIn("role", self.client.session, "Session has role after logout." + "-" + view)
            self.assertNotIn("selectedUser", self.client.session, "Session has selected user saved at logout screen." + "-" + view)
            self.assertNotIn("selectedCourse", self.client.session,
                             "Session has selected course saved at login screen." + "-" + view)
            self.assertNotIn("selectedSection", self.client.session,
                             "Session has selected section saved at login screen." + "-" + view)
            self.client.session["email"] = 'writchie@uwm.edu'
            self.client.session["role"] = 'admin'
            self.client.session["selecteduser"] = 'writchie@uwm.edu'
            self.client.session["selectedcourse"] = 1
            self.client.session["selectedsection"] = 1
            self.client.session.save()

    def test_GetLoginAlreadyLoggedIn(self):
        response = self.client.get('/login/', follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
