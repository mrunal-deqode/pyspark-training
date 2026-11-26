from src.spark_processing.session import create_spark_session


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    numbers_rdd = sc.parallelize(numbers)

    filtered_rdd = numbers_rdd.filter(
        lambda number: number % 2 == 0
    )

    squared_rdd = filtered_rdd.map(
        lambda number: number ** 2
    )

    print("Final result:", squared_rdd.collect())

    print("\nRDD Lineage / Debug String:")
    print(squared_rdd.toDebugString().decode("utf-8"))

    # print("\nRDD Dependencies:")
    # print(squared_rdd.dependencies)

    spark.stop()


if __name__ == "__main__":
    main()
