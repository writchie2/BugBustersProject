import sys

sys.path.append('../SchedulingApp')
from SchedulingApp.models import MyUser, Course, Section
from SchedulingApp.Model_Classes.Section_Functions import (
    func_SectionCreator,
    func_SectionDeleter,
    func_AssignUserToSection,
    func_RemoveSectionUser,
    func_UserIsInstructorOfSection,
    func_EditSectionNumber,
    func_EditType,
    func_EditLocation,
    func_EditDaysMeeting,
    func_EditStartTime,
    func_EditEndTime
)
from django.test import TestCase


class TestSectionCreator(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", "spring", 2023)
        self.newCourse.save()
        self.newSection = Section.objects.create(2, 200, "section", "1020 Kenwood", "M", "15:00", "16:00")
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
        with self.assertRaises(Exception, msg="Adding to non-existent course does not raise an exception."):
            func_SectionCreator(100, 5, "TH", "E108 CHEM BLDG", "lecture", "14:30", "16:20")

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
        self.newSection = Section(2, 200, "section", "1020 Kenwood", "M", "15:00", "16:00", None, self.newCourse)
        self.newSection.save()
        self.erik = MyUser(1, "erikshen@uwm.edu", "Qwerty-12345", "Erik", "Shen", "123-456-7890",
                           "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "admin")
        self.erik.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "123-456-7890",
                            "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "admin")
        self.henry.save()
        self.newCourse.add(self.erik, self.henry)
        self.newCourse.save()
        self.newSection.add(self.erik)
        self.newSection.save()

    def test_ValidAssignUser(self):
        message = func_AssignUserToSection('writchie@uwm.edu', 2)
        self.assertEqual(message, "User added successfully!")
        self.assertIn(self.henry, self.newSection.assignedUser.all(), "User not added to section's users")

    def test_AssignUserAlreadyIn(self):
        message = func_AssignUserToSection("erikshen@uwm.edu", 2)
        self.assertEqual(message, "User is already in the section!")

    def test_AssignUserNonexistantUser(self):
        message = func_AssignUserToSection("mystery@uwm.edu", 2)
        self.assertEqual(message, "User does not exist!")

    def test_AssignUserNonexistantSection(self):
        message = func_AssignUserToSection("writchie@uwm.edu", 3)
        self.assertEqual(message, "This section does not exist!")


class TestRemoveSectionUser(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Test", "Department", 100, "spring", 2023)
        self.newCourse.save()
        self.newSection = Section(2, 200, "section", "1020 Kenwood", "M", "15:00", "16:00", None, self.newCourse)
        self.newSection.save()
        self.erik = MyUser(1, "erikshen@uwm.edu", "Qwerty-12345", "Erik", "Shen", "123-456-7890", "3400 N Maryland Ave",
                           "Milwaukee", "WI", "53211", "admin")
        self.erik.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "123-456-7890",
                            "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "admin")
        self.henry.save()
        self.newCourse.assignedUser.add(self.erik, self.henry)
        self.newCourse.save()
        self.newSection.assignedUser.add(self.erik)
        self.newSection.save()

    def test_ValidRemoveUser(self):
        message = func_RemoveSectionUser('erikshen@uwm.edu', 2)
        self.assertEqual(message, "User removed successfully!")
        self.assertNotIn(self.erik, self.swe.assignedUser.all(), "User not removed from section's users")

    def test_AssignUserNotIn(self):
        message = func_RemoveSectionUser('writchie@uwm.edu', 2)
        self.assertEqual(message, "User is not in the section!")

    def test_AssignUserNonexistantUser(self):
        message = func_RemoveSectionUser('mystery@uwm.edu', 2)
        self.assertEqual(message, "User does not exist!")

    def test_AssignUserNonexistantSection(self):
        message = func_RemoveSectionUser('erikshen@uwm.edu', 3)
        self.assertEqual(message, "This section does not exist!")


class TestUserIsInstructorOfSection(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Test", "Department", 100, "spring", 2023)
        self.newCourse.save()
        self.newSection = Section(2, 200, "section", "1020 Kenwood", "M", "15:00", "16:00", None, self.newCourse)
        self.newSection.save()
        self.erik = MyUser(1, "erikshen@uwm.edu", "Qwerty-12345", "Erik", "Shen", "123-456-7890",
                           "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "instructor")
        self.erik.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "123-456-7890",
                            "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "instructor")
        self.henry.save()
        self.sarah = MyUser(3, "scramer@uwm.edu", "password", "Sarah", "Cramer", "123-456-7890",
                            "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "ta")
        self.sarah.save()
        self.bob = MyUser(4, "ballen@uwm.edu", "password", "Bob", "Allen", "123-456-7890",
                          "3400 N Maryland Ave", "Milwaukee", "WI", "53211", "admin")
        self.bob.save()
        self.newCourse.assignedUser.add(self.erik, self.henry, self.sarah, self.bob)
        self.newCourse.save()
        self.newSection.assignedUser.add(self.erik, self.sarah)
        self.newSection.save()

        def test_IsInstructorInSection(self):
            result = func_UserIsInstructorOfSection('erikshen@uwm.edu', 1, 2)
            self.assertEqual(result, 'True', "True not passed for instructor of section")

        def test_InstructorNotInSection(self):
            result = func_UserIsInstructorOfSection('writchie@uwm.edu', 1, 2)
            self.assertEqual(result, 'False', "False not passed for instructor not in course")

        def test_TAInSection(self):
            result = func_UserIsInstructorOfSection('scramer@uwm.edu', 1, 2)
            self.assertEqual(result, 'False', "False not passed for TA in section")

        def test_AdminNotInSection(self):
            result = func_UserIsInstructorOfSection('ballen@uwm.edu', 1, 2)
            self.assertEqual(result, 'False', "False not passed for admin not in section")

        def test_NonexistantUser(self):
            result = func_UserIsInstructorOfSection('mystery@uwm.edu', 1, 2)
            self.assertEqual(result, 'User does not exist!', "False not passed for admin not in section")

        def test_NonexistantSection(self):
            result = func_UserIsInstructorOfSection('writchie@uwm.edu', 1, 3)
            self.assertEqual(result, 'This section does not exist!', "False not passed for admin not in section")


class TestEditSectionNumber(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "section", "1020 Kenwood", "M", "15:00", "16:00", None, self.newCourse)
        self.newSection.save()

    def test_EditNumberValid(self):
        message = func_EditSectionNumber(802, 1)
        self.assertEqual(message, 'Section Number edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id="1").sectionNumber, '802', 'section number not changed')

        message = func_EditSectionNumber(804, 1)
        self.assertEqual(message, 'Section Number edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id="1").sectionNumber, '804', 'section number not changed')

    def test_EditNumberInvalidNumber(self):
        message = func_EditSectionNumber('', 1)
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!", "error message does not play for invalid section number")
        self.assertEqual(Section.objects.get(id=1).sectionNumber, '800', 'section number changed when invalid')

        message = func_EditSectionNumber('99', 1)
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!", "error message does not play for invalid section number")
        self.assertEqual(Section.objects.get(id=1).sectionNumber, '800', 'section number changed when invalid')

        message = func_EditSectionNumber('1000', 1)
        self.assertEqual(message, "Invalid Section Number. Must be between 100 and 999 and unique!", "error message does not play for invalid section number")
        self.assertEqual(Section.objects.get(id=1).sectionNumber, '800', 'section number changed when invalid')

    def test_EditNumberInvalidSection(self):
        message = func_EditSectionNumber('802', 2)
        self.assertEqual(message, "Section does not exist!", "error message does not play for invalid sectionID")


class TestEditType(TestCase):
    def setUp(self):
        self.newCourse = Course(1, "Software Engineering", "COMPSCI", "361", 2023)
        self.newCourse.save()
        self.newSection = Section(1, 800, "section", "1020 Kenwood", "M", "15:00", "16:00", None, self.newCourse)
        self.newSection.save()

    def test_EditTypeValid(self):
        message = func_EditType('lecture', 1)
        self.assertEqual(message, 'Type edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id="1").type, 'lecture', 'section number not changed')

        message = func_EditType('lab', 1)
        self.assertEqual(message, 'Type edited successfully!', "success message does not play")
        self.assertEqual(Section.objects.get(id="1").type, 'lab', 'section number not changed')

    def test_EditTypeInvalid(self):
        message = func_EditType('Lecture', 1)
        self.assertEqual(message, 'Invalid Type. Must be lecture, lab, or grader.', "error message does not play for invalid course department")
        self.assertEqual(Section.objects.get(id="1").type, 'lecture', 'section type changed when invalid')

        message = func_EditType('labs', 1)
        self.assertEqual(message, 'Invalid Type. Must be lecture, lab, or grader.',
                         "error message does not play for invalid course department")
        self.assertEqual(Section.objects.get(id="1").type, 'lecture', 'section type changed when invalid')

        message = func_EditType('', 1)
        self.assertEqual(message, 'Invalid Type. Must be lecture, lab, or grader.',
                         "error message does not play for invalid course department")
        self.assertEqual(Section.objects.get(id="1").type, 'lecture', 'section type changed when invalid')

    def test_EditTypeInvalidSection(self):
        message = func_EditType('lecture', 2)
        self.assertEqual(message, 'Invalid Type. Must be lecture, lab, or grader.',
                         "error message does not play for invalid course department")
        self.assertEqual(Section.objects.get(id="1").type, 'lecture', 'section type changed when invalid')


class TestEditLocation(TestCase):
    pass


class TestEditDaysMeeting(TestCase):
    pass


class TestEditStartTime(TestCase):
    pass


class TestEditEndTime(TestCase):
    pass


class TestRemoveSection(TestCase):
    def setUp(self):
        self.newCourse = Course.objects.create(id=1, name="Test", department="Department", courseNumber=100,
                                               semester="spring", year=2023)
        self.newCourse.save()
        self.newSection = Section.objects.create(id=2, sectionNumber=200, type="section", location="1020 Kenwood",
                                                 daysMeeting="M", startTime="15:00", endTime="16:00",
                                                 assignedUser=None,
                                                 course=self.newCourse)
        self.newSection.save()
        self.newSection = Section.objects.create(id=3, sectionNumber=300, type="section", location="2020 Kenwood",
                                                 daysMeeting="W", startTime="15:00", endTime="16:00",
                                                 assignedUser=None,
                                                 course=self.newCourse)
        self.newSection.save()

    def test_validremovesection(self):
        message = func_SectionDeleter(3)
        self.assertEqual(message, "Section deleted successfully")

    def test_invalidsectionid(self):
        with self.assertRaises(Exception, msg="Removing from non-existent course does not raise an exception."):
            func_SectionDeleter(5)

    def test_nosectionid(self):
        with self.assertRaises(Exception, msg="Removing from empty course does not raise an exception."):
            func_SectionDeleter(None)

    def test_removedoublesection(self):
        message = func_SectionDeleter(3)
        self.assertEqual(message, "Section deleted successfully")
        with self.assertRaises(Exception, msg="Removing section multiple times does not raise an exception."):
            func_SectionDeleter(3)
