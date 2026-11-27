
import time

from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DoubleType,
    StringType,
    BooleanType,
    TimestampType,
)

from pyspark.sql.functions import (
    col,
    sum as spark_sum,
    when,
    year,
)

from src.spark_processing.session import create_spark_session


APPLICATIONS_PATH = "data/raw/applications.csv"


def main():
    spark = create_spark_session()

    try:
        # 1. Load CSV using automatic schema inference
        start_time = time.perf_counter()

        inferred_df = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(APPLICATIONS_PATH)
        )

        inferred_count = inferred_df.count()
        inferred_time = time.perf_counter() - start_time

        # 2. Define an explicit schema
        applications_schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("candidate_id", IntegerType(), True),
            StructField("job_id", IntegerType(), True),
            StructField("years_of_experience", DoubleType(), True),
            StructField("status", StringType(), True),
            StructField("is_active", BooleanType(), True),
            StructField("created_at", TimestampType(), True),
        ])

        # 3. Load CSV using the explicit schema
        start_time = time.perf_counter()

        explicit_df = (
            spark.read
            .option("header", True)
            .schema(applications_schema)
            .csv(APPLICATIONS_PATH)
        )

        explicit_count = explicit_df.count()
        explicit_time = time.perf_counter() - start_time

        # 4. Compare results
        print("\n========== ROW COUNTS ==========")
        print("Inferred schema count:", inferred_count)
        print("Explicit schema count:", explicit_count)

        print("\n========== INFERRED SCHEMA ==========")
        inferred_df.printSchema()

        print("\n========== EXPLICIT SCHEMA ==========")
        explicit_df.printSchema()

        print("\n========== LOAD TIME COMPARISON ==========")
        print(f"Inferred schema: {inferred_time:.4f} seconds")
        print(f"Explicit schema: {explicit_time:.4f} seconds")

        # 5. Explore the dataset
        print("\n========== DATA DESCRIPTION ==========")
        explicit_df.describe(
            "years_of_experience"
        ).show()

        print("\n========== SAMPLE RECORDS ==========")
        explicit_df.show(5, truncate=False)

        print("\n========== NULL VALUE CHECK ==========")

        from pyspark.sql.functions import col, sum as spark_sum, when

        null_counts = explicit_df.select(
            *[
                spark_sum(
                    when(col(column).isNull(), 1).otherwise(0)
                ).alias(column)
                for column in explicit_df.columns
            ]
        )

        null_counts.show()

        print("\n========== DATA TYPES ==========")
        print(explicit_df.dtypes)

        # 6. Create meaningful derived columns
        enriched_df = (
            explicit_df
            .withColumn(
                "experience_category",
                when(col("years_of_experience") == 0, "Fresher")
                .when(col("years_of_experience") <= 2, "Junior")
                .when(col("years_of_experience") <= 5, "Mid-Level")
                .otherwise("Senior")
            )
            .withColumn(
                "application_year",
                year(col("created_at"))
            )
        )

        print("\n========== DERIVED COLUMNS ==========")
        enriched_df.select(
            "id",
            "years_of_experience",
            "experience_category",
            "created_at",
            "application_year"
        ).show(10, truncate=False)

        # 7. Recruitment business question
        print("\n========== ACTIVE EXPERIENCED APPLICANTS ==========")

        experienced_applications = (
            enriched_df
            .filter(
                (col("is_active") == True)
                & (col("years_of_experience") >= 5)
            )
            .select(
                col("id").alias("application_id"),
                col("candidate_id"),
                col("years_of_experience"),
                col("status").alias("application_status"),
                col("experience_category")
            )
        )

        experienced_applications.show(10, truncate=False)

        print("\nTotal matching applications:",
              experienced_applications.count())

        # 8. Demonstrate drop()
        print("\n========== DROP COLUMN DEMO ==========")

        reduced_df = enriched_df.drop("is_active")

        print("Original columns:", enriched_df.columns)
        print("Columns after drop:", reduced_df.columns)

        print("\n========== CATALYST OPTIMIZED PLAN ==========")
        experienced_applications.explain(mode="extended")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
