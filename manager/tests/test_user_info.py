from django.contrib.auth.models import User
from django.test import TestCase
from manager.models import StudentInfo, ParentInfo
from django.db.utils import IntegrityError


class StudentInfoModelTestCase(TestCase):
    """Test cases for the StudentInfo class"""

    def setUp(self):
        """Set up to create user objects and save it to the database"""
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
        A user may only have at most 1 instance of StudentInfo
        associated at any point in time.
        """
        si = StudentInfo.objects.create(user=self.user1, displayed_name="tester")
        self.assertEqual(si, StudentInfo.objects.filter(user=self.user1)[0])
        with self.assertRaises(IntegrityError):
            # creating a new StudentInfo object with the same User
            # is not possible
            si2 = StudentInfo.objects.create(user=self.user1, displayed_name="joker")
        # as a side note: django db treats any code block as a "transaction"
        # so if any errors occurs during database operations the entire block
        # is reverted.

    def test_update_student_info(self):
        """An updated StudentInfo object still retains its original User."""
        si = StudentInfo.objects.create(user=self.user1, displayed_name="tester")
        si.displayed_name = "joker"
        si.parent = self.user2
        self.assertEqual(si.user, self.user1)

    def test_delete_parent(self):
        """
        Deleting a parent does not delete the StudentInfo object.
        The parent field is then replaced with NULL.
        """
        si = StudentInfo.objects.create(user=self.user1, displayed_name="tester")
        parent = User.objects.create_user(
            username="Jolyne", password="Aylmao123", email="bestmom@gmail.com"
        )
        parent.save()
        si.parent = parent
        self.assertEqual(si.parent, parent)
        self.assertEqual(1, StudentInfo.objects.count())
        parent.delete()
        self.assertEqual(1, StudentInfo.objects.count())
        # refresh the object by calling it from the database
        self.assertEqual(None, StudentInfo.objects.get(pk=1).parent)


class ParentInfoModelTestCase(TestCase):
    """Test cases for the ParentInfo class"""

    def setUp(self):
        """Set up to create user objects and save it to the database"""
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
        si1 = StudentInfo.objects.create(
            user=self.user1, displayed_name="Child1", parent=self.user3
        )
        si2 = StudentInfo.objects.create(
            user=self.user2, displayed_name="Child2", parent=self.user3
        )
        pi = ParentInfo.objects.create(user=self.user3, displayed_name="Parent")
        self.assertEqual(2, self.user3.student_set.count())
