
import os
import sys
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    count,
    countDistinct,
    round,
    desc,
    date_format
)


# ============================================================
# 1. ENVIRONMENT CONFIGURATION
# ============================================================

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


# ============================================================
# 2. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_retail.csv"


# ============================================================
# 3. CREATE SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("EcommerceEDA")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "12")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


try:

    # ========================================================
    # 4. LOAD CLEANED DATA
    # ========================================================

    print("\n========== LOADING CLEANED DATA ==========\n")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    print("Total records:", df.count())

    print("\nDataset Schema:")
    df.printSchema()


    # ========================================================
    # 5. FEATURE ENGINEERING
    # ========================================================

    # Revenue = Quantity * UnitPrice

    df = df.withColumn(
        "Revenue",
        round(col("Quantity") * col("UnitPrice"), 2)
    )

    # Extract month from invoice date

    df = df.withColumn(
        "Month",
        date_format(col("InvoiceDate"), "yyyy-MM")
    )

    # Register temporary SQL view

    df.createOrReplaceTempView("retail")


    # ========================================================
    # 6. GENERAL BUSINESS STATISTICS
    # ========================================================

    print("\n========== GENERAL STATISTICS ==========\n")

    df.select(
        countDistinct("InvoiceNo").alias("Total Invoices"),
        countDistinct("CustomerID").alias("Total Customers"),
        countDistinct("StockCode").alias("Unique Products"),
        countDistinct("Country").alias("Countries"),
        round(sum("Revenue"), 2).alias("Total Revenue")
    ).show(truncate=False)


    # ========================================================
    # 7. TOP 10 PRODUCTS BY QUANTITY SOLD
    # ========================================================

    print("\n========== TOP 10 PRODUCTS BY QUANTITY ==========\n")

    top_products = (
        df.groupBy("StockCode", "Description")
        .agg(
            sum("Quantity").alias("Total Quantity Sold"),
            round(sum("Revenue"), 2).alias("Total Revenue")
        )
        .orderBy(desc("Total Quantity Sold"))
        .limit(10)
    )

    top_products.show(truncate=False)


    # ========================================================
    # 8. TOP 10 CUSTOMERS BY REVENUE
    # ========================================================

    print("\n========== TOP 10 CUSTOMERS BY REVENUE ==========\n")

    top_customers = (
        df.groupBy("CustomerID")
        .agg(
            round(sum("Revenue"), 2).alias("Total Spending"),
            countDistinct("InvoiceNo").alias("Total Orders")
        )
        .orderBy(desc("Total Spending"))
        .limit(10)
    )

    top_customers.show(truncate=False)


    # ========================================================
    # 9. COUNTRY-WISE REVENUE
    # ========================================================

    print("\n========== COUNTRY-WISE REVENUE ==========\n")

    country_sales = (
        df.groupBy("Country")
        .agg(
            round(sum("Revenue"), 2).alias("Total Revenue"),
            countDistinct("CustomerID").alias("Total Customers")
        )
        .orderBy(desc("Total Revenue"))
    )

    country_sales.show(20, truncate=False)


    # ========================================================
    # 10. MONTHLY SALES ANALYSIS
    # ========================================================

    print("\n========== MONTHLY SALES ==========\n")

    monthly_sales = (
        df.groupBy("Month")
        .agg(
            round(sum("Revenue"), 2).alias("Monthly Revenue"),
            countDistinct("InvoiceNo").alias("Total Orders")
        )
        .orderBy("Month")
    )

    monthly_sales.show(50, truncate=False)


    # ========================================================
    # 11. SPARK SQL ANALYSIS
    # ========================================================

    print("\n========== SPARK SQL ANALYSIS ==========\n")

    sql_result = spark.sql("""
        SELECT
            Description,
            SUM(Quantity) AS total_quantity,
            ROUND(SUM(Quantity * UnitPrice), 2) AS total_revenue
        FROM retail
        GROUP BY Description
        ORDER BY total_revenue DESC
        LIMIT 10
    """)

    print("Top 10 products by revenue using Spark SQL:")

    sql_result.show(truncate=False)


finally:

    # ========================================================
    # 12. STOP SPARK SESSION
    # ========================================================

    spark.stop()

    print("\nSpark Session Stopped.")
