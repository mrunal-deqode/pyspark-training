from src.spark_processing.session import create_spark_session
from src.spark_processing.data_loader import load_recruitment_data


spark = create_spark_session()

try:
    users, profiles, jobs, applications = load_recruitment_data(spark)

    print("\nStep 1: Creating transformations...")

    filtered_applications = applications.filter(
        applications.status == "Selected"
    )

    selected_columns = filtered_applications.select(
        "candidate_id",
        "job_id",
        "status",
        "years_of_experience"
    )

    experienced_candidates = selected_columns.filter(
        selected_columns.years_of_experience >= 3
    )

    print("Transformations created successfully.")
    print("No action has been called yet.")

    input("\nPress Enter to execute the action...")

    print("\nStep 2: Executing action using count()")

    result = experienced_candidates.count()

    print("Number of selected applications with 3+ years experience:", result)

    input("\nPress Enter to stop Spark...")

finally:
    spark.stop()
