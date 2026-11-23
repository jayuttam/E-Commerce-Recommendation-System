
import os
import sys
import csv
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    explode,
    posexplode
)
from pyspark.ml.recommendation import ALS

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "als_interactions.csv"
)

MAPPING_FILE = (
    BASE_DIR / "data" / "processed"
    / "product_id_mapping.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "top_10_recommendations.csv"
)

# --------------------------------------------------
# PYTHON CONFIGURATION
# --------------------------------------------------

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# --------------------------------------------------
# SPARK SESSION
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("ALSRecommendationModel")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "12")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


def save_dataframe_as_csv(df, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    columns = df.columns

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        count = 0

        for row in df.toLocalIterator():
            writer.writerow(row.asDict())
            count += 1

    return count


try:

    # --------------------------------------------------
    # 1. LOAD DATA
    # --------------------------------------------------

    print("\n========== LOADING ALS DATA ==========")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    product_mapping = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(MAPPING_FILE))
    )

    print("Total interactions:", df.count())

    # --------------------------------------------------
    # 2. TRAIN-TEST SPLIT
    # --------------------------------------------------

    print("\n========== TRAIN-TEST SPLIT ==========")

    training_data, test_data = df.randomSplit(
        [0.8, 0.2],
        seed=42
    )

    print("Training records:", training_data.count())
    print("Testing records:", test_data.count())

    # --------------------------------------------------
    # 3. BUILD ALS MODEL
    # --------------------------------------------------

    print("\n========== TRAINING ALS MODEL ==========")

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

    print("\nALS model trained successfully!")

    # --------------------------------------------------
    # 4. TEST MODEL PREDICTIONS
    # --------------------------------------------------

    print("\n========== SAMPLE TEST PREDICTIONS ==========")

    predictions = model.transform(test_data)

    predictions.select(
        "userId",
        "itemId",
        "rating",
        "prediction"
    ).show(10, truncate=False)

    # --------------------------------------------------
    # 5. GENERATE TOP 10 RECOMMENDATIONS
    # --------------------------------------------------

    print("\n========== GENERATING RECOMMENDATIONS ==========")

    recommendations = model.recommendForAllUsers(10)

    # Convert nested recommendation arrays into rows.
    exploded = (
        recommendations
        .select(
            col("userId"),
            posexplode(col("recommendations")).alias(
                "position", "recommendation"
            )
        )
        .select(
            col("userId"),
            (col("position") + 1).alias("rank"),
            col("recommendation.itemId").alias("itemId"),
            col("recommendation.rating").alias("predictedScore")
        )
    )

    # Convert numeric item IDs back to actual product codes.
    final_recommendations = (
        exploded.join(
            product_mapping,
            on="itemId",
            how="inner"
        )
        .select(
            "userId",
            "rank",
            "itemId",
            "StockCode",
            "predictedScore"
        )
        .orderBy("userId", "rank")
    )

    print("\nTop recommendations preview:")

    final_recommendations.show(20, truncate=False)

    # --------------------------------------------------
    # 6. SAVE RECOMMENDATIONS
    # --------------------------------------------------

    print("\n========== SAVING RECOMMENDATIONS ==========")

    saved_records = save_dataframe_as_csv(
        final_recommendations,
        OUTPUT_FILE
    )

    print("Output file:", OUTPUT_FILE)
    print("Saved recommendation rows:", saved_records)

    print("\nSUCCESS: ALS recommendations generated!")

finally:

    spark.stop()

    print("\nSpark Session Stopped.")
