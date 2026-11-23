
import os
import sys
import csv
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "customer_product_interactions.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "als_interactions.csv"
)

MAPPING_FILE = (
    BASE_DIR / "data" / "processed"
    / "product_id_mapping.csv"
)

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("PrepareALSData")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "12")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


def save_dataframe_as_csv(df, output_file):
    """Save a Spark DataFrame using Python CSV to avoid
    the Windows Hadoop native-write dependency."""

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
    print("\n========== LOADING INTERACTION DATA ==========")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    print("Total interactions:", df.count())

    print("\n========== CREATING USER IDS ==========")

    df = df.withColumn(
        "userId",
        col("CustomerID").cast("int")
    )

    print("User IDs created.")

    print("\n========== CREATING PRODUCT IDS ==========")

    indexer = StringIndexer(
        inputCol="StockCode",
        outputCol="itemId",
        handleInvalid="error",
        stringOrderType="alphabetAsc"
    )

    indexer_model = indexer.fit(df)

    df = indexer_model.transform(df)

    df = df.withColumn(
        "itemId",
        col("itemId").cast("int")
    )

    print("Product IDs created.")
    print("Number of products:", len(indexer_model.labels))

    print("\n========== PREPARING ALS DATA ==========")

    als_df = df.select(
        "CustomerID",
        "StockCode",
        "userId",
        "itemId",
        col("InteractionStrength").alias("rating")
    )

    print("\nALS dataset preview:")
    als_df.show(10, truncate=False)

    print("\n========== DATA VALIDATION ==========")

    print("Total records:", als_df.count())
    print("Unique users:", als_df.select("userId").distinct().count())
    print("Unique products:", als_df.select("itemId").distinct().count())

    invalid_records = als_df.filter(
        col("userId").isNull()
        | col("itemId").isNull()
        | col("rating").isNull()
        | (col("rating") <= 0)
    ).count()

    print("Invalid records:", invalid_records)

    print("\n========== CREATING PRODUCT MAPPING ==========")

    product_mapping = spark.createDataFrame(
        [
            (index, stock_code)
            for index, stock_code
            in enumerate(indexer_model.labels)
        ],
        ["itemId", "StockCode"]
    )

    print("Product mapping preview:")
    product_mapping.show(10, truncate=False)

    print("\n========== SAVING ALS DATA ==========")

    saved = save_dataframe_as_csv(
        als_df,
        OUTPUT_FILE
    )

    mapping_saved = save_dataframe_as_csv(
        product_mapping,
        MAPPING_FILE
    )

    print("\nALS data saved:", OUTPUT_FILE)
    print("Saved interaction records:", saved)

    print("\nProduct mapping saved:", MAPPING_FILE)
    print("Saved product mappings:", mapping_saved)

    if saved == als_df.count() and invalid_records == 0:
        print("\nSUCCESS: ALS data preparation completed!")
    else:
        print("\nWARNING: Please investigate the validation results.")

finally:
    spark.stop()
    print("\nSpark Session Stopped.")

