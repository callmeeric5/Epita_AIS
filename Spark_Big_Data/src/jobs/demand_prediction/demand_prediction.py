from pyspark.sql.functions import hour, dayofweek, month, year, sum
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from datetime import datetime, timedelta
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import SparkSession


def demand_prediction(df, gcs_output_path: None):
    spark = SparkSession.builder.appName("DemandPredictionAnalysis").getOrCreate()
    df_demand = df.withColumn("pickup_hour", hour("tpep_pickup_datetime"))
    df_demand = df_demand.withColumn(
        "pickup_day_of_week", dayofweek("tpep_pickup_datetime")
    )
    df_demand = df_demand.withColumn("pickup_month", month("tpep_pickup_datetime"))
    df_demand = df_demand.withColumn("pickup_year", year("tpep_pickup_datetime"))
    df_demand = (
        df_demand.groupBy(
            "pickup_hour", "pickup_day_of_week", "pickup_month", "pickup_year"
        )
        .agg(sum("passenger_count").alias("total_pickup"))
        .orderBy("pickup_hour", "pickup_day_of_week", "pickup_month", "pickup_year")
    )
    selected_features = [
        "pickup_hour",
        "pickup_day_of_week",
        "pickup_month",
        "pickup_year",
    ]

    assembler = VectorAssembler(inputCols=selected_features, outputCol="features")
    df_demand = assembler.transform(df_demand)
    train_data, test_data = df_demand.randomSplit([0.8, 0.2], seed=42)
    lr = LinearRegression(featuresCol="features", labelCol="total_pickup", regParam=0.2)
    lr_model = lr.fit(train_data)
    predictions = lr_model.transform(test_data)
    evaluator = RegressionEvaluator(
        labelCol="total_pickup", predictionCol="prediction", metricName="rmse"
    )
    rmse = evaluator.evaluate(predictions)
    predicted_df = predictions.select(
        "pickup_hour",
        "pickup_day_of_week",
        "pickup_month",
        "pickup_year",
        "total_pickup",
        "prediction",
    )
    predicted_df.repartition(1).write.mode("overwrite").format("csv").option(
        "header", "true"
    ).save(f"{gcs_output_path}/prediction_analysis")
    print("Root Mean Squared Error (RMSE) on test data = {:.2f}".format(rmse))

    current_time = datetime.now()
    next_hour_time = current_time + timedelta(hours=1)

    next_hour_features = [
        next_hour_time.hour,
        next_hour_time.weekday() + 1,
        next_hour_time.month,
        next_hour_time.year,
    ]
    print("Next hour's features:", next_hour_features)

    next_hour_df = spark.createDataFrame([next_hour_features], selected_features)
    assembler = VectorAssembler(inputCols=selected_features, outputCol="features")
    next_hour_df = assembler.transform(next_hour_df)
    next_hour_predictions = lr_model.transform(next_hour_df)
    next_hour_predicted_pickups = next_hour_predictions.select("prediction").collect()[
        0
    ][0]

    print("Predicted number of pickups in the next hour:", next_hour_predicted_pickups)
