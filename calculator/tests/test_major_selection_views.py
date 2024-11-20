"""Test cases for APIs relating to getting university-related data."""

from .calculator_base_test_case import CalculatorExtraTestCase
from rest_framework import status


class UniversityAPITest(CalculatorExtraTestCase):
    """Test University, Faculty and Major APIs."""

    def test_getting_university(self):
        """Test fetching university data from the api view."""
        response = self.client.get("/api/universities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_getting_faculty(self):
        """Test getting valid faculty data."""
        response = self.client.get("/api/faculties/?university=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response2 = self.client.get("/api/faculties/?university=2")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)

    def test_getting_faculty_with_invalid_university_id(self):
        """Getting faculty of invalid university should return an empty list."""
        response = self.client.get("/api/faculties/?university=3000")
        self.assertEqual(len(response.data), 0)

    def test_getting_faculty_without_university_id(self):
        """Getting faculty without supplying university id.

        Should results in an empty response data.
        """
        response = self.client.get("/api/faculties/")
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_getting_major(self):
        """Test getting valid major data."""
        response = self.client.get("/api/majors/?faculty=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response2 = self.client.get("/api/majors/?faculty=2")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 4)

    def test_getting_major_with_invalid_faculty_id(self):
        """Getting majors of invalid faculty should return an empty list."""
        response = self.client.get("/api/faculties/?faculty=3000")
        self.assertEqual(len(response.data), 0)

    def test_getting_major_without_faculty_id(self):
        """Getting majors without supplying faculty id.

        Should results in an empty response data.
        """
        response = self.client.get("/api/faculties/")
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_getting_criteria(self):
        """Test getting valid criteria data."""
        response = self.client.get("/api/criteria/?major=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_getting_criteria_with_invalid_major_id(self):
        """Test getting valid criteria data."""
        response = self.client.get("/api/criteria/?major=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_criteria_set(self):
        """Retrieve a score of one Criteria Set."""
        response = self.client.get("/api/criteria/1/")
        self.assertEqual(
            response.data["criteria"],
            [
                {"id": 1, "min_score": 20.0, "weight": 10.0, "exam": 1},
                {"id": 3, "min_score": 20.0, "weight": 40.0, "exam": 3},
                {"id": 5, "min_score": 20.0, "weight": 40.0, "exam": 5},
            ],
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
