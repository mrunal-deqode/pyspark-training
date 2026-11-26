from src.spark_processing.session import create_spark_session


def main():
    spark = create_spark_session()
    sc = spark.sparkContext

    numbers = [10, 20, 30, 40, 50]

    numbers_rdd = sc.parallelize(numbers)

    print("RDD created successfully!")
    print("RDD type:", type(numbers_rdd))
    print("RDD contents:", numbers_rdd.collect())
    print("Number of partitions:", numbers_rdd.getNumPartitions())

    # Transformation 1: Square each number
    squared_rdd = numbers_rdd.map(lambda number: number ** 2)

    # Transformation 2: Keep only even squared numbers
    even_squared_rdd = squared_rdd.filter(
        lambda number: number % 2 == 0
    )

    print("Original numbers:", numbers_rdd.collect())
    print("Squared numbers:", squared_rdd.collect())
    print("Even squared numbers:", even_squared_rdd.collect())

    # Create an RDD containing sentences
    sentences = [
        "Python is powerful",
        "Spark processes data",
        "FastAPI builds APIs"
    ]

    sentences_rdd = sc.parallelize(sentences)

    # Split each sentence into words and flatten the result
    words_rdd = sentences_rdd.flatMap(lambda sentence: sentence.split(" "))

    print("Original sentences:", sentences_rdd.collect())
    print("Words after flatMap:", words_rdd.collect())
    print("Total words:", words_rdd.count())

    # RDD Actions
    print("\n--- RDD Actions ---")

    print("Count:", numbers_rdd.count())

    print("First 3 elements:", numbers_rdd.take(3))

    print("First element:", numbers_rdd.first())

    total = numbers_rdd.reduce(lambda a, b: a + b)
    print("Sum using reduce:", total)

    spark.stop()


if __name__ == "__main__":
    main()
