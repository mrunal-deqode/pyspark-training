from src.data_generation.config import RAW_DATA_DIR


def load_recruitment_data(spark):
    """Load all recruitment CSV datasets into Spark DataFrames."""

    users_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW_DATA_DIR / "users.csv"))
    )

    profiles_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW_DATA_DIR / "candidate_profiles.csv"))
    )

    jobs_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW_DATA_DIR / "jobs.csv"))
    )

    applications_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW_DATA_DIR / "applications.csv"))
    )

    return users_df, profiles_df, jobs_df, applications_df
