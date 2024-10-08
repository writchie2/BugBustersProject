import sys

sys.path.append('../../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.Model_Classes.Section_Functions import (
    func_SectionCreator,
    func_SectionDeleter,
    func_AssignUserToSection,
    func_RemoveSectionUser,
    func_EditSectionNumber,
    func_EditType,
    func_EditLocation,
    func_EditDaysMeeting,
    func_EditStartTime,
    func_EditEndTime,
    func_GetCourseFromSection
)
from django.test import TestCase


class TestSectionCreator(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", "spring", 2023)
        self.newCourse.save()
        self.newSection = Section(2, 200, "section", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()

    def test_ValidSection(self):
        message = func_SectionCreator(100, 1, "TH", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message, "Section created successfully!", "Proper success message is not returned")
        self.assertIn(Section.objects.filter(sectionNumber=100).first(), self.newCourse.section_set.all())

    def test_InvalidNumber(self):
        message = func_SectionCreator(200, 1, "TH", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "Proper error message is not returned")
        self.assertEqual(Section.objects.filter(sectionNumber=200).count(), 1,
                         "Section created with invalid section number")

        message = func_SectionCreator(99, 1, "TH", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "Proper error message is not returned")
        self.assertNotIn(Section.objects.filter(sectionNumber=99).first(), self.newCourse.section_set.all())

        message = func_SectionCreator(1000, 1, "TH", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "Proper error message is not returned")
        self.assertNotIn(Section.objects.filter(sectionNumber=1000).first(), self.newCourse.section_set.all())

    def test_InvalidSectionId(self):
        message = func_SectionCreator(100, 5, "TH", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message, "Course does not exist!")
        self.assertEqual(Section.objects.filter(id=3).first(), None)

    def test_InvalidSectionDays(self):
        message = func_SectionCreator(100, 1, "WM", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "Days that are not chronological should fail.")
        self.assertNotIn(Section.objects.filter(daysMeeting="WM").first(), self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "MA", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "Asynchronous with a day should fail.")
        self.assertNotIn(Section.objects.filter(daysMeeting="MA").first(), self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "", "E108 CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "No days selected should fail.")
        self.assertNotIn(Section.objects.filter(daysMeeting="").first(), self.newCourse.section_set.all())

    def test_InvalidSectionLocation(self):
        message = func_SectionCreator(100, 1, "M", "CHEM BLDG", "lecture", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Location. Format: Room# Building Name",
                         "Location without Room# should fail.")
        self.assertNotIn(Section.objects.filter(location="CHEM BLDG").first(), self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108", "lecture", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Location. Format: Room# Building Name",
                         "Location without Building Name should fail.")
        self.assertNotIn(Section.objects.filter(location="E108").first(), self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "", "lecture", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Location. Format: Room# Building Name",
                         "No section location should fail.")
        self.assertNotIn(Section.objects.filter(location="").first(), self.newCourse.section_set.all())

    def test_InvalidSectionType(self):
        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "Lecture", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Type. Must be lecture, lab, or grader.",
                         "Section type 'Lecture, Lab, or Grader' should fail.")
        self.assertNotIn(Section.objects.filter(type="Lecture").first(), self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "labs", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Type. Must be lecture, lab, or grader.",
                         "Unknown section type should fail.")
        self.assertNotIn(Section.objects.filter(type="labs").first(), self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "", "14:30", "16:20")
        self.assertEqual(message,
                         "Invalid Type. Must be lecture, lab, or grader.",
                         "No section type should fail.")
        self.assertNotIn(Section.objects.filter(type="").first(), self.newCourse.section_set.all())

    def test_InvalidSectionTimes(self):
        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "lecture", "7:30", "16:20")
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Start time before 8:00 should fail.")
        self.assertNotIn(Section.objects.filter(startTime="7:30", endTime="16:20").first(),
                         self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "lecture", "20:30", "16:20")
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Start time after 18:00 should fail.")
        self.assertNotIn(Section.objects.filter(startTime="20:30", endTime="16:20").first(),
                         self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "lecture", "", "16:20")
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Missing start time should fail.")
        self.assertNotIn(Section.objects.filter(startTime="", endTime="16:20").first(),
                         self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "lecture", "14:30", "12:20")
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Start time after end time should fail.")
        self.assertNotIn(Section.objects.filter(startTime="14:30", endTime="12:20").first(),
                         self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "lecture", "14:30", "22:20")
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "End time ending after 21:00 should fail.")
        self.assertNotIn(Section.objects.filter(startTime="14:30", endTime="22:20").first(),
                         self.newCourse.section_set.all())

        message = func_SectionCreator(100, 1, "M", "E108 CHEM BLDG", "lecture", "14:30", "")
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "Missing end time should fail.")
        self.assertNotIn(Section.objects.filter(startTime="14:30", endTime="").first(),
                         self.newCourse.section_set.all())


