import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from django.test import TestCase, Client, RequestFactory

class CreateSectionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "writchie@uwm.edu"
        session["role"] = "admin"
        session["selectedcourse"] = 1
        session.save()
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.henry = MyUser(1, "writchie@uwm.edu", "Password!", "Henry", "Ritchie", "5555555555", "1234 main st",
                            "Milwaukee", "WI", 53026, "admin")
        self.henry.save()


    def test_GetCreateSectionNonAdmin(self):
        pass

    def test_CreateSectionValid(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     }, follow=True)
        newSection = Section.objects.filter().first()
        self.assertEqual(newSection.sectionNumber, 100, "Section saved with wrong sectionnumber")
        self.assertEqual(newSection.type, "lecture", "Section saved with wrong type")
        self.assertEqual(newSection.location, "180 Chemistry BLDG", "Section saved with wrong location")
        self.assertEqual(newSection.daysMeeting, "TH", "Section saved with wrong daysMeeting")
        self.assertEqual(newSection.startTime, "09:30", "Section saved with wrong startTime")
        self.assertEqual(newSection.endTime, "10:20", "Section saved with wrong endTime")
        self.assertEqual(newSection.course, self.swe, "Section saved with wrong course")
        self.assertTemplateUsed(response, 'createsection.html')

    def test_CreateSectionIsDisplayed(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     }, follow=True)
        response = self.client.get('/coursepage', follow=True)
        displayed = any(section['title'] == "100 Lecture" for section in response.context['course']['sections'])
        self.assertTrue(displayed, "New section not displayed in course page")


    def test_CreateSectionInvalidName(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": -100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "Error not played if invalid section number")
        self.assertEqual(Section.objects.filter(sectionNumber=-100).first(), None,
                         "Course made with invalid course number")

    def test_CreateSectionInvalidDaysMeeting(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "HT",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "Error not played if invalid daysmeeting")
        self.assertEqual(Section.objects.filter(daysMeeting='HT').first(), None,
                         "Course made with invalid daysmeeting")

    def test_CreateSectionInvalidLocation(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "Chemistry BLDG 180",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Location. Format: Room# Building Name",
                         "Error not played if invalid location")
        self.assertEqual(Section.objects.filter(location='Chemistry BLDG 180').first(), None,
                         "Course made with invalid location")

    def test_CreateSectionInvalidLocation(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "section",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "10:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Type. Must be lecture, lab, or grader.",
                         "Error not played if invalid type")
        self.assertEqual(Section.objects.filter(type='section').first(), None,
                         "Course made with invalid section")

    def test_CreateSectionInvalidStartTime(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "05:30",
                                     "endtime": "10:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Error not played if invalid time")
        self.assertEqual(Section.objects.filter(startTime='05:30').first(), None,
                         "Course made with invalid section")

    def test_CreateSectionInvalidEndTime(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "21:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Error not played if invalid time")
        self.assertEqual(Section.objects.filter(endTime='21:20').first(), None,
                         "Course made with invalid section")

    def test_CreateSectionInvalidEndBeforeStart(self):
        response = self.client.post("/createsection/",
                                    {"sectionnumber": 100,
                                     "type": "lecture",
                                     "location": "180 Chemistry BLDG",
                                     "daysmeeting": "TH",
                                     "starttime": "09:30",
                                     "endtime": "8:20",
                                     "course": self.client.session['selectedcourse'],
                                     }, follow=True)
        self.assertTemplateUsed(response, 'createsection.html')
        self.assertEqual(response.context["message"], "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Error not played if invalid time")
        self.assertEqual(Section.objects.filter(endTime='8:20').first(), None,
                         "Course made with invalid section")
