from src.spark_processing.session import create_spark_session
from src.spark_processing.data_loader import load_recruitment_data


spark = create_spark_session()

try:
    users, profiles, jobs, applications = load_recruitment_data(spark)

    selected_applications = (
        applications
        .filter(applications.status == "Selected")
        .select(
            "candidate_id",
            "job_id",
            "years_of_experience"
        )
        .filter(applications.years_of_experience >= 3)
    )

    print("\nLogical and Physical Execution Plan:")
    selected_applications.explain(extended=True)

finally:
    spark.stop()
