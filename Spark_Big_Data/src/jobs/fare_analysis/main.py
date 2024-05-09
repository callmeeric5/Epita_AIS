from jobs.fare_analysis.fare_passenger import analyze_fare_passenger
from jobs.fare_analysis.fare_location import analyze_fare_location


def analyze(spark, format="parquet", gcs_input_path=None, gcs_output_path=None):
    df = spark.read.format(format).load(gcs_input_path)
    analyze_fare_passenger(df, gcs_output_path)
    analyze_fare_location(df, gcs_output_path)
    spark.stop()
