
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    row_number,
    sum as spark_sum
)
from pyspark.sql.window import Window


# ============================================================
# 1. CREATE SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("PopularityBaselineEvaluation")
    .master("local[*]")
    .config("spark.driver.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


# ============================================================
# 2. LOAD INTERACTION DATA
# ============================================================

print("\n========== LOADING DATA ==========")

data_path = "data/processed/als_interactions.csv"

interactions = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(data_path)
    .select(
        col("userId").cast("int"),
        col("itemId").cast("int"),
        col("rating").cast("double")
    )
    .dropna()
)

print("Total interactions:", interactions.count())


# ============================================================
# 3. TRAIN-TEST SPLIT
# ============================================================

print("\n========== TRAIN-TEST SPLIT ==========")

training_data, test_data = interactions.randomSplit(
    [0.8, 0.2],
    seed=42
)

training_data = training_data.cache()
test_data = test_data.cache()

print("Training interactions:", training_data.count())
print("Testing interactions:", test_data.count())


# ============================================================
# 4. IDENTIFY ELIGIBLE TEST INTERACTIONS
# ============================================================

print("\n========== FILTERING TEST DATA ==========")

train_users = training_data.select("userId").distinct()
train_items = training_data.select("itemId").distinct()

relevant_test = (
    test_data
    .join(train_users, "userId", "inner")
    .join(train_items, "itemId", "inner")
)

relevant_counts = (
    relevant_test
    .groupBy("userId")
    .agg(count("*").alias("relevant_count"))
)

print("Eligible test interactions:", relevant_test.count())
print("Evaluated users:", relevant_counts.count())


# ============================================================
# 5. CALCULATE GLOBAL PRODUCT POPULARITY
# ============================================================

print("\n========== CALCULATING PRODUCT POPULARITY ==========")

# Count how many times each product appears in training data.
# Rank products by purchase frequency.
# itemId is used only as a deterministic tie-breaker.

popularity_window = Window.orderBy(
    col("purchase_count").desc(),
    col("itemId").asc()
)

popular_products = (
    training_data
    .groupBy("itemId")
    .agg(count("*").alias("purchase_count"))
    .withColumn(
        "popularity_rank",
        row_number().over(popularity_window)
    )
    .filter(col("popularity_rank") <= 200)
    .select("itemId", "popularity_rank")
)

print("Popular products selected:", popular_products.count())


# ============================================================
# 6. GENERATE PERSONALIZED RECOMMENDATIONS
# ============================================================

print("\n========== GENERATING RECOMMENDATIONS ==========")

# Give every evaluated user the globally popular products.
candidate_recommendations = (
    relevant_counts
    .select("userId")
    .crossJoin(popular_products)
)

# Remove products the user has already purchased in training data.
unseen_recommendations = candidate_recommendations.join(
    training_data.select("userId", "itemId").distinct(),
    ["userId", "itemId"],
    "left_anti"
)

# Preserve global popularity order for each user.
recommendation_window = Window.partitionBy("userId").orderBy(
    col("popularity_rank").asc()
)

top10_recommendations = (
    unseen_recommendations
    .withColumn(
        "rank",
        row_number().over(recommendation_window)
    )
    .filter(col("rank") <= 10)
    .select("userId", "itemId", "rank")
    .cache()
)

print("Generated recommendations:", top10_recommendations.count())


# ============================================================
# 7. CALCULATE HITS
# ============================================================

print("\n========== CALCULATING HITS ==========")

hits = (
    top10_recommendations
    .join(
        relevant_test.select("userId", "itemId"),
        ["userId", "itemId"],
        "inner"
    )
    .groupBy("userId")
    .agg(count("*").alias("hits"))
)

user_metrics = (
    relevant_counts
    .join(hits, "userId", "left")
    .fillna(0, subset=["hits"])
    .withColumn(
        "precision_at_10",
        col("hits") / 10.0
    )
    .withColumn(
        "recall_at_10",
        col("hits") / col("relevant_count")
    )
)


# ============================================================
# 8. CALCULATE FINAL METRICS
# ============================================================

print("\n========== FINAL EVALUATION ==========")

final_metrics = user_metrics.agg(
    spark_sum("precision_at_10").alias("precision_sum"),
    spark_sum("recall_at_10").alias("recall_sum"),
    count("*").alias("total_users")
).collect()[0]

total_users = final_metrics["total_users"]

precision_at_10 = (
    final_metrics["precision_sum"] / total_users
)

recall_at_10 = (
    final_metrics["recall_sum"] / total_users
)

print("\n========== POPULARITY BASELINE RESULTS ==========")

print("Evaluated users:", total_users)

print("Precision@10:", round(precision_at_10, 4))
print("Recall@10:", round(recall_at_10, 4))


# ============================================================
# 9. DISPLAY SAMPLE USER METRICS
# ============================================================

print("\n========== SAMPLE USER METRICS ==========")

user_metrics.select(
    "userId",
    "relevant_count",
    "hits",
    "precision_at_10",
    "recall_at_10"
).orderBy("userId").show(10, truncate=False)


# ============================================================
# 10. CLEANUP
# ============================================================

training_data.unpersist()
test_data.unpersist()
top10_recommendations.unpersist()

spark.stop()

print("\nPopularity baseline evaluation completed successfully!")
