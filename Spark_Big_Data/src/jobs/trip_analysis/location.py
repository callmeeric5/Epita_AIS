from pyspark.sql.functions import desc


def analyze_location(df, gcs_output_path: None):
    df_trip_pulocation = (
        df.groupby("PULocationID").count().orderBy(desc("count")).limit(10)
    )
    df_trip_dolocation = (
        df.groupby("DOLocationID").count().orderBy(desc("count")).limit(10)
    )

    df_trip_pulocation.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/top_10_pulocation_analysis")

    df_trip_dolocation.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/top_10_dolocation_analysis")
