import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class SectionDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session["selectedsection"] = 1
        session.save()
        self.swe = Course(1,"Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section = Section(1, 100, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()

    def test_DeleteSectionValid(self):
        response = self.client.post("/sectionpage/", {'navigation': 'deletesection'}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertNotIn(self.section, Section.objects.all(), "Section not deleted")

        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when deleting section.")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when deleting section.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user when deleting section.")
        self.assertEqual(self.client.session["selectedcourse"], self.swe.id, "Selected course not saved when deleting course.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section when deleting section.")

    def test_DeletedSectionNotInList(self):
        response = self.client.post("/sectionpage/", {'navigation': 'deletesection'}, follow=True)
        displayed = any(section['title'] == "100 Lecture" for section in response.context['course']['sections'])
        self.assertFalse(displayed, "New section displayed in course page after deletion")

    def test_DeleteSectionNotAdmin(self):
        session = self.client.session
        session["email"] = "ballen@uwm.edu"
        session["role"] = "ta"
        session["selectedcourse"] = 1
        session.save()
        response = self.client.post("/sectionpage/", {"navigation": "deletesection"}, follow=True)
        self.assertTemplateUsed(response, 'sectionpage.html')
        self.assertIn(self.section, Section.objects.all(), "Section was deleted")
        self.assertEqual(self.client.session["email"], "ballen@uwm.edu",
                         "Email not saved when when non-admin tries to delete section")
        self.assertEqual(response.context["message"], "Only admins can delete sections!",
                         "Message not played if non-admin tries to delete section")
        self.assertEqual(self.client.session["role"], "ta", "Role not saved when non-admin tries to delete section")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when non-admin tries to delete section")
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user when non-admin tries to delete course.")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when non-admin tries to delete section")
