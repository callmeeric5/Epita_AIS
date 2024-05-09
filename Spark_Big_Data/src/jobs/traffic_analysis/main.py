from jobs.traffic_analysis.trip_speed import analyze_trip_speed


def analyze(spark, format="parquet", gcs_input_path=None, gcs_output_path=None):
    df = spark.read.format(format).load(gcs_input_path)
    analyze_trip_speed(df, gcs_output_path)
    spark.stop()
