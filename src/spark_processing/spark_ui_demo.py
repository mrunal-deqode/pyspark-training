import time

from src.spark_processing.session import create_spark_session
from src.spark_processing.data_loader import load_recruitment_data


spark = create_spark_session()

try:
    users, profiles, jobs, applications = load_recruitment_data(spark)

    print("\nSpark UI URL:", spark.sparkContext.uiWebUrl)

    print("\nRunning application count action...")

    total_applications = applications.count()

    print("Total applications:", total_applications)

    print("\nSpark application is running.")
    print("Open the Spark UI in your browser.")
    print("Press Ctrl+C in the terminal when inspection is complete.")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping Spark application...")

finally:
    spark.stop()
