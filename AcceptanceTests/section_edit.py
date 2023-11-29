import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory
class EditUserPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session["selectedsection"] = 1
        session.save()
        self.swe = Course(1, "SWE", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section = Section(1, 100, 'lecture', "Chemistry BLDG 180", "TH", "09:30", "10:20", self.swe.id)
        self.section.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()

    def test_EditSectionNumberValid(self):
        response = self.client.post("/editsection/", {"sectionnumber": 200}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing sectionnumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing sectionnumber")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing sectionnumber")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing sectionnumber")
        self.assertEqual(self.section.sectionNumber, 200,
                         "Section Number not edited in editsection when valid")
        self.assertEqual(response.context["message"], "Section Number edited successfully!",
                         "success message does not show for successful edit")

    def test_EditSectionNumberInvalid(self):
        response = self.client.post("/editsection/", {"sectionnumber": -100}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing sectionnumber")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing sectionnumber")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing sectionnumber")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing sectionnumber")
        self.assertEqual(self.section.sectionNumber, 100,
                         "Section Number edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "error message does not show for unsuccessful edit")

    def test_EditLocationValid(self):
        response = self.client.post("/editsection/", {"location": "190 Chemistry BLDG"}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing location")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing location")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing location")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing location")
        self.assertEqual(self.section.location, "190 Chemistry BLDG",
                         "Location not edited in location when valid")
        self.assertEqual(response.context["message"], "Location edited successfully!",
                         "success message does not show for successful edit")

    def test_EditLocationInvalid(self):
        response = self.client.post("/editsection/", {"location": ''}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing location")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing location")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing location")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing location")
        self.assertEqual(self.section.location, "Chemistry BLDG 180",
                         "Location edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid Location. Format: Room# Building Name",
                         "error message does not show for unsuccessful edit")

    def test_EditDaysMeetingValid(self):
        response = self.client.post("/editsection/", {"daysmeeting": "MW"}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing daysmeeting")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing daysmeeting")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing daysmeeting")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing daysmeeting")
        self.assertEqual(self.section.daysMeeting, "MW",
                         "Days Meeting not edited in location when valid")
        self.assertEqual(response.context["message"], "Days Meeting edited successfully!",
                         "success message does not show for successful edit")

    def test_EditDaysMeetingInvalid(self):
        response = self.client.post("/editsection/", {"daysmeeting": ''}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing daysmeeting")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing daysmeeting")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing daysmeeting")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing daysmeeting")
        self.assertEqual(self.section.daysMeeting, "TH",
                         "Days Meeting edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "error message does not show for unsuccessful edit")

    def test_EditStartTimeValid(self):
        response = self.client.post("/editsection/", {"starttime": "08:00"}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing starttime")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing starttime")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing starttime")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing starttime")
        self.assertEqual(self.section.startTime, "08:00",
                         "Start Time not edited in location when valid")
        self.assertEqual(response.context["message"], "Start Time edited successfully!",
                         "success message does not show for successful edit")

    def test_EditStartTimeInvalid(self):
        response = self.client.post("/editsection/", {"starttime": ''}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing starttime")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing starttime")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing starttime")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing starttime")
        self.assertEqual(self.section.startTime, "09:30",
                         "Start Time edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not show for unsuccessful edit")


    def test_EditEndTimeValid(self):
        response = self.client.post("/editsection/", {"endtime": "12:00"}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing endtime")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing endtime")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing endtime")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing endtime")
        self.assertEqual(self.section.endTime, "12:00",
                         "End Time not edited in location when valid")
        self.assertEqual(response.context["message"], "End Time edited successfully!",
                         "success message does not show for successful edit")

    def test_EditEndTimeInvalid(self):
        response = self.client.post("/editsection/", {"endtime": ''}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing endtime")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing endtime")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing endtime")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing endtime")
        self.assertEqual(self.section.endTime, "10:20",
                         "End Time edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not show for unsuccessful edit")

    def test_EditTypeValid(self):
        response = self.client.post("/editsection/", {"type": "lab"}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing type")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing type")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing type")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing type")
        self.assertEqual(self.section.type, "lab",
                         "Type not edited in location when valid")
        self.assertEqual(response.context["message"], "Type edited successfully!",
                         "success message does not show for successful edit")

    def test_EditTypeInvalid(self):
        response = self.client.post("/editsection/", {"type": ''}, follow=True)
        self.section = Section.objects.filter(id=1).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing type")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing type")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing type")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing type")
        self.assertEqual(self.section.type, "lecture",
                         "Type edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid Type. Must be lecture, lab, or grader.",
                         "error message does not show for unsuccessful edit")
