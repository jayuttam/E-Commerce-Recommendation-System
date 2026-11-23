
import os
import sys
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, explode, posexplode, row_number,
    count, sum as spark_sum, lit, avg
)
from pyspark.sql.window import Window
from pyspark.ml.recommendation import ALS

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "als_interactions.csv"

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ALSEvaluation")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "12")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

try:
    print("\n========== LOADING DATA ==========")

    df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    training_data, test_data = df.randomSplit(
        [0.8, 0.2], seed=42
    )

    print("Training records:", training_data.count())
    print("Testing records:", test_data.count())

    print("\n========== TRAINING ALS ==========")

    als = ALS(
        userCol="userId",
        itemCol="itemId",
        ratingCol="rating",
        rank=20,
        maxIter=10,
        regParam=0.1,
        implicitPrefs=True,
        alpha=1.0,
        nonnegative=True,
        coldStartStrategy="drop",
        seed=42
    )

    model = als.fit(training_data)

    print("Model trained successfully!")

    print("\n========== PREPARING TEST DATA ==========")

    # Only evaluate users and products known to training.
    train_users = training_data.select("userId").distinct()
    train_items = training_data.select("itemId").distinct()

    relevant_items = (
        test_data
        .join(train_users, "userId", "inner")
        .join(train_items, "itemId", "inner")
        .select("userId", "itemId")
        .distinct()
    )

    relevant_counts = (
        relevant_items
        .groupBy("userId")
        .agg(count("*").alias("relevant_count"))
    )

    print("Eligible test interactions:", relevant_items.count())

    print("\n========== GENERATING CANDIDATE RECOMMENDATIONS ==========")

    # Generate 50 candidates so filtering previously
    # purchased products still leaves enough recommendations.
    recommendations = model.recommendForAllUsers(50)

    exploded = (
        recommendations
        .select(
            col("userId"),
            posexplode("recommendations")
            .alias("position", "recommendation")
        )
        .select(
            "userId",
            col("recommendation.itemId").alias("itemId"),
            col("recommendation.rating").alias("score")
        )
    )

    # Remove products already present in training data.
    unseen = exploded.join(
        training_data.select("userId", "itemId").distinct(),
        ["userId", "itemId"],
        "left_anti"
    )

    # Re-rank after filtering.
    rank_window = Window.partitionBy("userId").orderBy(
        col("score").desc()
    )

    top10 = (
        unseen
        .withColumn("rank", row_number().over(rank_window))
        .filter(col("rank") <= 10)
        .select("userId", "itemId", "rank")
    )

    print("Top 10 recommendations prepared.")

    print("\n========== CALCULATING METRICS ==========")

    # A hit means the recommended product appears in test data.
    hits = (
        top10
        .join(relevant_items, ["userId", "itemId"], "inner")
        .groupBy("userId")
        .agg(count("*").alias("hits"))
    )

    per_user = (
        relevant_counts
        .join(hits, "userId", "left")
        .fillna(0, subset=["hits"])
        .withColumn(
            "precision_at_10",
            col("hits") / lit(10.0)
        )
        .withColumn(
            "recall_at_10",
            col("hits") / col("relevant_count")
        )
    )

    results = per_user.agg(
        avg("precision_at_10").alias("Precision@10"),
        avg("recall_at_10").alias("Recall@10"),
        count("*").alias("Evaluated users")
    ).first()

    print("\n========== FINAL EVALUATION RESULTS ==========")
    print("Evaluated users:", results["Evaluated users"])
    print("Precision@10:", round(results["Precision@10"], 4))
    print("Recall@10:", round(results["Recall@10"], 4))

    print("\n========== SAMPLE USER METRICS ==========")
    per_user.show(10, truncate=False)

    print("\nSUCCESS: ALS evaluation completed!")

finally:
    spark.stop()
    print("\nSpark Session Stopped.")
