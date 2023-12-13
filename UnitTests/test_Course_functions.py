import sys
from django.test import TestCase

from SchedulingApp.Model_Classes.Course_Functions import func_CourseCreator, func_AssignUserToCourse, \
    func_RemoveCourseUser, func_UserIsInstructorOfCourse, func_EditCourseName, func_EditDepartment, \
    func_EditCourseNumber, func_EditSemester, func_EditYear, func_CourseDeleter
from SchedulingApp.models import Course, MyUser

sys.path.append('../SchedulingApp')

class TestCourseCreator(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_ValidCourse(self):
        message = func_CourseCreator("Computer Architecture", "COMPSCI", 451, "spring", 2023)
        self.assertEqual(message, "Course created successfully!", "Proper success message is not returned")
        self.assertNotEqual(Course.objects.filter(name='Computer Architecture').first(), None, "Course did not get created")

    def test_InvalidName(self):
        message = func_CourseCreator("computer architecture", "COMPSCI", 451, "spring", 2023)
        self.assertEqual(message, "Invalid Course Name. Only letters and single spaces are allowed.", "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(name='computer architecture').first(), None, "Course created with invalid name")

        message = func_CourseCreator("", "COMPSCI", 451, "spring", 2023)
        self.assertEqual(message, "Invalid Course Name. Only letters and single spaces are allowed.",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(name='').first(), None,
                         "Course created with invalid name")

        message = func_CourseCreator("Computer   Architecture", "COMPSCI", 451, "spring", 2023)
        self.assertEqual(message, "Invalid Course Name. Only letters and single spaces are allowed.",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(name='Computer   Architecture').first(), None,
                         "Course created with invalid name")

        message = func_CourseCreator("Computer 4rchitecture", "COMPSCI", 451, "spring", 2023)
        self.assertEqual(message, "Invalid Course Name. Only letters and single spaces are allowed.",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(name='Computer   Architecture').first(), None,
                         "Course created with invalid name")

    def test_InvalidDepartment(self):
        message = func_CourseCreator("Computer Architecture", "compsci", 451, "spring", 2023)
        self.assertEqual(message, "Invalid Department. All Departments come from the UWM course cataloge.", "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(department='compsci').first(), None, "Course created with invalid department")

        message = func_CourseCreator("Computer Architecture", " COMPSCI", 451, "spring", 2023)
        self.assertEqual(message, "Invalid Department. All Departments come from the UWM course cataloge.",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(department=' COMPSCI').first(), None,
                         "Course created with invalid department")

    def test_InvalidNumber(self):
        message = func_CourseCreator("Computer Architecture", "COMPSCI", 99, "spring", 2023)
        self.assertEqual(message, "Invalid Course Number. Must be between 100 and 999 and unique.", "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(courseNumber=99).first(), None, "Course created with invalid course number")

        message = func_CourseCreator("Computer Architecture", "COMPSCI", 1000, "spring", 2023)
        self.assertEqual(message, "Invalid Course Number. Must be between 100 and 999 and unique.",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(courseNumber=1000).first(), None,
                         "Course created with invalid course number")

        message = func_CourseCreator("Computer Architecture", "COMPSCI", 361, "spring", 2023)
        self.assertEqual(message, "Invalid Course Number. Must be between 100 and 999 and unique.",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(courseNumber=361).count(), 1,
                         "Course created with invalid course number")

    def test_InvalidSemester(self):
        message = func_CourseCreator("Computer Architecture", "COMPSCI", 451, "Spring", 2023)
        self.assertEqual(message, "Invalid Semester. Acceptable values are fall, spring, winter, and summer", "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(semester='Spring').first(), None, "Course created with invalid semester")

        message = func_CourseCreator("Computer Architecture", "COMPSCI", 451, "autumn", 2023)
        self.assertEqual(message, "Invalid Semester. Acceptable values are fall, spring, winter, and summer",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(semester='autumn').first(), None, "Course created with invalid semester")

        message = func_CourseCreator("Computer Architecture", "COMPSCI", 451, "", 2023)
        self.assertEqual(message, "Invalid Semester. Acceptable values are fall, spring, winter, and summer",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(semester='').first(), None, "Course created with invalid semester")

    def test_InvalidSemester(self):
        message = func_CourseCreator("Computer Architecture", "COMPSCI", 451, "spring", 2026)
        self.assertEqual(message, "Invalid Year. Must be later than 1956 and cannot be greater than 2025", "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(year=2027).first(), None, "Course created with invalid year")

        message = func_CourseCreator("Computer Architecture", "COMPSCI", 451, "spring", 1956)
        self.assertEqual(message, "Invalid Year. Must be later than 1956 and cannot be greater than 2025",
                         "Proper error message is not returned")
        self.assertEqual(Course.objects.filter(year=1956).first(), None, "Course created with invalid year")

class TestAssignUserToCourse(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.emma = MyUser(1, "esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                 "Milwaukee", "WI", '53026', "admin")

        self.emma.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                   "Milwaukee", "WI", '53026', "admin")
        self.henry.save()
        self.swe.assignedUser.add(self.emma)
        self.swe.save()

    def test_ValidAssignUser(self):
        message = func_AssignUserToCourse('writchie@uwm.edu', 1)
        self.assertEqual(message, "User added successfully!")
        self.assertIn(self.henry, self.swe.assignedUser.all(), "User not added to course's users")

    def test_AssignUserAlreadyIn(self):
        message = func_AssignUserToCourse('esonnen@uwm.edu', 1)
        self.assertEqual(message, "User is already in the course!")

    def test_AssignUserNonexistantUser(self):
        message = func_AssignUserToCourse('nope@uwm.edu', 1)
        self.assertEqual(message, "User does not exist!")

    def test_AssignUserNonexistantCourse(self):
        message = func_AssignUserToCourse('writchie@uwm.edu', 2)
        self.assertEqual(message, "This course does not exist!")

class TestRemoveCourseUser(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.emma = MyUser(1, "esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                 "Milwaukee", "WI", '53026', "admin")

        self.emma.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                   "Milwaukee", "WI", '53026', "admin")
        self.henry.save()
        self.swe.assignedUser.add(self.emma)
        self.swe.save()

    def test_ValidRemoveUser(self):
        message = func_RemoveCourseUser('esonnen@uwm.edu', 1)
        self.assertEqual(message, "User removed successfully!")
        self.assertNotIn(self.emma, self.swe.assignedUser.all(), "User not removed from course's users")

    def test_AssignUserNotIn(self):
        message = func_RemoveCourseUser('writchie@uwm.edu', 1)
        self.assertEqual(message, "User is not in the course!")

    def test_AssignUserNonexistantUser(self):
        message = func_RemoveCourseUser('nope@uwm.edu', 1)
        self.assertEqual(message, "User does not exist!")

    def test_AssignUserNonexistantCourse(self):
        message = func_RemoveCourseUser('esonnen@uwm.edu', 2)
        self.assertEqual(message, "This course does not exist!")

class TestUserIsInstructorOfCourse(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.emma = MyUser(1, "esonnen@uwm.edu", "password", "Emma", "Sonnen", "5555555555", "1234 main st",
                                 "Milwaukee", "WI", '53026', "instructor")

        self.emma.save()
        self.henry = MyUser(2, "writchie@uwm.edu", "password", "Henry", "Ritchie", "5555555555", "1234 main st",
                                   "Milwaukee", "WI", '53026', "instructor")
        self.henry.save()
        self.sarah = MyUser(3, "scramer@uwm.edu", "password", "Sarah", "Cramer", "5555555555", "1234 main st",
                                  "Milwaukee", "WI", '53026', "ta")

        self.sarah.save()
        self.bob = MyUser(4, "ballen@uwm.edu", "password", "Bob", "Allen", "5555555555", "1234 main st",
                               "Milwaukee", "WI", '53026', "admin")

        self.bob.save()
        self.swe.assignedUser.add(self.emma, self.sarah)
        self.swe.save()

    def test_IsInstructorInCourse(self):
        result = func_UserIsInstructorOfCourse('esonnen@uwm.edu', 1)
        self.assertEqual(result, 'True',  "True not passed for instructor of course")

    def test_InstructorNotInCourse(self):
        result = func_UserIsInstructorOfCourse('writchie@uwm.edu', 1)
        self.assertEqual(result, 'False', "False not passed for instructor not in course")

    def test_TAInCourse(self):
        result = func_UserIsInstructorOfCourse('scramer@uwm.edu', 1)
        self.assertEqual(result, 'False', "False not passed for TA in course")

    def test_AdminNotInCourse(self):
        result = func_UserIsInstructorOfCourse('ballen@uwm.edu', 1)
        self.assertEqual(result, 'False', "False not passed for admin not in course")

    def test_NonexistantUser(self):
        result = func_UserIsInstructorOfCourse('nope@uwm.edu', 1)
        self.assertEqual(result, 'User does not exist!', "False not passed for admin not in course")

    def test_NonexistantCourse(self):
        result = func_UserIsInstructorOfCourse('writchie@uwm.edu', 2)
        self.assertEqual(result, 'This course does not exist!', "False not passed for admin not in course")

class TestEditCourseName(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_EditNameValid(self):
        result = func_EditCourseName('Computer Architecture', 1)
        self.assertEqual(result, 'Course Name edited successfully!', "success message does not play")
        self.assertEqual(Course.objects.get(id=1).name, 'Computer Architecture', 'course name not changed')

        result = func_EditCourseName('Our Physical Environment', 1)
        self.assertEqual(result, 'Course Name edited successfully!', "success message does not play")
        self.assertEqual(Course.objects.get(id=1).name, 'Our Physical Environment', 'course name not changed')

    def test_EditNameInvalidName(self):
        result = func_EditCourseName('computer crchitecture', 1)
        self.assertEqual(result, "Invalid Course Name. Only letters and single spaces are allowed.",
                         "error message does not play for invalid course name")
        self.assertEqual(Course.objects.get(id=1).name, 'Software Engineering', 'course name changed when invalid')

        result = func_EditCourseName('', 1)
        self.assertEqual(result, "Invalid Course Name. Only letters and single spaces are allowed.",
                         "error message does not play for invalid name")
        self.assertEqual(Course.objects.get(id=1).name, 'Software Engineering', 'course name changed when invalid')

    def test_EditNameInvalidCourse(self):
        result = func_EditCourseName('Computer Acrchitecture', 2)
        self.assertEqual(result, "Course does not exist!", "error message does not play for invalid courseID")

class TestEditCourseDepartment(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_EditDepartmentValid(self):
        result = func_EditDepartment('ANTHRO', 1)
        self.assertEqual(result, "Department edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).department, 'ANTHRO', 'course department not changed')

        result = func_EditDepartment('GEO SCI', 1)
        self.assertEqual(result, "Department edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).department, 'GEO SCI', 'course department not changed')

    def test_EditDepartmentInvalidDepartment(self):
        result = func_EditDepartment('anthro', 1)
        self.assertEqual(result, "Invalid Department. All Departments come from the UWM course cataloge.",
                         "error message does not play for invalid course department")
        self.assertEqual(Course.objects.get(id=1).department, 'COMPSCI', 'course department changed when invalid')

        result = func_EditDepartment('', 1)
        self.assertEqual(result, "Invalid Department. All Departments come from the UWM course cataloge.",
                         "error message does not play for invalid department")
        self.assertEqual(Course.objects.get(id=1).department, 'COMPSCI', 'course department changed when invalid')

    def test_EditDepartmentInvalidCourse(self):
        result = func_EditDepartment('ANTHRO', 2)
        self.assertEqual(result, "Course does not exist!", "error message does not play for invalid courseID")

class TestEditCourseNumber(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()
        self.ca = Course(2, "Computer Architecture", "COMPSCI", 451, "spring", 2023)
        self.ca.save()

    def test_EditCourseNumberValid(self):
        result = func_EditCourseNumber(100, 1)
        self.assertEqual(result, "Course Number edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).courseNumber, 100, 'course number not changed')

        result = func_EditCourseNumber(600, 1)
        self.assertEqual(result, "Course Number edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).courseNumber, 600, 'course number not changed')

    def test_EditCourseNumberInvalidCourseNumber(self):
        result = func_EditCourseNumber(99, 1)
        self.assertEqual(result, "Invalid Course Number. Must be between 100 and 999 and unique.",
                         "error message does not play for invalid course number")
        self.assertEqual(Course.objects.get(id=1).courseNumber, 361, 'course number changed when invalid')

        result = func_EditCourseNumber(1000, 1)
        self.assertEqual(result, "Invalid Course Number. Must be between 100 and 999 and unique.",
                         "error message does not play for invalid number")
        self.assertEqual(Course.objects.get(id=1).courseNumber, 361, 'course number changed when invalid')

        result = func_EditCourseNumber(451, 1)
        self.assertEqual(result, "Invalid Course Number. Must be between 100 and 999 and unique.",
                         "error message does not play for invalid number")
        self.assertEqual(Course.objects.get(id=1).courseNumber, 361, 'course number changed when invalid')

    def test_EditCourseNumberInvalidCourse(self):
        result = func_EditCourseNumber(200, 3)
        self.assertEqual(result, "Course does not exist!", "error message does not play for invalid courseID")

class TestEditCourseSemester(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_EditSemesterValid(self):
        result = func_EditSemester('fall', 1)
        self.assertEqual(result, "Semester edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).semester, 'fall', 'course semester not changed')

        result = func_EditSemester('summer', 1)
        self.assertEqual(result, "Semester edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).semester, 'summer', 'course semester not changed')

    def test_EditSemesterInvalidSemester(self):
        result = func_EditSemester('Fall', 1)
        self.assertEqual(result, "Invalid Semester. Acceptable values are fall, spring, winter, and summer",
                         "error message does not play for invalid course semester")
        self.assertEqual(Course.objects.get(id=1).semester, 'spring', 'course semester changed when invalid')

        result = func_EditSemester('', 1)
        self.assertEqual(result, "Invalid Semester. Acceptable values are fall, spring, winter, and summer",
                         "error message does not play for invalid semester")
        self.assertEqual(Course.objects.get(id=1).semester, 'spring', 'course semester changed when invalid')

    def test_EditSemesterInvalidCourse(self):
        result = func_EditSemester('spring', 2)
        self.assertEqual(result, "Course does not exist!", "error message does not play for invalid courseID")

class TestEditCourseYear(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_EditYearValid(self):
        result = func_EditYear(2025, 1)
        self.assertEqual(result, "Year edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).year, 2025, 'course year not changed')

        result = func_EditYear(2015, 1)
        self.assertEqual(result, "Year edited successfully!", "success message does not play")
        self.assertEqual(Course.objects.get(id=1).year, 2015, 'course year not changed')

    def test_EditYearInvalidYear(self):
        result = func_EditYear(2026, 1)
        self.assertEqual(result, "Invalid Year. Must be later than 1956 and cannot be greater than 2025",
                         "error message does not play for invalid course semester")
        self.assertEqual(Course.objects.get(id=1).year, 2023, 'course year changed when invalid')

        result = func_EditYear(1956, 1)
        self.assertEqual(result, "Invalid Year. Must be later than 1956 and cannot be greater than 2025",
                         "error message does not play for invalid semester")
        self.assertEqual(Course.objects.get(id=1).year, 2023, 'course year changed when invalid')

    def test_EditYearInvalidCourse(self):
        result = func_EditYear('spring', 2)
        self.assertEqual(result, "Course does not exist!", "error message does not play for invalid courseID")

class Test_CourseDeleter(TestCase):
    def setUp(self):
        self.swe = Course(1, "Software Engineering", "COMPSCI", 361, "spring", 2023)
        self.swe.save()

    def test_DeleteCourseValid(self):
        result = func_CourseDeleter(1)
        self.assertEqual(result, "Course deleted successfully", "sucess message does not play for course deletion")
        course_exists = Course.objects.filter(id=1).exists()
        self.assertFalse(course_exists, "Course was not deleted")

    def test_DeleteCourseInvalidCourse(self):
        result = func_CourseDeleter(2)
        self.assertEqual(result, "Course does not exist!", "error message does not play for invalid courseID")