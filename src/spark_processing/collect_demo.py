from src.spark_processing.session import create_spark_session


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    large_rdd = sc.parallelize(range(1, 1_000_001))

    print("Total records:", large_rdd.count())

    # Collect every record to the driver
    collected_data = large_rdd.collect()

    print("Records returned to driver:", len(collected_data))
    print("First 10 collected records:", collected_data[:10])

    # Safer alternative when only a sample is needed
    print("First 10 records using take():", large_rdd.take(10))

    spark.stop()


if __name__ == "__main__":
    main()
