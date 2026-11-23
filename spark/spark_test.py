
from pyspark.sql import SparkSession

# 1. Create a Spark session
spark = (
    SparkSession.builder
    .appName("EcommerceRecommendationSystem")
    .master("local[*]")
    .getOrCreate()
)

print("Spark Session Created Successfully!")

# 2. Create sample e-commerce data
data = [
    (1, "Laptop", "Electronics", 55000),
    (2, "Keyboard", "Accessories", 1500),
    (3, "Mouse", "Accessories", 800),
    (4, "Mobile", "Electronics", 25000),
    (5, "Headphones", "Accessories", 2000)
]

columns = ["product_id", "product_name", "category", "price"]

# 3. Convert data into a Spark DataFrame
df = spark.createDataFrame(data, columns)

# 4. Display the data
print("\nE-commerce Product Data:")

df.show()

# 5. Perform a transformation
electronics = df.filter(df.category == "Electronics")

print("\nElectronics Products:")

electronics.show()

# 6. Count total products
print("Total products:", df.count())

# 7. Stop Spark
spark.stop()

print("Spark Application Completed Successfully!")
