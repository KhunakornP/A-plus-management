"""Test cases for APIs relating to getting university-related data."""

from .calculator_base_test_case import CalculatorBaseTestCase
from rest_framework import status


class UniversityAPITest(CalculatorBaseTestCase):
    """Test University, Faculty and Major APIs."""

    def test_getting_university(self):
        """Test fetching university data from the api view."""
        response = self.client.get("/api/university/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_getting_faculty(self):
        """Test getting valid faculty data."""
        response = self.client.get("/api/faculty/?university=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response2 = self.client.get("/api/faculty/?university=2")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)

    def test_getting_faculty_with_invalid_university_id(self):
        """Getting faculty of invalid university should return an empty list."""
        response = self.client.get("/api/faculty/?university=3000")
        self.assertEqual(len(response.data), 0)

    def test_getting_faculty_without_university_id(self):
        """Getting faculty without supplying university id.

        Should results in an empty response data.
        """
        response = self.client.get("/api/faculty/")
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_getting_major(self):
        """Test getting valid major data."""
        response = self.client.get("/api/major/?faculty=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response2 = self.client.get("/api/major/?faculty=2")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 3)

    def test_getting_major_with_invalid_faculty_id(self):
        """Getting majors of invalid faculty should return an empty list."""
        response = self.client.get("/api/faculty/?faculty=3000")
        self.assertEqual(len(response.data), 0)

    def test_getting_major_without_faculty_id(self):
        """Getting majors without supplying faculty id.

        Should results in an empty response data.
        """
        response = self.client.get("/api/faculty/")
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
