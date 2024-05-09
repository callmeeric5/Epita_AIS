from pyspark.sql.functions import hour, dayofweek, year, avg


def analyze_tip_by_time(df, gcs_output_path: None):
    df_tip_hour = (
        df.groupBy(hour("tpep_pickup_datetime").alias("hour"))
        .agg(
            avg("tip_percentage").alias("avg_tip_percentage"),
            avg("trip_distance").alias("avg_distance"),
        )
        .orderBy("hour")
    )
    df_tip_week = (
        df.groupBy(dayofweek("tpep_pickup_datetime").alias("weekday"))
        .agg(
            avg("tip_percentage").alias("avg_tip_percentage"),
            avg("trip_distance").alias("avg_distance"),
        )
        .orderBy("weekday")
    )
    df_tip_year = (
        df.groupBy(year("tpep_pickup_datetime").alias("year"))
        .agg(
            avg("tip_percentage").alias("avg_tip_percentage"),
            avg("trip_distance").alias("avg_distance"),
        )
        .orderBy("year")
    )
    df_tip_hour.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/tip_hour_analysis")

    df_tip_week.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/tip_weekday_analysis")

    df_tip_year.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/tip_year_analysis")
