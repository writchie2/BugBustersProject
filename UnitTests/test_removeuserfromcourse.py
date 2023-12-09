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

        # Create non-admin user
        self.non_admin = MyUser.objects.create(
            email='nonadmin@uwm.edu',
            password='nonadminpassword!23',
            firstName='Non',
            lastName='Admin',
            phoneNumber='9876543210',
            streetAddress='5678 Side St',
            city='Milwaukee',
            state='WI',
            zipcode=53206,
            role='TA'
        )

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
        non_existing_user = MyUser.objects.create(email='nonexisting@uwm.edu',
                                                  password='nonexistingpassword!2',
                                                  firstName='John',
                                                  lastName='Doe')
        # Count number of users
        initial_user_count = self.course.assignedUser.count()

        # Attempt to remove user not in course
        response = self.client.post('/coursepage/', {'removeuser': 'nonexisting@uwm.edu'}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertContains(response, "User is already not assigned to this course!")

        # Ensure the number of users is the same
        self.assertEqual(self.course.assignedUser.count(), initial_user_count)
        self.assertNotIn(non_existing_user, self.course.assignedUser.all())

        # Check that user was not deleted
        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")

    def test_remove_non_existing_user(self):
        # Count number of users
        initial_user_count = self.course.assignedUser.count()

        # Attempt to remove non-existing user
        response = self.client.post('/coursepage/', {'removeuser': 'random@uwm.edu'}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertContains(response, "User does not exist!")

        # Ensure the number of users is the same
        self.assertEqual(self.course.assignedUser.count(), initial_user_count)


    def test_user_not_removed_from_all_assigned_courses(self):
        # Create new course
        other_course = Course.objects.create(name='Other Course',
                                             department='MATH',
                                             courseNumber=456,
                                             semester='fall',
                                             year=2023)

        # Assign user to new course
        other_course.assignedUser.add(self.user)

        # Count number of users before
        initial_user_count = self.course.assignedUser.count()
        initial_other_course_user_count = other_course.assignedUser.count()

        # Remove user
        response = self.client.post('/coursepage/', {'removeuser': 'nonexisting@uwm.edu'}, follow=True)
        self.assertTemplateUsed(response, 'coursepage.html')
        self.assertContains(response, "User is already not assigned to this course!")

        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

        # Check that user was not deleted
        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")

        # Verify that the user is still associated with the other course
        self.assertEqual(other_course.assignedUser.count(), initial_other_course_user_count)
        self.assertIn(self.user, other_course.assignedUser.all())

    def test_non_admin_attempt_remove_user(self):
        # Count number of users before removal
        initial_user_count = self.course.assignedUser.count()

        # Log in as non-admin user
        self.client.login(email='nonadmin@uwm.edu', password='nonadminpassword!23')

        # Attempt to remove user from course as a non-admin user
        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)

        # Ensure the response indicates a permission error or similar
        self.assertContains(response, "Permission Denied")

        # Ensure the number of users is unchanged
        self.assertEqual(self.course.assignedUser.count(), initial_user_count)

        # Check that user was not deleted
        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")
