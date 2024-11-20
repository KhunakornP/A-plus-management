"""Base test case for Calculator app models."""

from django.test import TestCase
from calculator.models import University, Faculty, Major, CriteriaSet, Criterion, Exams


class CalculatorBaseTestCase(TestCase):
    """Set up 2 universities, each with one faculty.

    Faculty #1 has has 3 majors. While #2 has 4.
    """

    def setUp(self):
        """Set Up universities, faculties and majors."""
        faculty_name = "Engineering"
        self.university1 = University.objects.create(name="Kasetsart")
        self.faculty1 = Faculty.objects.create(
            name=faculty_name, university=self.university1
        )
        self.university2 = University.objects.create(name="KMITL")
        self.faculty2 = Faculty.objects.create(
            name=faculty_name, university=self.university2
        )
        Faculty.objects.create(university=self.university1, name="Humanity")
        for i in range(1, 8):
            m = Major.objects.create(
                name=f"Major #{i}",
                code=f"{i}",
                faculty=self.faculty1 if i % 2 == 0 else self.faculty2,
            )
            m.save()


class CalculatorExtraTestCase(CalculatorBaseTestCase):
    """Set up some CriteriaSet in addition to CalculatorBaseTestCase.

    (From CalculatorBaseTestCase)
    - 2 Universities. Each with 1 faculty.
    - Faculty #1 has has 3 majors. While #2 has 4.

    (Additional SetUps)
    - 2 CriteriaSet for Major #1.
    - Each CriteriaSet has 3 exams and different weight distribution.
    """

    def setUp(self):
        """Set up CalculatorBaseTestCase. As well as some exams and criteria."""
        super().setUp()
        major = Major.objects.get(pk=1)

        self.cs1 = CriteriaSet(major=major)
        self.cs2 = CriteriaSet(major=major)
        self.cs1.save()
        self.cs2.save()
        name = ["Maths", "Biology", "English"]
        score_weight = [10, 50, 40, 30, 40, 20]
        for i in range(6):
            e = Exams.objects.create(name=name[i % 3])
            c = Criterion.objects.create(exam=e, min_score=20, weight=score_weight[i])
            c.save()
            self.cs1.criteria.add(c) if i % 2 == 0 else self.cs2.criteria.add(c)
