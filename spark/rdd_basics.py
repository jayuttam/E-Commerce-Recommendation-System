from pyspark.sql import SparkSession

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("EcommerceRDDBasics") \
    .master("local[*]") \
    .getOrCreate()

# 2. Create a Python list
prices = [1000, 2000, 3000, 4000, 5000]

# 3. Convert list into RDD
rdd = spark.sparkContext.parallelize(prices)

# 4. Display all elements
print("Original RDD:")
print(rdd.collect())

# 5. Stop Spark
spark.stop()