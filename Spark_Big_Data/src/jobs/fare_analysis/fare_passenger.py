from pyspark.sql.functions import desc, avg


def analyze_fare_passenger(df, gcs_output_path: None):
    df_fare_passenger = (
        df.groupBy("passenger_count")
        .agg(avg("fare_amount").alias("avg_fare"))
        .orderBy(desc("avg_fare"))
    )
    df_fare_passenger.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/fare_passenger_count_analysis")
    correlation_fare_distance = df.stat.corr("fare_amount", "trip_distance")
    print(
        f"Correlation between fare_amount and trip_distance: {correlation_fare_distance}"
    )
