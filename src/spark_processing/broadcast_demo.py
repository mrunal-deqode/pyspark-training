from src.spark_processing.session import create_spark_session


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    # Small domain-specific lookup table
    job_type_lookup = {
        "Full-time": "Permanent Employment",
        "Contract": "Fixed-term Employment",
        "Internship": "Training Opportunity",
        "Part-time": "Flexible Employment"
    }

    # Broadcast lookup data to executors
    broadcast_lookup = sc.broadcast(job_type_lookup)

    # Sample recruitment job records
    jobs = [
        (101, "Java Developer", "Full-time"),
        (102, "Python Developer", "Contract"),
        (103, "React Intern", "Internship"),
        (104, "Data Analyst", "Part-time"),
        (105, "Backend Developer", "Full-time")
    ]

    jobs_rdd = sc.parallelize(jobs, 2)

    # Enrich records using the broadcast lookup
    enriched_jobs = jobs_rdd.map(
        lambda job: (
            job[0],
            job[1],
            job[2],
            broadcast_lookup.value.get(job[2], "Unknown")
        )
    )

    print("Enriched recruitment jobs:")

    for job in enriched_jobs.collect():
        print(job)

    broadcast_lookup.unpersist()
    spark.stop()


if __name__ == "__main__":
    main()
