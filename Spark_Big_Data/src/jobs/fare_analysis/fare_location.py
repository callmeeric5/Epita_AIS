from pyspark.sql.functions import desc, avg


def analyze_fare_location(df, gcs_output_path: None):
    df_fare_location = (
        df.groupBy("PULocationID", "DOLocationID")
        .agg(avg("fare_amount").alias("avg_fare"))
        .orderBy(desc("avg_fare"))
    )
    df_fare_location.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/fare_location_analysis")
