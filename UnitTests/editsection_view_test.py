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

    def test_GetTemplate(self):
        response = self.client.get('/editsection/')
        self.assertTemplateUsed(response, 'editsection.html')

    def test_GetSessionVars(self):
        response = self.client.get('/editsection/')
        self.assertNotIn("selecteduser", self.client.session,
                         "Session has selected user saved at editcourse screen.")
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when navigating to edituser")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when navigating to edituser")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when navigating to editcourse")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when navigating to editsection")
    def test_PostLogout(self):
        response = self.client.post("/editsection/", {"navigation": "logout"}, follow=True)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn("email", self.client.session, "Session has email after logout.")
        self.assertNotIn("role", self.client.session, "Session has role after logout.")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at logout screen.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at login screen.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at login screen.")

    def test_PostCourseList(self):
        response = self.client.post("/editsection/", {"navigation": "courselist"}, follow=True)
        self.assertTemplateUsed(response, 'courselist.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to courselist")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to courselist")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at courselist.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at courselist.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at courselist.")

    def test_PostDirectory(self):
        response = self.client.post("/editsection/", {"navigation": "directory"}, follow=True)
        self.assertTemplateUsed(response, 'directory.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to directory")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at direcotry.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at directory.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at directory.")

    def test_PostDashboard(self):
        response = self.client.post("/editsection/", {"navigation": "dashboard"}, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to dashboard")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to dashboard")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at dashboard.")
        self.assertNotIn("selectedcourse", self.client.session, "Session has selected course saved at dashboard.")
        self.assertNotIn("selectedsection", self.client.session, "Session has selected section saved at dashboard.")

    def test_PostCancel(self):
        response = self.client.post("/editsection/", {"navigation": "cancel"}, follow=True)
        self.assertTemplateUsed(response, 'sectionpage.html')
        self.assertEqual(self.client.session["email"], "writchie@uwm.edu",
                         "Email not saved when navigating to userpage")
        self.assertEqual(self.client.session["role"], "admin", "Role not saved when navigating to directory")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when edit cancel")
        self.assertNotIn("selecteduser", self.client.session, "Session has selected user saved at coursepage.")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when edit cancel")

    def test_PostEditSectionNumberValid(self):
        response = self.client.post("/editsection/", {"sectionnumber": 200}, follow=True)
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
        self.assertEqual(response.context["message"], "Section Number changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditSectionNumberInvalid(self):
        response = self.client.post("/editsection/", {"sectionnumber": -100}, follow=True)
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
        self.assertEqual(response.context["message"], "Invalid Section Number, Please try again.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditLocationValid(self):
        response = self.client.post("/editsection/", {"location": "Chemistry BLDG 190"}, follow=True)
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing location")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing location")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing location")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing location")
        self.assertEqual(self.section.location, "Chemistry BLDG 190",
                         "Location not edited in location when valid")
        self.assertEqual(response.context["message"], "Location changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditLocationInvalid(self):
        response = self.client.post("/editsection/", {"location": ''}, follow=True)
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
        self.assertEqual(response.context["message"], "Invalid Location, Please try again.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditDaysMeetingValid(self):
        response = self.client.post("/editsection/", {"daysmeeting": "MW"}, follow=True)
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
        self.assertEqual(response.context["message"], "Days Meeting changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditDaysMeetingInvalid(self):
        response = self.client.post("/editsection/", {"daysmeeting": ''}, follow=True)
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
        self.assertEqual(response.context["message"], "Invalid Meeting Days, Please try again.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditStartTimeValid(self):
        response = self.client.post("/editsection/", {"starttime": "12:00"}, follow=True)
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing starttime")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing starttime")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing starttime")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing starttime")
        self.assertEqual(self.section.startTime, "12:00",
                         "Start Time not edited in location when valid")
        self.assertEqual(response.context["message"], "Start Time changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditStartTimeInvalid(self):
        response = self.client.post("/editsection/", {"starttime": ''}, follow=True)
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing starttime")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing starttime")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing starttime")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing starttime")
        self.assertEqual(self.section.startTime, "09:20",
                         "Start Time edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid Start Time, Please try again.",
                         "error message does not show for unsuccessful edit")


    def test_PostEditEndTimeValid(self):
        response = self.client.post("/editsection/", {"endtime": "12:00"}, follow=True)
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
        self.assertEqual(response.context["message"], "End Time changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditEndTimeInvalid(self):
        response = self.client.post("/editsection/", {"endtime": ''}, follow=True)
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing endtime")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing endtime")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing endtime")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing endtime")
        self.assertEqual(self.section.endTime, "10:30",
                         "End Time edited in editsection when invalid")
        self.assertEqual(response.context["message"], "Invalid End Time, Please try again.",
                         "error message does not show for unsuccessful edit")

    def test_PostEditTypeValid(self):
        response = self.client.post("/editsection/", {"type": "section"}, follow=True)
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual("writchie@uwm.edu", self.client.session["email"],
                         "Email not saved when editing type")
        self.assertEqual(self.client.session["role"], "admin",
                         "Role not saved when editing type")
        self.assertEqual(self.client.session["selectedcourse"], 1,
                         "selected course not saved when editing type")
        self.assertEqual(self.client.session["selectedsection"], 1,
                         "selected section not saved when editing type")
        self.assertEqual(self.section.type, "section",
                         "Type not edited in location when valid")
        self.assertEqual(response.context["message"], "Type changed successfully",
                         "success message does not show for successful edit")

    def test_PostEditTypeInvalid(self):
        response = self.client.post("/editsection/", {"type": ''}, follow=True)
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
        self.assertEqual(response.context["message"], "Invalid Type, Please try again.",
                         "error message does not show for unsuccessful edit")
