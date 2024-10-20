"""Test StudentInfo creation, update and User deletion."""

from django.contrib.auth.models import User
from django.test import TestCase
from manager.models import StudentInfo, ParentInfo
from django.db.utils import IntegrityError


class StudentInfoModelTestCase(TestCase):
    """Test cases for the StudentInfo class."""

    def setUp(self):
        """Set up to create user objects and save it to the database."""
        super().setUp()
        self.username = "DekD"
        self.password = "Tcaslover123"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="notavalidemail@gmail.com",
        )
        self.user1.first_name = "Tester"
        self.user1.save()
        self.user2 = User.objects.create_user(
            username="John", password="Bestdad1941", email="notavalidemail2@gmail.com"
        )
        self.user2.save()

    def test_student_info_creation(self):
        """
        Test StudentInfo creation after User creation.

        A StudentInfo object is created after a User object is created.
        A user may only have at most 1 instance of StudentInfo
        associated at any point in time.
        """
        self.assertEqual(1, StudentInfo.objects.filter(user=self.user1).count())
        user = User.objects.create_user(
            username="Dummy_D",
            password="Iamnotreal123",
            email="dopeopleuse@yahooanymore?",
        )
        # 2 from startup 1 from user creation
        self.assertEqual(3, StudentInfo.objects.count())
        self.assertEqual(1, StudentInfo.objects.filter(user=user).count())
        with self.assertRaises(IntegrityError):
            # creating a new StudentInfo object with the same User
            # is not possible
            StudentInfo.objects.create(user=self.user1, displayed_name="joker")
        # as a side note: django db treats any code block as a "transaction"
        # so if any errors occurs during database operations the entire block
        # is reverted and subsequent queries will fail.

    def test_update_student_info(self):
        """An updated StudentInfo object still retains its original User."""
        si = StudentInfo.objects.get(user=self.user1)
        si.displayed_name = "joker"
        si.parent = self.user2
        self.assertEqual(si.user, self.user1)

    def test_delete_parent(self):
        """
        Deleting a parent does not delete the StudentInfo object.

        The parent field is then also replaced with NULL.
        """
        si = StudentInfo.objects.get(user=self.user1)
        parent = User.objects.create_user(
            username="Jolyne", password="Aylmao123", email="bestmom@gmail.com"
        )
        parent.save()
        si.parent = parent
        self.assertEqual(si.parent, parent)
        self.assertEqual(1, StudentInfo.objects.filter(user=self.user1).count())
        parent.delete()
        self.assertEqual(1, StudentInfo.objects.filter(user=self.user1).count())
        # refresh the object by calling it from the database
        self.assertEqual(None, StudentInfo.objects.get(pk=1).parent)


class ParentInfoModelTestCase(TestCase):
    """Test cases for the ParentInfo class."""

    def setUp(self):
        """Set up to create user objects and save it to the database."""
        super().setUp()
        self.username = "DekD"
        self.password = "Tcaslover123"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="notavalidemail@gmail.com",
        )
        self.user1.first_name = "Tester"
        self.user2 = User.objects.create_user(
            username="myTcasser",
            password="myTcasdabest123",
            email="notavalidemail@gmail.com",
        )
        self.user2.save()
        self.user3 = User.objects.create_user(
            username="John", password="Bestdad1941", email="notavalidemail2@gmail.com"
        )
        self.user3.save()

    def test_get_all_children(self):
        """A User who is a parent can find all Users who are their child."""
        # get the related StudentInfo objects
        si1 = StudentInfo.objects.get(user=self.user1)
        si2 = StudentInfo.objects.get(user=self.user2)
        # update parent in the database
        si1.parent = self.user3
        si2.parent = self.user3
        si1.save()
        si2.save()
        pi = ParentInfo.objects.create(user=self.user3, displayed_name="Parent")
        self.assertEqual(2, self.user3.student_set.count())
        self.assertEqual(pi.user, self.user3)
