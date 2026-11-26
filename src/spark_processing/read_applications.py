from src.spark_processing.session import create_spark_session
from src.data_generation.config import RAW_DATA_DIR


def read_applications(spark):
    """Read the applications CSV into a Spark DataFrame."""

    file_path = RAW_DATA_DIR / "applications.csv"

    applications_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(file_path))
    )

    return applications_df


if __name__ == "__main__":
    spark = create_spark_session()

    try:
        applications_df = read_applications(spark)

        print("\nApplications Schema:")
        applications_df.printSchema()

        print("\nFirst 5 Applications:")
        applications_df.show(5, truncate=False)

    finally:
        spark.stop()
