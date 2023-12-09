import sys
from django.test import TestCase, Client
from SchedulingApp.models import Course, MyUser
from SchedulingApp.functions import func_RemoveUserFromCourse


# check that user doing this is admin
# should also test that removing user does not delete user
class test_RemoveUserFromCourse(TestCase):

    def setUp(self):
        self.client = Client()

        # Create admin
        self.admin = MyUser.objects.create(
            email='admin@uwm.edu',
            password='password!123',
            firstName='Administrator',
            lastName='Admin',
            phoneNumber='1231234567',
            streetAddress='1234 Main St',
            city='Milwaukee',
            state='WI',
            zipcode=53206,
            role='admin'
        )

        # Log in as admin
        self.client.login(email='admin@uwm.edu', password='password!123')

        # Create course
        self.course = Course.objects.create(
            name='Intro to Software Engineering',
            department='COMPSCI',
            courseNumber=361,
            semester='spring',
            year=2023
        )

        # Create user to add to course
        self.user = MyUser.objects.create(
            email="user@uwm.edu",
            password="password",
            firstName="Jane",
            lastName="Doe",
            phoneNumber="3333333333",
            streetAddress="1236 main st",
            city="Milwaukee",
            state="WI",
            zipcode=53026,
            role="TA")

        # Add user to course
        self.course.assignedUser.add(self.user)

    def test_func_RemoveUserFromCourse_success(self):
        # Check number of users before removal
        initial_user_count = self.course.assignedUser.count()

        # Delete user from course
        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertContains(response, "User removed from course successfully!")

        # Ensure user was actually removed from course
        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

        # Check that user was not deleted
        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")

    def test_user_not_in_course(self):
        # Create user not assigned to course
        non_existing_user = MyUser.objects.create(email='nonexisting@uwm.edu', password='nonexistingpassword!2',
                                                  firstName='John', lastName='Doe')
        # Count number of users
        initial_user_count = self.course.assignedUser.count()
        func_RemoveUserFromCourse(non_existing_user)
        self.assertEqual(self.course.assignedUser.count(), initial_user_count)
        self.assertNotIn(non_existing_user, self.course.assignedUser.all())
        try:
            non_existing_user.firstName
        except Exception:
            self.fail("User was removed from database!")

    def test_func_RemoveUserFromCourse_from_multiple_courses(self):
        other_course = Course.objects.create(name='Other Course', department='MATH', courseNumber=456, semester='fall',
                                             year=2023)
        other_course.assignedUser.add(self.user)

        initial_user_count = self.course.assignedUser.count()
        initial_other_course_user_count = other_course.assignedUser.count()

        func_RemoveUserFromCourse(self.user)

        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

        # Verify that the user is still associated with the other course
        self.assertEqual(other_course.assignedUser.count(), initial_other_course_user_count)
        self.assertIn(self.user, other_course.assignedUser.all())
