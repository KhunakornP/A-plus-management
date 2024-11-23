"""A script to import admission data from MyTCAS' csv file."""

import csv
import os
import re
from functools import reduce
from calculator.models import (
    University,
    Faculty,
    Major,
    Exams,
    CriteriaSet,
    ScoreHistory,
)

PATH = os.path.join(os.getcwd(), os.path.join("calculator", "data"))


def load_uni_faculty_major() -> None:
    """Create University, Faculty and Major objects."""
    data = get_non_duplicate_major_sample()
    for row in data:
        university = University.objects.get_or_create(name=row["university"])[0]
        faculty = Faculty.objects.get_or_create(
            name=row["faculty"], university=university
        )[0]
        major = Major.objects.get_or_create(
            name=row["major"], code=row["major_code"], faculty=faculty
        )[0]
        criteria_set = CriteriaSet.objects.get_or_create(
            name=row["criteria_set"], major=major
        )[0]
        university.save()
        faculty.save()
        major.save()
        criteria_set.save()
    print("Successfully imported University, Faculty and Major data")


def get_non_duplicate_major_sample() -> None:
    """Get sample of Unviersity, Faculty and Major.

    Due to time constraints, we only create demo for 3 universities.
    (Chulalongkorn, Kasetsart and KMITL)
    and only some faculties.
    (Engineering, Arts and Business Administration)
    """
    with open(os.path.join(PATH, "TCAS67_maxmin.csv"), encoding="utf-8-sig") as f:
        demo_university = (
            "จุฬาลงกรณ์มหาวิทยาลัย",
            "มหาวิทยาลัยเกษตรศาสตร์",
            "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง",
        )
        demo_faculty = ("คณะวิศวกรรมศาสตร์", "คณะอักษรศาสตร์", "คณะบริหารธุรกิจ")
        sample_data = filter(
            lambda x: x["university"] in demo_university
            and x["faculty"] in demo_faculty,
            map(
                lambda row: {
                    "university": row["สถาบัน"],
                    "faculty": row["คณะ"],
                    "major": row["หลักสูตร"],
                    "major_code": row["รหัสหลักสูตร"],
                    "criteria_set": row["รายละเอียด"]
                    if row["รายละเอียด"] != ""
                    else row["หลักสูตร"],
                    "min_score": string_to_numeric(row["คะแนนต่ำสุด หลังประมวลผลรอบ 2"]),
                    "max_score": string_to_numeric(row["คะแนนสูงสุด หลังประมวลผลรอบ 2"]),
                    "register": string_to_numeric(row["สมัคร"]),
                    "max_seat": string_to_numeric(row["รับ"]),
                    "admitted": string_to_numeric(row["ผ่าน(รอบ2)"]),
                },
                csv.DictReader(f),
            ),
        )

        non_duplicated_sample = reduce(
            lambda cum, i: cum + [i] if i not in cum else cum, sample_data, []
        )

    return non_duplicated_sample


def string_to_numeric(n: str) -> float | int:
    """Clean and check for empty string from csv.

    :param n: the sting of number
    :return: float or int of the string. 0 if the string is empty.
    """
    cleaned_n = re.sub(",", "", n)
    if cleaned_n == "":
        return 0
    if "." in cleaned_n:
        return float(cleaned_n)
    return int(cleaned_n)


def load_exams() -> None:
    """Create Exams objects."""
    with open(os.path.join(PATH, "exams.csv"), encoding="utf-8-sig") as f:
        rows = csv.DictReader(f)
        for row in rows:
            exam = Exams.objects.get_or_create(
                name=row["name"], max_score=row["max_score"]
            )[0]
            exam.core = eval(row["core"])
            exam.save()

        print("Successfully imported exams data.")


def load_criteria() -> None:
    """Load the score criteria of each major."""
    with open(os.path.join(PATH, "criteria.csv"), encoding="utf-8-sig") as f:
        rows = csv.DictReader(f)
        for row in rows:
            criteria_set = CriteriaSet.objects.get_or_create(
                name=row["criteria_name"],
                major=Major.objects.get(code=row["major_code"]),
            )[0]
            criteria = eval(eval(row["criteria"]))
            for exam_name, criterion in criteria.items():
                try:
                    weight = criterion["weight"]
                    min_score = criterion["min_score"]
                    criteria_set.criteria.get_or_create(
                        exam=Exams.objects.get(name=exam_name.strip()),
                        weight=weight,
                        min_score=min_score,
                    )
                except Exams.DoesNotExist as e:
                    raise Exams.DoesNotExist(f"Exam {exam_name} Not Found.") from e
            criteria_set.save()

        print("Successfully loaded criteria.")


def load_score_history() -> None:
    """Load the score history."""
    non_duplicate_sample = get_non_duplicate_major_sample()
    for row in non_duplicate_sample:
        try:
            major = Major.objects.get(code=row["major_code"])
            ScoreHistory.objects.create(
                major=major,
                criteria_set=CriteriaSet.objects.get(
                    name=row["criteria_set"], major=major
                ),
                min_score=row["min_score"],
                max_score=row["max_score"],
                register=row["register"],
                max_seat=row["max_seat"],
                admitted=row["admitted"],
                year=2567,
            )
        except Major.MultipleObjectsReturned:
            raise Major.MultipleObjectsReturned(
                f"University: {row["university"]}, faculty:{row["faculty"]}"
            )
    print("Successfully loaded score history.")


def run() -> None:
    """Run the import script."""
    load_uni_faculty_major()
    load_exams()
    load_criteria()
    load_score_history()
