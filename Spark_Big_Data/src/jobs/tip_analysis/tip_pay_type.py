from pyspark.sql.functions import col, avg

def analyze_pay_type(df, gcs_output_path: None):
    df_tip_payment = (
        df.groupBy("payment_type")
        .agg(avg("tip_percentage").alias("avg_tip_percentage"), avg("tip_amount"))
        .orderBy("payment_type")
    )

    df_tip_payment.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/tip_payment_type_analysis")
