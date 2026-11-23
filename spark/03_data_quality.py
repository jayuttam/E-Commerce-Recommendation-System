
import os
import sys
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim

# Configure Python executable
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

data_file = (
    BASE_DIR / "data" / "processed" / "online_retail.csv"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("EcommerceDataQuality")
    .master("local[*]")
    .getOrCreate()
)

# Load dataset
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(data_file))
)

# Total records
total_records = df.count()

print("\n========== DATA QUALITY REPORT ==========")

print("Total records:", total_records)

# 1. Missing Customer IDs
missing_customers = df.filter(
    col("CustomerID").isNull()
).count()

print("Missing Customer IDs:", missing_customers)

# 2. Cancelled invoices
cancelled_invoices = df.filter(
    trim(col("InvoiceNo")).startswith("C")
).count()

print("Cancelled invoice records:", cancelled_invoices)

# 3. Invalid quantities
invalid_quantities = df.filter(
    col("Quantity") <= 0
).count()

print("Invalid quantities:", invalid_quantities)

# 4. Invalid prices
invalid_prices = df.filter(
    col("UnitPrice") <= 0
).count()

print("Invalid prices:", invalid_prices)

# 5. Missing product descriptions
missing_descriptions = df.filter(
    col("Description").isNull() |
    (trim(col("Description")) == "")
).count()

print("Missing descriptions:", missing_descriptions)

# 6. Missing StockCodes
missing_stockcodes = df.filter(
    col("StockCode").isNull()
).count()

print("Missing StockCodes:", missing_stockcodes)

# 7. Duplicate records
duplicate_count = total_records - df.dropDuplicates().count()

print("Duplicate records:", duplicate_count)

print("\n========== REPORT COMPLETED ==========")

spark.stop()
