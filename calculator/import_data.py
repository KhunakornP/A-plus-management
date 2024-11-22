"""A script to import admission data from MyTCAS' csv file."""

import csv
import os
from functools import reduce
from calculator.models import University, Faculty, Major

PATH = os.path.join(
    os.getcwd(), os.path.join("calculator", os.path.join("data", "TCAS67_maxmin.csv"))
)


def run():
    """Run the import script."""
    with open(PATH, encoding="utf-8-sig") as f:
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
                lambda r: {
                    "university": r["สถาบัน"],
                    "faculty": r["คณะ"],
                    "major": r["หลักสูตร"],
                    "major_code": r["รหัสหลักสูตร"],
                },
                csv.DictReader(f),
            ),
        )

        non_duplicated_sample = reduce(
            lambda cum, i: cum + [i] if i not in cum else cum, sample_data, []
        )

        for row in non_duplicated_sample:
            university = University.objects.get_or_create(name=row["university"])[0]
            faculty = Faculty.objects.get_or_create(
                name=row["faculty"], university=university
            )[0]
            major = Major.objects.get_or_create(
                name=row["major"], code=row["major_code"], faculty=faculty
            )[0]
            university.save()
            faculty.save()
            major.save()

    print("Successfully imported University, Faculty and Major data")
