from src.spark_processing.session import create_spark_session


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    # Controlled application records:
    # (application_id, candidate_id, years_of_experience)
    applications = [
        (1, 101, 3),
        (2, 102, 5),
        (3, 103, -1),   # Invalid: negative experience
        (4, 104, 2),
        (5, 105, -3),   # Invalid: negative experience
        (6, 106, 7),
        (7, 107, 0),
        (8, 108, -2)    # Invalid: negative experience
    ]

    applications_rdd = sc.parallelize(applications, 2)

    # Create accumulator
    invalid_count = sc.accumulator(0)

    def validate_application(record):
        application_id, candidate_id, experience = record

        if experience < 0:
            invalid_count.add(1)
            return False

        return True

    # Validate records
    valid_applications = applications_rdd.filter(
        validate_application
    )

    # Trigger Spark execution
    valid_records = valid_applications.collect()

    print("Valid applications:")
    for record in valid_records:
        print(record)

    # Read accumulator on driver after action
    print("\nTotal valid records:", len(valid_records))
    print("Total invalid records:", invalid_count.value)

    spark.stop()


if __name__ == "__main__":
    main()
