from pyspark.sql.functions import col, desc, avg


def analyze_tip_percentage(df, gcs_output_path: None):
    df_tip = df.withColumn(
        "tip_percentage", col("tip_amount") / col("total_amount") * 100
    )
    df_tip_trip = (
        df_tip.groupBy("PULocationID", "DOLocationID")
        .agg(
            avg("tip_percentage").alias("avg_tip_percentage"),
            avg("trip_distance").alias("avg_distance"),
        )
        .orderBy(desc("avg_tip_percentage"))
    )
    df_tip_trip.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/tip_percentage_analysis")
    correlation = df_tip.stat.corr("trip_distance", "tip_percentage")
    print(f"Correlation between trip_distance and tip_percentage: {correlation}")
    return df_tip
