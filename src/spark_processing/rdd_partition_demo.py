from src.spark_processing.session import create_spark_session


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    numbers = list(range(1, 101))
    numbers_rdd = sc.parallelize(numbers, 8)

    # Increase partitions using repartition
    repartitioned_rdd = numbers_rdd.repartition(12)

    # Reduce partitions using coalesce
    coalesced_rdd = repartitioned_rdd.coalesce(2)

    print("Original partitions:", numbers_rdd.getNumPartitions())
    print("Repartitioned partitions:", repartitioned_rdd.getNumPartitions())
    print("Coalesced partitions:", coalesced_rdd.getNumPartitions())

    print("\nRepartition lineage:")
    print(repartitioned_rdd.toDebugString().decode("utf-8"))

    print("\nCoalesce lineage:")
    print(coalesced_rdd.toDebugString().decode("utf-8"))

    print("\nFinal record count:", coalesced_rdd.count())

    spark.stop()


if __name__ == "__main__":
    main()
