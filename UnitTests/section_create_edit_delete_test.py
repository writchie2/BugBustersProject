import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.functions import func_Login
from django.test import TestCase, Client, RequestFactory

class SectionCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session.save()
        self.swe = Course(1, "Introduction to Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section = Section(1, 100, 'lecture', "180 Chemistry BLDG", "TH", "09:30", "10:20", self.swe.id)
        self.section.save()
        session["selectedcourse"] = self.swe.id
        session["selectedsection"] = self.section.id
        session.save()

    def test_CreateSectionValid(self):
        response = self.client.post('/createsection/',
                                    {"sectionnumber": 200, "type": 'lab', "location": 'S195 Lubar Hall',
                                     "daysmeeting": 'M', "starttime": "14:30", "endtime": "16:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Section created successfully!",
                         "Success message not displayed after section creation")

        newSection = Section.objects.filter(sectionNumber=200).first()
        self.assertNotEqual(None, newSection, "Section not added to database.")
        self.assertEqual(newSection.type, "lab", "Section created with incorrect type")
        self.assertEqual(newSection.location, "S195 Lubar Hall", "Section created with incorrect location")
        self.assertEqual(newSection.daysMeeting, "M", "Section created with incorrect daysmeeting")
        self.assertEqual(newSection.startTime, "14:30", "Section created with incorrect starttime")
        self.assertEqual(newSection.endTime, "16:20", "Section created with incorrect endtime")
        self.assertEqual(newSection.course, self.swe, "Section created with incorrect course foreignkey")

    def test_CreateSectionInvalidSectionNumber(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '0', "type": 'lab', "location": 'S195 Lubar Hall',
                                 "daysmeeting": 'T', "starttime": "14:30", "endtime": "16:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Section Number. Must be between 100 and 999 and unique!",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=0).first(), "Section added to database after invalid creation.")

    def test_CreateSectionInvalidType(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '200', "type": 'le', "location": 'S195 Lubar Hall',
                                 "daysmeeting": 'T', "starttime": "14:30", "endtime": "16:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Type. Must be lecture, section, or grader.",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=200).first(), "Section added to database after invalid creation.")

    def test_CreateSectionInvalidDaysMeeting(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '200', "type": 'lecture', "location": 'S195 Lubar Hall',
                                 "daysmeeting": 'TM', "starttime": "14:30", "endtime": "16:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=200).first(), "Section added to database after invalid creation.")

    def test_CreateSectionInvalidLocation(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '200', "type": 'lecture', "location": 'Lubar Hall',
                                 "daysmeeting": 'T', "starttime": "14:30", "endtime": "16:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Location. Format: Room# Building Name",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=200).first(), "Section added to database after invalid creation.")

    def test_CreateSectionInvalidStartTime(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '200', "type": 'lecture', "location": 'S195 Lubar Hall',
                                 "daysmeeting": 'T', "starttime": "18:30", "endtime": "19:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=200).first(), "Section added to database after invalid creation.")

    def test_CreateSectionInvalidEndTime(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '200', "type": 'lecture', "location": 'S195 Lubar Hall',
                                 "daysmeeting": 'T', "starttime": "17:30", "endtime": "20:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=200).first(), "Section added to database after invalid creation.")

    def test_CreateSectionInvalidEndBeforeStart(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '200', "type": 'lecture', "location": 'S195 Lubar Hall',
                                 "daysmeeting": 'T', "starttime": "12:30", "endtime": "11:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=200).first(), "Section added to database after invalid creation.")

    def test_CreateSectionInvalidBlankField(self):
        response = self.client.post('/createsection/',
                                {"sectionnumber": '200', "type": 'lecture',
                                 "daysmeeting": 'T', "starttime": "12:30", "endtime": "11:20"}, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Please fill out all fields!",
                     "Error message not displayed after section creation failure")
        self.assertEqual(None, Section.objects.filter(sectionNumber=200).first(), "Section added to database after invalid creation.")

class SectionEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session["selectedsection"] = 2
        session.save()
        self.swe = Course(1, "Introduction to Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section = Section(2, 100, 'lecture', "180 Chemistry BLDG", "TH", "09:30", "10:20", self.swe.id)
        self.section.save()
        session["selectedcourse"] = self.swe.id
        session["selectedsection"] = self.section.id
        session.save()

    def test_EditNumberValid(self):
        response = self.client.post('/editsection/', {"sectionnumber": "600"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.sectionNumber, 600, "Section Number not edited")
        self.assertEqual(response.context['message'], "Section Number edited successfully!")

    def test_EditNumberInvalid(self):
        response = self.client.post('/editsection/', {"sectionnumber":"0"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.sectionNumber, 100, "Section Number edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Section Number. Must be between 100 and 999 and unique!")

    def test_EditLocationValid(self):
        response = self.client.post('/editsection/', {"location": "600 EMS"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.location, '600 EMS', "Location not edited")
        self.assertEqual(response.context['message'], "Location edited successfully!")

    def test_EditLocationInvalid(self):
        response = self.client.post('/editsection/', {"location": "EMS"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.location, '180 Chemistry BLDG', "Location edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Location. Format: Room# Building Name")

    def test_EditDaysMeetingValid(self):
        response = self.client.post('/editsection/', {"daysmeeting": "MW"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.daysMeeting, 'MW', "Days Meeting not edited")
        self.assertEqual(response.context['message'], "Days Meeting edited successfully!")

    def test_EditDaysMeetingInvalid(self):
        response = self.client.post('/editsection/', {"daysmeeting": "WM"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.daysMeeting, 'TH', "Days Meeting edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.")

    def test_EditStartTimeValid(self):
        response = self.client.post('/editsection/', {"starttime": "09:00"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.startTime, "09:00", "Start time not edited")
        self.assertEqual(response.context['message'], "Start Time edited successfully!")

    def test_EditStartTimeInvalid(self):
        response = self.client.post('/editsection/', {"starttime": "05:00"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.startTime, "09:30", "Start Time edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.")

    def test_EditEndTimeValid(self):
        response = self.client.post('/editsection/', {"endtime": "11:00"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.endTime, "11:00", "End Time not edited")
        self.assertEqual(response.context['message'], "End Time edited successfully!")

    def test_EditEndTimeInvalid(self):
        response = self.client.post('/editsection/', {"endtime": "22:00"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.endTime, "10:20", "End Time edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.")

    def test_EditSectionTypeValid(self):
        response = self.client.post('/editsection/', {"type": "grader"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.type, 'grader', "Type not edited")
        self.assertEqual(response.context['message'], "Type edited successfully!")

    def test_EditSectionTypeInvalid(self):
        response = self.client.post('/editsection/', {"type": "section"}, follow=True)
        editSection = Section.objects.filter(id=2).first()
        self.assertTemplateUsed(response, 'editsection.html')
        self.assertEqual(editSection.type, 'lecture', "Lecture edited when invalid")
        self.assertEqual(response.context['message'], "Invalid Type. Must be lecture, section, or grader.")

class SectionDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        self.swe = Course(1, "Introduction to Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.section = Section(2, 100, 'lecture', "180 Chemistry BLDG", "TH", "09:30", "10:20", self.swe.id)
        self.section.save()
        session["selectedcourse"] = self.swe.id
        session["selectedsection"] = self.section.id
        session.save()

    def test_DeleteSectionSuccess(self):
        response = self.client.post('/sectionpage/', {"navigation": "deletesection"}, follow=True)
        self.assertTemplateUsed(response,'coursepage.html')
        self.assertEqual(Section.objects.filter(id=self.section.id).first(), None, "Section not deleted from database when valid")

    def test_DeleteSectionNotAdmin(self):
        session = self.client.session
        session['role'] = 'ta'
        session.save()
        response = self.client.post('/sectionpage/', {"navigation": "deletesection"}, follow=True)
        self.assertTemplateUsed(response,'sectionpage.html')
        self.assertEqual(Section.objects.filter(id=self.section.id).first(), self.section, "Section is deleted from database when non admin tries to delete")
        self.assertEqual(response.context['message'], "Only admins can delete sections!",
                             "Error does not show when non admin tries to delete")

