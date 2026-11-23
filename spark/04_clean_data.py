
import os
import sys
import csv
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim


# ============================================================
# 1. ENVIRONMENT CONFIGURATION
# ============================================================

# Use the Python interpreter from the active virtual environment
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


# ============================================================
# 2. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "online_retail.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_retail.csv"


# ============================================================
# 3. CREATE SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("EcommerceDataCleaning")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "12")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


try:

    # ========================================================
    # 4. LOAD DATASET
    # ========================================================

    print("\n========== LOADING DATASET ==========\n")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {INPUT_FILE}"
        )

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    original_count = df.count()

    print("Original records:", original_count)

    print("\nOriginal dataset schema:")
    df.printSchema()


    # ========================================================
    # 5. REMOVE DUPLICATE RECORDS
    # ========================================================

    df = df.dropDuplicates()


    # ========================================================
    # 6. REMOVE MISSING CUSTOMER IDs
    # ========================================================

    df = df.filter(
        col("CustomerID").isNotNull()
    )


    # ========================================================
    # 7. REMOVE CANCELLED INVOICES
    # ========================================================

    df = df.filter(
        ~trim(col("InvoiceNo")).startswith("C")
    )


    # ========================================================
    # 8. REMOVE INVALID QUANTITIES
    # ========================================================

    df = df.filter(
        col("Quantity") > 0
    )


    # ========================================================
    # 9. REMOVE INVALID UNIT PRICES
    # ========================================================

    df = df.filter(
        col("UnitPrice") > 0
    )


    # ========================================================
    # 10. REMOVE MISSING STOCK CODES
    # ========================================================

    df = df.filter(
        col("StockCode").isNotNull()
    )


    # ========================================================
    # 11. CLEANING REPORT
    # ========================================================

    cleaned_count = df.count()

    removed_count = original_count - cleaned_count

    print("\n========== CLEANING REPORT ==========\n")

    print("Original records :", original_count)
    print("Cleaned records  :", cleaned_count)
    print("Removed records  :", removed_count)

    print("\n========== CLEANED DATA PREVIEW ==========\n")

    df.show(10, truncate=False)


    # ========================================================
    # 12. SAVE CLEANED DATASET
    # ========================================================

    print("\n========== SAVING CLEANED DATA ==========\n")

    # Remove an existing output file before writing
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    headers = df.columns

    # Write rows incrementally to avoid collecting the
    # entire Spark DataFrame into driver memory.
    with open(
        OUTPUT_FILE,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Write column names
        writer.writerow(headers)

        # Write dataset records
        for row in df.toLocalIterator():
            writer.writerow(row)

    print("Cleaned dataset saved successfully!")
    print("Output file:", OUTPUT_FILE)

    print(
        "File size:",
        round(OUTPUT_FILE.stat().st_size / (1024 * 1024), 2),
        "MB"
    )


    # ========================================================
    # 13. FINAL VERIFICATION
    # ========================================================

    print("\n========== FINAL VERIFICATION ==========\n")

    if OUTPUT_FILE.exists():

        print("File exists: YES")
        print("File size:", OUTPUT_FILE.stat().st_size, "bytes")

        with open(
            OUTPUT_FILE,
            mode="r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            saved_headers = next(reader)
            saved_records = sum(1 for _ in reader)

        print("Saved columns:", len(saved_headers))
        print("Saved records:", saved_records)

        if saved_records == cleaned_count:
            print("\nSUCCESS: Saved record count matches cleaned record count!")
        else:
            print("\nWARNING: Saved record count does not match!")

    else:
        print("ERROR: Output file was not created.")


finally:

    # ========================================================
    # 14. STOP SPARK SESSION
    # ========================================================

    spark.stop()

    print("\nSpark Session Stopped.")
