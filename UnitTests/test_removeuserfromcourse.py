from django.test import TestCase
from SchedulingApp.models import Course, MyUser

#check that user doing this is admin
class test_RemoveUserFromCourse(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email='test@uwm.edu', password='test!2password', firstName='John',
                                          lastName='Doe')
        self.course = Course.objects.create(name='Test Course', department='COMPSCI', courseNumber=123,
                                            semester='spring', year=2023)
        self.course.assignedUser.add(self.user)

    def test_func_RemoveUserFromCourse_success(self):
        initial_user_count = self.course.assignedUser.count()
        self.course.func_RemoveUserFromCourse(self.user)
        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

    def test_remove_non_existing_user(self):
        non_existing_user = MyUser.objects.create(email='nonexisting@uwm.edu', password='nonexistingpassword',
                                                  firstName='Jane', lastName='Doe')
        initial_user_count = self.course.assignedUser.count()
        self.course.func_RemoveUserFromCourse(non_existing_user)
        self.assertEqual(self.course.assignedUser.count(), initial_user_count)
        self.assertNotIn(non_existing_user, self.course.assignedUser.all())

    def test_func_RemoveUserFromCourse_from_multiple_courses(self):
        other_course = Course.objects.create(name='Other Course', department='MATH', courseNumber=456, semester='fall',
                                             year=2023)
        other_course.assignedUser.add(self.user)

        initial_user_count = self.course.assignedUser.count()
        initial_other_course_user_count = other_course.assignedUser.count()

        self.course.func_RemoveUserFromCourse(self.user)

        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

        # Verify that the user is still associated with the other course
        self.assertEqual(other_course.assignedUser.count(), initial_other_course_user_count)
        self.assertIn(self.user, other_course.assignedUser.all())

    def test_func_RemoveUserFromCourse_with_constraints(self):
        # Set up constraints (e.g., user is an instructor, and it's the active semester)
        self.user.role = 'instructor'
        self.user.save()

        # Attempt to remove the user during the active semester
        with self.assertRaises(ValueError) as context:
            self.course.func_RemoveUserFromCourse(self.user)

        # Verify that the user is still associated with the course
        self.assertIn(self.user, self.course.assignedUser.all())
