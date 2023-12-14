import sys
from django.test import TestCase, Client
from SchedulingApp.models import Course, MyUser



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

        # Create another course just for funsies
        self.other_course = Course(5, 'Other Course',
                                   'MATH',
                                   456,
                                   'fall',
                                   2023)
        self.other_course.save()

    # Tests removing a user from course in an ideal scenario
    def test_func_RemoveUserFromCourse_success(self):
        initial_user_count = self.course.assignedUser.count()

        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)
        self.assertContains(response, "User removed from course successfully!")

        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")

    # Tests removing a user that is not assigned in the course
    def test_user_not_in_course(self):
        non_existing_user = MyUser.objects.create(email='nonexisting@uwm.edu',
                                                  password='nonexistingpassword!2',
                                                  firstName='John',
                                                  lastName='Doe')

        initial_user_count = self.course.assignedUser.count()

        response = self.client.post('/coursepage/', {'removeuser': 'nonexisting@uwm.edu'}, follow=True)
        self.assertContains(response, "User is not in this course!")

        self.assertEqual(self.course.assignedUser.count(), initial_user_count)
        self.assertNotIn(non_existing_user, self.course.assignedUser.all())

        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")

    # Tests removing a user that is not in the database
    def test_remove_non_existing_user(self):
        initial_user_count = self.course.assignedUser.count()

        response = self.client.post('/coursepage/', {'removeuser': 'random@uwm.edu'}, follow=True)
        self.assertContains(response, "User does not exist!")

        self.assertEqual(self.course.assignedUser.count(), initial_user_count)

    # Tests that removing a user from one course does not remove them from another
    def test_user_not_removed_from_all_assigned_courses(self):
        self.other_course.assignedUser.add(self.user)

        initial_user_count = self.course.assignedUser.count()
        initial_other_course_user_count = self.other_course.assignedUser.count()

        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)
        self.assertContains(response, "User removed from course successfully!")

        self.assertEqual(self.course.assignedUser.count(), initial_user_count - 1)
        self.assertNotIn(self.user, self.course.assignedUser.all())

        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")

        self.assertEqual(self.other_course.assignedUser.count(), initial_other_course_user_count)
        self.assertIn(self.user, self.other_course.assignedUser.all())

    # Tests a non-admin user trying to remove a user from course
    def test_non_admin_attempt_remove_user(self):
        initial_user_count = self.course.assignedUser.count()

        session = self.client.session
        session["email"] = "nonadmin@uwm.edu"
        session["role"] = "ta"
        session.save()

        response = self.client.post('/coursepage/', {'removeuser': 'user@uwm.edu'}, follow=True)

        self.assertContains(response, "Permission Denied")

        self.assertEqual(self.course.assignedUser.count(), initial_user_count)

        user_exists = MyUser.objects.filter(email='user@uwm.edu').exists()
        self.assertTrue(user_exists, "User was unexpectedly deleted from the database.")
