from pyspark.sql.functions import month, avg, unix_timestamp, dayofweek, hour


def analyze_duration(df, gcs_output_path: None):
    df_trip = df.withColumn(
        "trip_duration_mins",
        (
            unix_timestamp("tpep_dropoff_datetime")
            - unix_timestamp("tpep_pickup_datetime")
        )
        / 60,
    )
    df_trip_hour = (
        df_trip.groupBy(hour("tpep_pickup_datetime").alias("hour"))
        .agg(
            avg("trip_duration_mins").alias("avg_duration"),
            avg("trip_distance").alias("avg_distance"),
        )
        .orderBy("hour")
    )
    df_trip_day = (
        df_trip.groupBy(dayofweek("tpep_pickup_datetime").alias("weekday"))
        .agg(
            avg("trip_duration_mins").alias("avg_duration"),
            avg("trip_distance").alias("avg_distance"),
        )
        .orderBy("weekday")
    )
    df_trip_month = (
        df_trip.groupBy(month("tpep_pickup_datetime").alias("month"))
        .agg(
            avg("trip_duration_mins").alias("avg_duration"),
            avg("trip_distance").alias("avg_distance"),
        )
        .orderBy("month")
    )
    df_trip_hour.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/hour_analysis")

    df_trip_day.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/weekday_analysis")

    df_trip_month.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/month_analysis")
    return df_trip