class TestAssignUserToSection(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Test", "Department", 100, "spring", 2023)
        self.newCourse.save()
        self.newSection = Section(2, 200, "section", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()
        self.erik = MyUser(1, "erikshen@uwm.edu", "Qwerty-12345", "Erik", "Shen", "123-456-7890",
                           "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "admin")
        self.erik.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "123-456-7890",
                            "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "admin")
        self.henry.save()
        self.newCourse.assignedUser.add(self.erik, self.henry)
        self.newCourse.save()
        self.newSection.assignedUser = self.erik
        self.newSection.save()

    def test_ValidAssignUser(self):
        message = func_AssignUserToSection('writchie@uwm.edu', 2)
        self.assertEqual(message, "There is already someone assigned to the section!")
        self.assertEqual(self.erik, self.newSection.assignedUser, "User not added to section's users")

    def test_AssignUserAlreadyIn(self):
        message = func_AssignUserToSection("erikshen@uwm.edu", 2)
        self.assertEqual(message, "User is already assigned to the section!")

    def test_AssignUserNonexistantUser(self):
        message = func_AssignUserToSection("mystery@uwm.edu", 2)
        self.assertEqual(message, "User does not exist!")

    def test_AssignUserNonexistantSection(self):
        message = func_AssignUserToSection("writchie@uwm.edu", 3)
        self.assertEqual(message, "Section does not exist!")


class TestRemoveSectionUser(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Test", "Department", 100, "spring", 2023)
        self.newCourse.save()
        self.newSection = Section(2, 200, "section", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()
        self.erik = MyUser(1, "erikshen@uwm.edu", "Qwerty-12345", "Erik", "Shen", "123-456-7890", "3400 N Maryland Ave",
                           "Milwaukee", "WI", "53211", "admin")
        self.erik.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "123-456-7890",
                            "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "admin")
        self.henry.save()
        self.newCourse.assignedUser.add(self.erik, self.henry)
        self.newCourse.save()
        self.newSection.assignedUser = self.erik
        self.newSection.save()

    def test_ValidRemoveUser(self):
        message = func_RemoveSectionUser('erikshen@uwm.edu', 2)
        self.assertEqual(message, "User removed successfully!")
        self.assertEqual(self.erik, self.newSection.assignedUser, "User not removed from section's users")

    def test_AssignUserNotIn(self):
        message = func_RemoveSectionUser('writchie@uwm.edu', 2)
        self.assertEqual(message, "User is not assigned to the section!")

    def test_AssignUserNonexistantUser(self):
        message = func_RemoveSectionUser('mystery@uwm.edu', 2)
        self.assertEqual(message, "User does not exist!")

    def test_AssignUserNonexistantSection(self):
        message = func_RemoveSectionUser('erikshen@uwm.edu', 3)
        self.assertEqual(message, "Section does not exist!")


class TestEditSectionNumber(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "section", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()

    def test_EditNumberValid(self):
        message = func_EditSectionNumber(802, 1)
        self.assertEqual(message, 'Section Number edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id="1").sectionNumber, 802, 'section number not changed')

        message = func_EditSectionNumber(804, 1)
        self.assertEqual(message, 'Section Number edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id="1").sectionNumber, 804, 'section number not changed')

    def test_EditNumberInvalidNumber(self):
        message = func_EditSectionNumber('', 1)
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "error message does not play for invalid section number")
        self.assertEqual(Section.objects.get(id=1).sectionNumber, 800, 'section number changed when invalid')

        message = func_EditSectionNumber('99', 1)
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "error message does not play for invalid section number")
        self.assertEqual(Section.objects.get(id=1).sectionNumber, 800, 'section number changed when invalid')

        message = func_EditSectionNumber('1000', 1)
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!",
                         "error message does not play for invalid section number")
        self.assertEqual(Section.objects.get(id=1).sectionNumber, 800, 'section number changed when invalid')

    def test_EditNumberInvalidSection(self):
        message = func_EditSectionNumber('802', 2)
        self.assertEqual(message, "Section does not exist!", "error message does not play for invalid sectionID")


class TestEditType(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "lab", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()

    def test_EditTypeValid(self):
        message = func_EditType('lecture', 1)
        self.assertEqual(message, 'Type edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).type, 'lecture', 'section type not changed')

        message = func_EditType('lab', 1)
        self.assertEqual(message, 'Type edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).type, 'lab', 'section type not changed')

    def test_EditTypeInvalid(self):
        message = func_EditType('Lecture', 1)
        self.assertEqual(message, 'Invalid Type. Must be lecture, lab, or grader.',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).type, 'lab', 'section type changed when invalid')

        message = func_EditType('labs', 1)
        self.assertEqual(message, 'Invalid Type. Must be lecture, lab, or grader.',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).type, 'lab', 'section type changed when invalid')

        message = func_EditType('', 1)
        self.assertEqual(message, 'Invalid Type. Must be lecture, lab, or grader.',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).type, 'lab', 'section type changed when invalid')

    def test_EditTypeInvalidSection(self):
        message = func_EditType('lecture', 2)
        self.assertEqual(message, 'Section does not exist!',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).type, 'lab', 'section type changed when invalid')


class TestEditLocation(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "lab", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()

    def test_EditLocationValid(self):
        message = func_EditLocation('1020 Kenwood', 1)
        self.assertEqual(message, 'Location edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).location, "1020 Kenwood", 'section location not changed')

        message = func_EditLocation('E108 Chemistry', 1)
        self.assertEqual(message, 'Location edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).location, 'E108 Chemistry', 'section location not changed')

    def test_EditLocationInvalid(self):
        message = func_EditLocation('Kenwood', 1)
        self.assertEqual(message, 'Invalid Location. Format: Room# Building Name',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).location, '1020 Kenwood', 'section location changed when invalid')

        message = func_EditLocation('1020', 1)
        self.assertEqual(message, 'Invalid Location. Format: Room# Building Name',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).location, '1020 Kenwood', 'section location changed when invalid')

        message = func_EditLocation('', 1)
        self.assertEqual(message, 'Invalid Location. Format: Room# Building Name',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).location, '1020 Kenwood', 'section location changed when invalid')

    def test_EditLocationInvalidSection(self):
        message = func_EditLocation('1020 Kenwood', 2)
        self.assertEqual(message, 'Section does not exist!',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).location, '1020 Kenwood', 'section location changed when invalid')


class TestEditDaysMeeting(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "lab", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()

    def test_EditDaysMeetingValid(self):
        message = func_EditDaysMeeting('M', 1)
        self.assertEqual(message, 'Days Meeting edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).daysMeeting, "M", 'section days not changed')

        message = func_EditDaysMeeting('TH', 1)
        self.assertEqual(message, 'Days Meeting edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).daysMeeting, 'TH', 'section days not changed')

        message = func_EditDaysMeeting('A', 1)
        self.assertEqual(message, 'Days Meeting edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).daysMeeting, 'A', 'section days not changed')

    def test_EditDaysMeetingInvalid(self):
        message = func_EditDaysMeeting('WM', 1)
        self.assertEqual(message,
                         "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).daysMeeting, 'M', 'section days changed when invalid')

        message = func_EditDaysMeeting('MA', 1)
        self.assertEqual(message,
                         "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).daysMeeting, 'M', 'section days changed when invalid')

        message = func_EditDaysMeeting('', 1)
        self.assertEqual(message,
                         "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).daysMeeting, 'M', 'section days changed when invalid')

    def test_EditDaysMeetingInvalidSection(self):
        message = func_EditDaysMeeting('M', 2)
        self.assertEqual(message, 'Section does not exist!',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).daysMeeting, 'M', 'section days changed when invalid')


class TestEditStartTime(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "lab", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()

    def test_EditStartTimeValid(self):
        message = func_EditStartTime('15:00', 1)
        self.assertEqual(message, 'Start Time edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).startTime, "15:00", 'section start time not changed')

        message = func_EditStartTime('8:00', 1)
        self.assertEqual(message, 'Start Time edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).startTime, '8:00', 'section start time not changed')

        message = func_EditStartTime('13:30', 1)
        self.assertEqual(message, 'Start Time edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).startTime, '13:30', 'section start time not changed')

    def test_EditStartTimeInvalid(self):
        message = func_EditStartTime('6:00', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).startTime, '15:00', 'section start time changed when invalid')

        message = func_EditStartTime('19:00', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).startTime, '15:00', 'section start time changed when invalid')

        message = func_EditStartTime('32:00', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).startTime, '15:00', 'section start time changed when invalid')

        message = func_EditStartTime('', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).startTime, '15:00', 'section start time changed when invalid')

    def test_EditStartTimeInvalidSection(self):
        message = func_EditStartTime('15:00', 2)
        self.assertEqual(message, 'Section does not exist!',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).startTime, '15:00', 'section start time changed when invalid')


class TestEditEndTime(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "lab", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()

    def test_EditEndTimeValid(self):
        message = func_EditEndTime('16:00', 1)
        self.assertEqual(message, 'End Time edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).endTime, "16:00", 'section end time not changed')

        message = func_EditEndTime('18:30', 1)
        self.assertEqual(message, 'End Time edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).endTime, "18:30", 'section end time not changed')

        message = func_EditEndTime('19:00', 1)
        self.assertEqual(message, 'End Time edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id=1).endTime, '19:00', 'section end time not changed')

    def test_EditEndTimeInvalid(self):
        message = func_EditEndTime('6:00', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).endTime, '16:00', 'section end time changed when invalid')

        message = func_EditEndTime('22:00', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).endTime, '16:00', 'section end time changed when invalid')

        message = func_EditEndTime('32:00', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).endTime, '16:00', 'section end time changed when invalid')

        message = func_EditEndTime('', 1)
        self.assertEqual(message,
                         "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end.",
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).endTime, '16:00', 'section end time changed when invalid')

    def test_EditEndTimeInvalidSection(self):
        message = func_EditEndTime('16:00', 2)
        self.assertEqual(message, 'Section does not exist!',
                         "error message does not play for invalid section type")
        self.assertEqual(Section.objects.get(id=1).endTime, '16:00', 'section end time changed when invalid')


class TestGetCourseFromSection(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "lab", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()
        self.newSectiontwo = Section(2, 401, "lecture", "E108 Chemistry", "MW", "9:30", "10:20", 1)
        self.newSectiontwo.save()

    def test_GetCourseFromSectionValid(self):
        func_GetCourseFromSection(2)
        self.assertEqual(Section.objects.get(id=2).course, Course.objects.get(id=1),
                         'section was not gotten when valid')

        func_GetCourseFromSection(1)
        self.assertEqual(Section.objects.get(id=1).course, Course.objects.get(id=1),
                         'section was not gotten when valid')

    def test_GetCourseFromSectionInvalid(self):
        message = func_GetCourseFromSection(3)
        self.assertEqual(message, 'Section does not exist!',
                         "error message does not play for invalid section from course")
        self.assertEqual(Section.objects.get(id=1).course, Course.objects.get(id=1), 'section gotten when invalid')


class TestSectionDeleter(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Test", "Department", 100, "spring", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "lab", "1020 Kenwood", "M", "15:00", "16:00", 1)
        self.newSection.save()
        self.newSectiontwo = Section(2, 401, "lecture", "E108 Chemistry", "MW", "9:30", "10:20", 1)
        self.newSectiontwo.save()

    def test_SectionDeleterValid(self):
        message = func_SectionDeleter(2)
        self.assertEqual(message, "Section deleted successfully")

    def test_SectionDeleterIDInvalid(self):
        message = func_SectionDeleter(5)
        self.assertEqual(message, "Section does not exist!")

    def test_SectionDeleterNoIDInvalid(self):
        message = func_SectionDeleter(None)
        self.assertEqual(message, "Section does not exist!")

    def test_SectionDeleterDoubleInvalid(self):
        message = func_SectionDeleter(2)
        self.assertEqual(message, "Section deleted successfully")
        message = func_SectionDeleter(2)
        self.assertEqual(message, "Section does not exist!")
