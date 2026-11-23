
import os
import sys
import csv
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    countDistinct,
    sum as spark_sum,
    round as spark_round,
    log1p,
    lower,
    trim,
)

# --------------------------------------------------
# PATHS AND PYTHON CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_retail.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "customer_product_interactions.csv"

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# --------------------------------------------------
# CREATE SPARK SESSION
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("CustomerProductInteractions")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "12")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

try:
    # --------------------------------------------------
    # 1. LOAD CLEANED DATA
    # --------------------------------------------------

    print("\n========== LOADING CLEANED DATA ==========")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    print("Total transaction records:", df.count())

    # --------------------------------------------------
    # 2. EXCLUDE NON-PRODUCT TRANSACTIONS
    # --------------------------------------------------

    print("\n========== FILTERING NON-PRODUCT ITEMS ==========")

    non_product_pattern = (
    "postage|carriage|manual|bank charges|discount|adjustment|"
    "commission|amazon fee|cruk"
)

    df = df.filter(
        ~lower(trim(col("Description"))).rlike(non_product_pattern)
    )

    print("Records after item filtering:", df.count())

    # --------------------------------------------------
    # 3. CALCULATE CUSTOMER-PRODUCT INTERACTIONS
    # --------------------------------------------------

    print("\n========== CREATING INTERACTIONS ==========")

    interactions = (
        df.groupBy("CustomerID", "StockCode")
        .agg(
            countDistinct("InvoiceNo").alias("PurchaseCount"),
            spark_sum("Quantity").alias("TotalQuantity"),
            spark_round(
                spark_sum(col("Quantity") * col("UnitPrice")), 2
            ).alias("TotalSpend")
        )
        .withColumn(
            "InteractionStrength",
            log1p(col("PurchaseCount"))
        )
        .select(
            col("CustomerID").cast("long"),
            col("StockCode"),
            col("PurchaseCount"),
            col("TotalQuantity"),
            col("TotalSpend"),
            col("InteractionStrength")
        )
    )

    total_interactions = interactions.count()

    print("Total customer-product interactions:", total_interactions)

    # --------------------------------------------------
    # 4. DISPLAY SAMPLE
    # --------------------------------------------------

    print("\n========== INTERACTION DATA PREVIEW ==========")

    interactions.orderBy(
        col("PurchaseCount").desc()
    ).show(10, truncate=False)

    # --------------------------------------------------
    # 5. SAVE CSV WITHOUT HADOOP WRITE
    # --------------------------------------------------

    print("\n========== SAVING INTERACTION DATA ==========")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    columns = interactions.columns

    with open(
        OUTPUT_FILE,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        saved_records = 0

        for row in interactions.toLocalIterator():
            writer.writerow(row.asDict())
            saved_records += 1

    print("\nInteraction dataset saved successfully!")
    print("Output file:", OUTPUT_FILE)
    print("Saved records:", saved_records)
    print("File size:", round(OUTPUT_FILE.stat().st_size / (1024 * 1024), 2), "MB")

    if saved_records == total_interactions:
        print("\nSUCCESS: All interactions saved!")
    else:
        print("\nWARNING: Saved record count does not match!")

finally:
    spark.stop()
    print("\nSpark Session Stopped.")
