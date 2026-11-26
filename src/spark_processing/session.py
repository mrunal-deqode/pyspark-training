from pyspark.sql import SparkSession


def create_spark_session():
    """Create and return a local SparkSession."""

    spark = (
        SparkSession.builder
        .appName("RecruitmentAnalytics")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )

    return spark


if __name__ == "__main__":
    spark = create_spark_session()

    print("SparkSession created successfully!")
    print("PySpark version:", spark.version)
    print("Spark application name:", spark.sparkContext.appName)
    print("Spark master:", spark.sparkContext.master)

    spark.stop()
