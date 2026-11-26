import csv
from io import StringIO
from pathlib import Path

from src.spark_processing.session import create_spark_session


def parse_profile(line):
    row = next(csv.reader(StringIO(line)))

    return {
        "user_id": row[1],
        "skills": row[5]
    }


def extract_skill_pairs(profile):
    skills = profile["skills"].split(",")

    return [
        (skill.strip(), 1)
        for skill in skills
        if skill.strip()
    ]


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    project_root = Path(__file__).resolve().parents[2]
    file_path = str(
        project_root / "data" / "raw" / "candidate_profiles.csv"
    )

    profiles_rdd = sc.textFile(file_path)

    skill_counts = (
        profiles_rdd
        .filter(lambda line: not line.startswith("id,"))
        .map(parse_profile)
        .flatMap(extract_skill_pairs)
        .reduceByKey(lambda a, b: a + b)
    )

    print("Top 10 most common candidate skills:")

    for skill, count in skill_counts.takeOrdered(
        10, key=lambda item: -item[1]
    ):
        print(f"{skill}: {count}")

    spark.stop()


if __name__ == "__main__":
    main()
