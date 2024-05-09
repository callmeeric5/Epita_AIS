from jobs.trip_analysis.duration import analyze_duration
from jobs.trip_analysis.location import analyze_location


def analyze(spark, format="parquet", gcs_input_path=None, gcs_output_path=None):
    df = spark.read.format(format).load(gcs_input_path)
    df_trip = analyze_duration(df, gcs_output_path)
    analyze_location(df_trip, gcs_output_path)
    spark.stop()
