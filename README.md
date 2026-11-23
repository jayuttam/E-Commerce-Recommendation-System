# 🛒 E-Commerce Recommendation System

> A scalable e-commerce analytics and product recommendation system built using **Apache Spark, PySpark, Spark SQL, Spark MLlib, and Streamlit**.

## 📌 Overview

The **E-Commerce Recommendation System** is a Big Data and Machine Learning project designed to process and analyze large-scale online retail transaction data using **Apache Spark**.

The system uses the **UCI Online Retail dataset** to analyze customer purchasing behavior, product performance, sales patterns, and customer-product interactions. These insights are then used to develop a recommendation system that can suggest relevant products to customers.

The project demonstrates the use of distributed data processing, Spark SQL, RDDs, and machine learning in an e-commerce environment.

---

## 🎯 Objectives

* Process large-scale e-commerce transaction data using Apache Spark.
* Demonstrate Spark RDD transformations and actions.
* Perform structured data analysis using Spark DataFrames.
* Execute analytical queries using Spark SQL.
* Analyze customer and product purchasing behavior.
* Build a product recommendation system using Spark MLlib.
* Evaluate the recommendation/model performance.
* Develop an interactive dashboard using Streamlit.
* Demonstrate how Big Data technologies can be used in real-world e-commerce applications.

---

## 🏗️ System Architecture

```text
                 UCI ONLINE RETAIL DATASET
                           │
                           ▼
                     ┌───────────┐
                     │  PySpark  │
                     └─────┬─────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
              RDDs              DataFrames
                 │                   │
                 │               Spark SQL
                 │                   │
                 │             Data Analytics
                 │                   │
                 └─────────┬─────────┘
                           ▼
                      Data Processing
                           │
                           ▼
                      Spark MLlib
                           │
                           ▼
                  Recommendation Engine
                           │
                           ▼
                    Streamlit Dashboard
```

---

## 🧰 Tech Stack

| Technology          | Purpose                             |
| ------------------- | ----------------------------------- |
| **Python**          | Main programming language           |
| **Apache Spark**    | Distributed data processing         |
| **PySpark**         | Python API for Apache Spark         |
| **Spark RDD**       | Distributed data transformations    |
| **Spark DataFrame** | Structured data processing          |
| **Spark SQL**       | Data analysis and querying          |
| **Spark MLlib**     | Machine learning and recommendation |
| **Streamlit**       | Interactive dashboard               |
| **Plotly**          | Data visualization                  |
| **CSV / Parquet**   | Data storage formats                |
| **Git & GitHub**    | Version control                     |

---

## 📊 Dataset

This project uses the **UCI Online Retail dataset**.

The dataset contains transaction records from an online retail business and includes information such as:

* Invoice number
* Product/Stock code
* Product description
* Quantity
* Invoice date
* Unit price
* Customer ID
* Country

### Dataset Source

**UCI Machine Learning Repository — Online Retail Dataset**

The dataset is used to demonstrate Spark-based processing and customer-product interaction analysis.

---

## 🔍 Key Features

### 1. Big Data Processing

Process transaction data using **PySpark** instead of relying only on traditional single-machine data processing.

### 2. RDD Processing

Demonstrate Spark's Resilient Distributed Dataset abstraction and operations such as:

```text
map()
filter()
reduce()
```

### 3. Spark DataFrame Processing

Transform and analyze structured e-commerce data using Spark DataFrames.

### 4. Spark SQL Analytics

Perform analytical queries such as:

* Top-selling products
* Revenue by product
* Revenue by country
* Customer purchase frequency
* Product popularity
* Category/product-level aggregations
* Customer spending analysis

Example:

```sql
SELECT
    StockCode,
    SUM(Quantity) AS total_quantity
FROM transactions
GROUP BY StockCode
ORDER BY total_quantity DESC;
```

### 5. Recommendation System

Use customer-product interaction data to generate personalized product recommendations using **Spark MLlib**.

Example:

```text
Customer
   │
   ├── Product A
   ├── Product B
   └── Product C
          ↓
   Recommendation Engine
          ↓
   Product D
   Product E
   Product F
```

### 6. Interactive Dashboard

The Streamlit dashboard will provide:

* Key performance indicators
* Product analytics
* Customer analytics
* Sales insights
* Product recommendations
* Interactive charts and filters

---

## 📁 Project Structure

```text
ecommerce-recommendation/
│
├── data/
│   ├── raw/
│   │   └── Online_Retail.xlsx
│   │
│   └── processed/
│
├── notebooks/
│   └── exploration.ipynb
│
├── spark/
│   ├── rdd_processing.py
│   ├── sql_analytics.py
│   ├── preprocessing.py
│   └── recommendation_model.py
│
├── models/
│   └── recommendation_model/
│
├── dashboard/
│   └── app.py
│
├── api/
│   └── main.py
│
├── streaming/
│   ├── producer.py
│   └── spark_streaming.py
│
├── tests/
│
├── requirements.txt
├── README.md
└── architecture.png
```

> **Note:** `api/` and `streaming/` are reserved for optional future extensions. The core version focuses on PySpark, Spark SQL, MLlib, and Streamlit.

---

## 🚀 Project Roadmap

### Phase 1 — Environment Setup

* Install Python
* Install Java/JDK
* Install Apache Spark
* Install PySpark
* Configure VS Code
* Create project repository

### Phase 2 — Dataset Preparation

* Download the UCI Online Retail dataset
* Load the dataset
* Understand the columns
* Handle missing values
* Remove invalid records
* Handle cancelled transactions
* Convert data types
* Create processed data

### Phase 3 — RDD Processing

Implement basic Spark RDD operations:

```text
Raw Data
   ↓
RDD
   ↓
map()
   ↓
filter()
   ↓
reduce()
   ↓
Result
```

### Phase 4 — Spark DataFrames

Convert cleaned data into Spark DataFrames and perform:

* Filtering
* Column transformations
* Aggregations
* Sorting
* Data type conversions

### Phase 5 — Spark SQL

Create temporary views and perform SQL-based analytics.

Examples:

```text
Customer Analysis
Product Analysis
Sales Analysis
Country Analysis
Purchase Analysis
```

### Phase 6 — Recommendation Model

Build the recommendation pipeline:

```text
Customer-Product Interactions
             ↓
       Preprocessing
             ↓
        Feature/Data
          Preparation
             ↓
        Spark MLlib
             ↓
       Train Model
             ↓
       Evaluate Model
             ↓
    Generate Recommendations
```

### Phase 7 — Streamlit Dashboard

Create an interactive web interface containing:

```text
Dashboard
│
├── Overview
├── Product Analytics
├── Customer Analytics
├── Sales Analytics
└── Recommendations
```

### Phase 8 — Optional Advanced Features

After completing the core project, additional technologies can be introduced:

```text
Kafka
  ↓
Spark Streaming
  ↓
Real-Time E-Commerce Events
  ↓
Real
```
