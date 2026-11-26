import time

from src.spark_processing.session import create_spark_session


def expensive_operation(number):
    result = number

    for _ in range(10):
        result = (result * 2 + 3) % 1000003

    return result


def run_three_actions(rdd):
    start = time.perf_counter()

    count = rdd.count()
    total = rdd.sum()
    first_values = rdd.take(10)

    elapsed = time.perf_counter() - start

    return count, total, first_values, elapsed


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    source_rdd = sc.parallelize(range(1, 500001), 8)
    processed_rdd = source_rdd.map(expensive_operation)

    print("Running without cache...")
    uncached_result = run_three_actions(processed_rdd)

    print("Running with cache...")
    cached_rdd = processed_rdd.cache()
    cached_result = run_three_actions(cached_rdd)

    print("\n--- Results ---")
    print("Without cache:")
    print("Count:", uncached_result[0])
    print("Sum:", uncached_result[1])
    print("First 10:", uncached_result[2])
    print("Time:", round(uncached_result[3], 3), "seconds")

    print("\nWith cache:")
    print("Count:", cached_result[0])
    print("Sum:", cached_result[1])
    print("First 10:", cached_result[2])
    print("Time:", round(cached_result[3], 3), "seconds")

    cached_rdd.unpersist()
    spark.stop()


if __name__ == "__main__":
    main()
