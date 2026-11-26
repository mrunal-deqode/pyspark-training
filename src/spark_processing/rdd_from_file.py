from src.spark_processing.session import create_spark_session
from pathlib import Path


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    project_root = Path(__file__).resolve().parents[2]
    file_path = str(
        project_root / "data" / "raw" / "candidate_profiles.csv"
    )

    profiles_rdd = sc.textFile(file_path)

    print("RDD created from CSV file!")
    print("First 5 lines:")
    for line in profiles_rdd.take(5):
        print(line)

    print("Total lines including header:", profiles_rdd.count())
    print("Number of partitions:", profiles_rdd.getNumPartitions())

    spark.stop()


if __name__ == "__main__":
    main()
