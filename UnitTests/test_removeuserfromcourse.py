import sys
from django.test import TestCase, Client
from SchedulingApp.models import Course, MyUser
from SchedulingApp.functions import func_RemoveUserFromCourse


# check that user doing this is admin
# should also test that removing user does not delete user
class test_RemoveUserFromCourse(TestCase):

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["email"] = "admin@uwm.edu"
        session["role"] = "admin"
        session.save()

        # Create admin
        self.admin = MyUser(1, 'admin@uwm.edu',
                            'password!123',
                            'Administrator',
                            'Admin',
                            '1231234567',
                            '1234 Main St',
                            'Milwaukee',
                            'WI',
                            53206,
                            'admin')
        self.admin.save()

        # Create non-admin user
        self.non_admin = MyUser(2,
                                'nonadmin@uwm.edu',
                                'nonadminpassword!23',
                                'Non',
                                'Admin',
                                '9876543210',
                                '5678 Side St',
                                'Milwaukee',
                                'WI',
                                53206,
                                'TA'
                                )

        self.non_admin.save()

        # Create course
        self.course = Course(3,
                             'Intro to Software Engineering',
                             'COMPSCI',
                             361,
                             'spring',
                             2023
                             )

        self.course.save()

        session["selectedcourse"] = self.course.id
        session.save()

        self.other_course = Course(5, 'Other Course',
                                   'MATH',
                                   456,
                                   'fall',
                                   2023)
        self.other_course.save()

        # Create user to add to course
        self.user = MyUser(4,
                           "user@uwm.edu",
                           "password##@@",
                           "Jane",
                           "Doe",
                           "3333333333",
                           "1236 main st",
                           "Milwaukee",
                           "WI",
                           53026,
                           "TA")
        self.user.save()

        # Add user to course
        self.course.assignedUser.add(self.user)

    def test_func_RemoveUserFromCourse_success(self):
        self.client.login(username='admin@uwm.edu', password='password!123')

        # Check number of users before removal
        initial_user_count = self.course.assignedUser.count()

        # Delete user from course
        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)
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
        self.assertContains(response, "User is not in this course!")

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
        self.assertContains(response, "User does not exist!")

        # Ensure the number of users is the same
        self.assertEqual(self.course.assignedUser.count(), initial_user_count)

    def test_user_not_removed_from_all_assigned_courses(self):
        # Assign user to new course
        self.other_course.assignedUser.add(self.user)

        # Count number of users before
        initial_user_count = self.course.assignedUser.count()
        initial_other_course_user_count = self.other_course.assignedUser.count()

        # Remove user
        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)
        self.assertContains(response, "User removed from course successfully!")

        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

        # Check that user was not deleted
        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")

        # Verify that the user is still associated with the other course
        self.assertEqual(self.other_course.assignedUser.count(), initial_other_course_user_count)
        self.assertIn(self.user, self.other_course.assignedUser.all())

    def test_non_admin_attempt_remove_user(self):
        # Count number of users before removal
        initial_user_count = self.course.assignedUser.count()

        # Log in as non-admin user
        session = self.client.session
        session["email"] = "nonadmin@uwm.edu"
        session["role"] = "ta"
        session.save()

        # Attempt to remove user from course as a non-admin user
        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)

        # Ensure the response indicates a permission error or similar
        self.assertContains(response, "Permission Denied")

        # Ensure the number of users is unchanged
        self.assertEqual(self.course.assignedUser.count(), initial_user_count)

        # Check that user was not deleted
        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")
