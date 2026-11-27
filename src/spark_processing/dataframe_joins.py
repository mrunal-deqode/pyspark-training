
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    LongType,
    StringType,
    BooleanType,
    TimestampType,
    DateType,
    DoubleType
)

from src.spark_processing.session import create_spark_session

from pyspark.sql.functions import (
    col,
    count,
    avg,
    max as spark_max,
    round as spark_round,
    when, asc, desc
)


APPLICATIONS_PATH = "data/raw/applications.csv"
JOBS_PATH = "data/raw/jobs.csv"


def main():
    spark = create_spark_session()

    try:
        # Explicit schema for applications
        applications_schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("candidate_id", IntegerType(), True),
            StructField("job_id", IntegerType(), True),
            StructField("years_of_experience", DoubleType(), True),
            StructField("status", StringType(), True),
            StructField("is_active", BooleanType(), True),
            StructField("created_at", TimestampType(), True),
        ])

        # Explicit schema for jobs
        jobs_schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("title", StringType(), True),
            StructField("job_type", StringType(), True),
            StructField("location", StringType(), True),
            StructField("min_experience_years", IntegerType(), True),
            StructField("max_experience_years", IntegerType(), True),
            StructField("salary_min", LongType(), True),
            StructField("salary_max", LongType(), True),
            StructField("status", StringType(), True),
            StructField("is_active", BooleanType(), True),
            StructField("created_by", IntegerType(), True),
            StructField("created_at", TimestampType(), True),
            StructField("deadline", DateType(), True),
        ])

        # Load applications
        applications_df = (
            spark.read
            .option("header", True)
            .schema(applications_schema)
            .csv(APPLICATIONS_PATH)
        )

        # Load jobs
        jobs_df = (
            spark.read
            .option("header", True)
            .schema(jobs_schema)
            .csv(JOBS_PATH)
        )

        print("\n========== APPLICATIONS SCHEMA ==========")
        applications_df.printSchema()

        print("\n========== JOBS SCHEMA ==========")
        jobs_df.printSchema()

        print("\n========== ROW COUNTS ==========")
        print("Applications:", applications_df.count())
        print("Jobs:", jobs_df.count())

        print("\n========== JOBS SAMPLE ==========")
        jobs_df.show(5, truncate=False)

        # Validate job IDs before joining
        print("\n========== JOB ID VALIDATION ==========")

        duplicate_job_ids = (
            jobs_df
            .groupBy("id")
            .agg(count("*").alias("record_count"))
            .filter(col("record_count") > 1)
        )

        print("Duplicate job IDs:", duplicate_job_ids.count())

        # Find applications whose job_id has no matching jobs.id
        unmatched_applications = applications_df.join(
            jobs_df,
            applications_df.job_id == jobs_df.id,
            "left_anti"
        )

        print(
            "Applications without matching jobs:",
            unmatched_applications.count()
        )

        unmatched_jobs = jobs_df.join(
            applications_df,
            jobs_df.id == applications_df.job_id,
            "left_anti"
        )

        print("Jobs without applications:", unmatched_jobs.count())
        unmatched_jobs.show(5, truncate=False)

        print("\n========== UNMATCHED APPLICATION SAMPLE ==========")
        unmatched_applications.show(10, truncate=False)

        # Compare all four join types
        print("\n========== JOIN TYPE COMPARISON ==========")

        inner_join_df = applications_df.join(
            jobs_df,
            applications_df.job_id == jobs_df.id,
            "inner"
        )

        left_join_df = applications_df.join(
            jobs_df,
            applications_df.job_id == jobs_df.id,
            "left"
        )

        print("\n========== LEFT JOIN PHYSICAL PLAN ==========")
        left_join_df.explain(mode="formatted")

        right_join_df = applications_df.join(
            jobs_df,
            applications_df.job_id == jobs_df.id,
            "right"
        )

        full_join_df = applications_df.join(
            jobs_df,
            applications_df.job_id == jobs_df.id,
            "full_outer"
        )

        print("Applications:", applications_df.count())
        print("Jobs:", jobs_df.count())

        print("Inner join rows:", inner_join_df.count())
        print("Left join rows:", left_join_df.count())
        print("Right join rows:", right_join_df.count())
        print("Full outer join rows:", full_join_df.count())

        print("\n========== LEFT JOIN SAMPLE ==========")

        left_join_df.select(
            applications_df.id.alias("application_id"),
            applications_df.job_id,
            jobs_df.title.alias("job_title"),
            jobs_df.job_type
        ).show(10, truncate=False)

        from pyspark.sql.functions import when

        print("\n========== EXPERIENCE GAP ANALYSIS ==========")

        enriched_applications = (
            left_join_df
            .withColumn(
                "experience_gap",
                spark_round(
                    applications_df.years_of_experience - jobs_df.min_experience_years,
                    2
                )
            )
            .withColumn(
                "experience_match",
                when(col("experience_gap") >= 0, "Meets Requirement")
                .otherwise("Below Requirement")
            )
        )

        enriched_applications.select(
            applications_df.id.alias("application_id"),
            applications_df.years_of_experience,
            jobs_df.min_experience_years,
            "experience_gap",
            "experience_match"
        ).show(10, truncate=False)

        print(
            "Total applications after enrichment:",
            enriched_applications.count()
        )

        # Group applications by job type and calculate multiple metrics
        print("\n========== RECRUITMENT AGGREGATION ==========")

        job_type_summary = (
            enriched_applications
            .groupBy(jobs_df.job_type)
            .agg(
                count(applications_df.id).alias("total_applications"),
                spark_round(
                    avg(applications_df.years_of_experience), 2
                ).alias("average_experience"),
                spark_round(
                    spark_max(applications_df.years_of_experience), 2
                ).alias("maximum_experience")
            )
        )

        job_type_summary.show(truncate=False)

        print("\n========== SORTED RECRUITMENT SUMMARY ==========")

        sorted_summary = job_type_summary.orderBy(
            desc("total_applications"),
            asc("job_type")
        )

        sorted_summary.show(truncate=False)

        print(
            "Total applications across groups:",
            job_type_summary.agg(
                {"total_applications": "sum"}
            ).first()[0]
        )

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
