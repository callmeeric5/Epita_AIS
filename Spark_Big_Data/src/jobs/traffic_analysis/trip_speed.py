from pyspark.sql.functions import hour, dayofweek, avg, unix_timestamp, col, month

"""
Analysis:

The similar trips can be defined as the trips have same distance, pickup/dropoff locations, and time.
Using pickup/dropoff as the criterion, it will mess the next grouping operation.
In this situation, only consider distance and time. In the previous analysis, the avg of distance, time by day/week/month is known
Suppose it follows normal distribution, according to the central limit theory and considering of saving time(regardless of the std), the threshold will be set as 1
"""


def analyze_trip_speed(df, gcs_output_path: None):
    df_trip = df.withColumn(
        "trip_duration_mins",
        (
            unix_timestamp("tpep_dropoff_datetime")
            - unix_timestamp("tpep_pickup_datetime")
        )
        / 60,
    )
    df_speed = df_trip.withColumn(
        "trip_speed", (col("trip_distance") / (col("trip_duration_mins") / 60))
    )

    threshold = 1
    df_speed_hour = (
        df_speed.groupBy(hour("tpep_pickup_datetime").alias("hour"))
        .agg(
            avg("trip_duration_mins").alias("avg_duration"),
            avg("trip_distance").alias("avg_distance"),
            avg("trip_speed").alias("avg_speed"),
        )
        .orderBy("hour")
    )
    lower_duration = col("avg_duration") - threshold
    upper_duration = col("avg_duration") + threshold
    lower_distance = col("avg_distance") - threshold
    upper_distance = col("avg_distance") + threshold

    df_speed_hour = df_speed_hour.filter(
        (lower_duration <= col("avg_duration"))
        & (col("avg_duration") <= upper_duration)
        & (lower_distance <= col("avg_distance"))
        & (col("avg_distance") <= upper_distance)
    )
    df_speed_week = (
        df_speed.groupBy(dayofweek("tpep_pickup_datetime").alias("week"))
        .agg(
            avg("trip_duration_mins").alias("avg_duration"),
            avg("trip_distance").alias("avg_distance"),
            avg("trip_speed").alias("avg_speed"),
        )
        .orderBy("week")
    )

    lower_duration = col("avg_duration") - threshold
    upper_duration = col("avg_duration") + threshold
    lower_distance = col("avg_distance") - threshold
    upper_distance = col("avg_distance") + threshold

    df_speed_week = df_speed_week.filter(
        (lower_duration <= col("avg_duration"))
        & (col("avg_duration") <= upper_duration)
        & (lower_distance <= col("avg_distance"))
        & (col("avg_distance") <= upper_distance)
    )
    df_speed_month = (
        df_speed.groupBy(month("tpep_pickup_datetime").alias("month"))
        .agg(
            avg("trip_duration_mins").alias("avg_duration"),
            avg("trip_distance").alias("avg_distance"),
            avg("trip_speed").alias("avg_speed"),
        )
        .orderBy("month")
    )
    lower_duration = col("avg_duration") - threshold
    upper_duration = col("avg_duration") + threshold
    lower_distance = col("avg_distance") - threshold
    upper_distance = col("avg_distance") + threshold

    df_speed_month = df_speed_month.filter(
        (lower_duration <= col("avg_duration"))
        & (col("avg_duration") <= upper_duration)
        & (lower_distance <= col("avg_distance"))
        & (col("avg_distance") <= upper_distance)
    )
    df_speed_hour.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/speed_hour_analysis")

    df_speed_week.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/speed_weekday_analysis")

    df_speed_month.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/speed_month_analysis")
