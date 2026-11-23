import os
import sys
from pathlib import Path

from pyspark.sql import SparkSession

# Configure Python executable for Windows
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# CSV dataset path
data_file = BASE_DIR / "data" / "processed" / "online_retail.csv"

# Create Spark session
spark = (
    SparkSession.builder
    .appName("EcommerceRecommendationSystem")
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

# Display dataset
print("\n========== DATASET PREVIEW ==========")
df.show(10, truncate=False)

# Display schema
print("\n========== DATASET SCHEMA ==========")
df.printSchema()

# Display total rows
print("\n========== DATASET STATISTICS ==========")
print("Total records:", df.count())

# Stop Spark
spark.stop()