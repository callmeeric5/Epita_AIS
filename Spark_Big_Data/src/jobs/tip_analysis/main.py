from jobs.tip_analysis.tip_percentage import analyze_tip_percentage
from jobs.tip_analysis.tip_by_time import analyze_tip_by_time
from jobs.tip_analysis.tip_pay_type import analyze_pay_type


def analyze(spark, format="parquet", gcs_input_path=None, gcs_output_path=None):
    df = spark.read.format(format).load(gcs_input_path)
    df_tip = analyze_tip_percentage(df, gcs_output_path)
    analyze_tip_by_time(df_tip, gcs_output_path)
    analyze_pay_type(df_tip, gcs_output_path)
    spark.stop()
