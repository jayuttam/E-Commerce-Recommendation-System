# E-Commerce Recommendation System Using Apache Spark ALS
### A Scalable Big Data Collaborative Filtering Pipeline and Interactive Web Analytics Platform

**Author:** Jay Uttam  
**Technology Stack:** Python 3.13, Apache Spark (PySpark MLlib 4.3.0), Pandas 3.1.1, Streamlit 1.67.0, Plotly 7.1.0, Pytest 9.2.0  
**Dataset:** UCI Online Retail Dataset (541k+ Transactions, £8.89 Million Cleaned Revenue)  
**Date:** November 2026  

---

## 1. Executive Summary & Abstract
Modern digital retail platforms face an unprecedented challenge known as **catalog overload**. With tens of thousands of unique stock keeping units (SKUs) available online, human cognitive bandwidth is insufficient to discover relevant items manually. Consequently, personalized recommendation systems have evolved from auxiliary e-commerce features into foundational revenue drivers. However, real-world retail transaction histories are notoriously sparse, skewed, and predominantly implicit—lacking explicit 1-to-5 star ratings while reflecting purchases, returns, wholesale orders, and system noise.

This project presents the engineering and empirical validation of an end-to-end, big-data recommendation engine developed with Python, Apache Spark (PySpark), and Streamlit. Utilizing the transnational UCI Online Retail dataset comprising 541,909 transactional records, we design a modular data pipeline that conducts systematic data quality profiling, eliminates operational noise (149,217 defective records removed), and constructs an implicit customer-product interaction matrix of 266,110 pairs across 4,334 verified customers and 3,657 product items.

To model implicit consumer preference, interaction confidence is formulated logarithmically as $r_{u,i} = \ln(1 + \text{PurchaseCount}_{u,i})$. We train an Alternating Least Squares (ALS) Matrix Factorization model under the Hu-Koren-Volinsky implicit feedback paradigm with latent rank $k=20$, L2 regularization $\lambda=0.1$, confidence rate $\alpha=1.0$, and non-negativity constraints. Using an 80/20 train/test split, we evaluate ranking performance strictly on unseen products. The proposed ALS model achieves a **Precision@10 of 0.1181 (11.81%)** and a **Recall@10 of 0.1145 (11.45%)** across 4,026 test users—substantially outperforming a Global Popularity Baseline (Precision@10: 0.0435, Recall@10: 0.0383) by **2.71x** and **2.99x** respectively.

---

## 2. Key Project Statistics At A Glance

| Metric Name | Value | Technical Context |
| :--- | :--- | :--- |
| **Raw Dataset Size** | 541,909 rows | UCI Machine Learning Repository Online Retail transaction logs |
| **Cleaned Dataset Size** | 392,692 rows | 100% verified transactional events (149k corrupted rows purged) |
| **Total Net Cleaned Revenue** | **£8,887,208.89** (~£8.89M) | Gross e-commerce turnover across 37 countries |
| **Distinct Invoices** | 18,532 orders | Unique checkout events across 12 months |
| **Active Customers** | 4,338 accounts | Customers with verified positive purchases |
| **Catalog Products (SKUs)** | 3,665 unique items | Distinct giftware products and home decor SKUs |
| **Implicit Interaction Pairs** | **266,110 pairs** | Aggregated `(CustomerID, StockCode)` interaction entries |
| **Catalog Matrix Density** | **1.68%** | Matrix Sparsity: **98.32%** empty cells |
| **Evaluated Test Customers** | 4,026 users | Customers with interactions in both train and test partitions |
| **ALS Model Precision@10** | **0.1181 (11.81%)** | Top-10 ranking precision on novel unseen products |
| **Popularity Precision@10** | **0.0435 (4.35%)** | Global benchmark precision on novel unseen products |
| **Precision Improvement** | **2.71x Multiplier** | **+171.5%** relative gain over popularity baseline |
| **Recall Improvement** | **2.99x Multiplier** | **+198.9%** relative gain over popularity baseline |

---

## 3. System Architecture & Pipeline Design

```
+-----------------------------------------------------------------------------------+
|                            END-TO-END PIPELINE ARCHITECTURE                       |
+-----------------------------------------------------------------------------------+
|  1. Data Ingestion & Quality Audit (spark/01_prepare_data.py, 03_data_quality.py) |
|     • Convert raw Excel to CSV; profile null keys, cancellations, price anomalies |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  2. Distributed Spark Data Cleaning (spark/04_clean_data.py)                      |
|     • Filter 135k null CustomerIDs, 9.2k returns ('C'), 10.6k non-positive qtys   |
|     • Custom df.toLocalIterator() streaming CSV export (Windows Hadoop workaround) |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  3. Feature Engineering & ALS Preparation (spark/06_create_interactions.py, 07)   |
|     • Filter 8 non-product fees (postage, amazon fee, discounts)                  |
|     • Interaction Strength: r_ui = ln(1 + PurchaseCount)                          |
|     • StringIndexer encoding: alphanumeric StockCode -> integer itemId mapping    |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  4. Spark MLlib ALS Model Training (spark/08_train_als.py)                        |
|     • 80/20 split, rank=20, maxIter=10, regParam=0.1, alpha=1.0, nonnegative=True |
|     • model.recommendForAllUsers(10) -> join product mapping -> CSV export        |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  5. Rigorous Ranking Evaluation & Benchmark (spark/09_evaluate_als.py, 10)        |
|     • Left_anti join against training data enforces Novelty (unseen items only!)  |
|     • Precision@10 & Recall@10 comparison: ALS (11.81%) vs Popularity (4.35%)     |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  6. Interactive Streamlit Web Platform (dashboard/app.py)                         |
|     • 5 Pages: Overview, Sales Analytics, Product Explorer, Recs, Model Perf     |
|     • In-memory caching (@st.cache_data), Plotly charts, Novelty badges          |
+-----------------------------------------------------------------------------------+
```

---

## 4. Mathematical Formulation: Hu-Koren-Volinsky Implicit ALS

The collaborative filtering matrix factorization objective decomposes the sparse interaction matrix $R$ ($4,334 \times 3,657$) into User matrix $U \in \mathbb{R}^{m \times 20}$ and Item matrix $V \in \mathbb{R}^{n \times 20}$ using the loss function:

$$\min_{U, V} \sum_{u=1}^m \sum_{i=1}^n c_{u,i} \left( p_{u,i} - u_u^T v_i \right)^2 + \lambda \left( \sum_{u=1}^m \|u_u\|_2^2 + \sum_{i=1}^n \|v_i\|_2^2 \right)$$

Where:
1. **Binary Preference ($p_{u,i}$):**
   $$p_{u,i} = \begin{cases} 1 & \text{if } r_{u,i} > 0 \\ 0 & \text{if } r_{u,i} = 0 \end{cases}$$
2. **Confidence Weighting ($c_{u,i}$):**
   $$c_{u,i} = 1 + \alpha \cdot r_{u,i} = 1 + 1.0 \cdot \ln(1 + \text{PurchaseCount}_{u,i})$$
   Zero interactions carry a default baseline confidence of 1; observed purchase orders logarithmically scale up confidence.
3. **L2 Regularization ($\lambda = 0.1$):**
   Guards against vector norm explosion on high-frequency purchasers.
4. **Non-Negativity Constraint ($u_u \ge 0, v_i \ge 0$):**
   Enforces additive, interpretable latent components.

---

## 5. Experimental Benchmark Results

| Model Evaluated | Evaluated Users | Precision@10 | Recall@10 | Relative Performance |
| :--- | :--- | :--- | :--- | :--- |
| **Global Popularity Baseline** | 4,026 | 0.0435 (4.35%) | 0.0383 (3.83%) | 1.00x (Baseline) |
| **Spark MLlib Implicit ALS (Ours)** | 4,026 | **0.1181 (11.81%)** | **0.1145 (11.45%)** | **2.71x Precision / 2.99x Recall** |

---

## 6. Comprehensive Viva Voce Defense Handbook (Top 25 Q&As)

### Q1: What is the core objective of your project?
**Answer:** To design, build, and empirically validate an industrial-grade, distributed recommendation engine using Apache Spark MLlib ALS that extracts implicit behavioral signals from transaction logs, statistically outperforms baseline popularity in ranking accuracy, and serves real-time insights via an interactive Streamlit dashboard.

### Q2: Why did you choose Collaborative Filtering over Content-Based Filtering?
**Answer:** Collaborative filtering discovers latent, serendipitous relationships across user behavior without requiring extensive manual feature engineering of product attributes. It effectively captures cross-category shopping patterns that pure text or category metadata cannot anticipate.

### Q3: What is the fundamental difference between explicit and implicit feedback?
**Answer:** Explicit feedback consists of conscious user evaluations (like 1-5 star ratings or thumbs up/down). Implicit feedback consists of observational behavioral logs (orders, clicks, quantities). Implicit data has no explicit negative ratings (non-purchase != dislike; usually unawareness) and requires confidence weighting rather than direct rating prediction.

### Q4: Why did you use log1p(PurchaseCount) to formulate interaction strength?
**Answer:** In e-commerce, wholesale buyers purchase hundreds of units in one order, while repeat loyal customers purchase across multiple orders. Distinct order count reflects true preference. Applying $\ln(1 + \text{count})$ enforces diminishing marginal utility and compresses extreme outliers, ensuring gradient descent in ALS remains numerically stable.

### Q5: What is the mathematical concept behind Matrix Factorization?
**Answer:** Matrix Factorization decomposes a massive, sparse User-Item interaction matrix $R$ ($m \times n$) into two low-rank dense matrices: User matrix $U$ ($m \times k$) and Item matrix $V$ ($n \times k$), such that $R \approx U \cdot V^T$. The dot product $u_u^T \cdot v_i$ predicts the affinity score.

### Q6: Why did you choose Alternating Least Squares (ALS) instead of Stochastic Gradient Descent (SGD)?
**Answer:** In distributed environments like Apache Spark, SGD requires sequential parameter updates, causing heavy cluster synchronization bottlenecks. ALS fixes one matrix while solving for the other, turning a non-convex problem into independent quadratic problems that can be solved in closed form in parallel across Spark worker nodes without inter-thread locking.

### Q7: Explain the loss function used in your ALS model.
**Answer:** We used the Hu, Koren, and Volinsky implicit loss function: $\min \sum c_{ui} (p_{ui} - u_u^T v_i)^2 + \lambda(||u_u||^2 + ||v_i||^2)$. Here, $p_{ui}$ is binary preference (1 if purchased, 0 otherwise), $c_{ui} = 1 + \alpha r_{ui}$ is confidence, and $\lambda$ is L2 regularization.

### Q8: What does the 'rank' parameter represent in Spark ALS?
**Answer:** Rank specifies the number of latent factors ($k=20$). These represent 20 hidden semantic dimensions characterizing user shopping styles and item properties (such as holiday gifts, luxury decor, or kitchen essentials).

### Q9: Why did you set nonnegative=True in ALS?
**Answer:** Non-negative matrix factorization constrains latent factor values to be $\ge 0$. This ensures latent dimensions represent purely additive, interpretable components of customer preference rather than complex subtractions of negative vectors.

### Q10: Why did you evaluate using Precision@10 and Recall@10 instead of RMSE?
**Answer:** In implicit recommendation, RMSE is mathematically flawed because unobserved entries are not negative ratings—they are mostly unseen items. A model predicting zero everywhere gets great RMSE but zero utility. In real e-commerce, users see Top-N items on screen, so ranking accuracy (Precision@10 and Recall@10) measures actual business success.

### Q11: How did you ensure your evaluation tested true product discovery (novelty)?
**Answer:** In script `09_evaluate_als.py`, we performed a Spark `left_anti` join between candidate recommendations and the user's training data. This strictly removes all previously purchased items from the candidate pool, forcing the model to recommend unseen products.

### Q12: What were your quantitative results compared to the baseline?
**Answer:** Across 4,026 test users, ALS achieved a Precision@10 of 11.81% and Recall@10 of 11.45%. The Global Popularity Baseline achieved 4.35% Precision@10 and 3.83% Recall@10. ALS delivered a 2.71x increase in Precision and a 2.99x increase in Recall.

### Q13: What is catalog sparsity, and what was it in your dataset?
**Answer:** Sparsity is the percentage of empty cells in the user-item interaction matrix. With 4,334 users and 3,657 items, there are 15,849,438 possible entries. We had 266,110 interactions, meaning the matrix density is 1.68% and sparsity is 98.32%.

### Q14: How does your system handle the Cold Start Problem for new users?
**Answer:** In offline evaluation, we configure `coldStartStrategy='drop'`. In production, we employ a hierarchical fallback: known users receive personalized ALS recommendations; new users with zero history receive the Global or Country-Specific Popularity recommendations precomputed in script 10.

### Q15: How does your system handle the Cold Start Problem for new products?
**Answer:** Pure collaborative filtering cannot recommend new items with zero purchase history. The industry solution is a hybrid recommender: using content-based embeddings (TF-IDF or BERT) on product descriptions to match new items to similar established items until interaction data accumulates.

### Q16: What major data cleaning steps were performed in PySpark?
**Answer:** We dropped exact duplicates, filtered out 135k null CustomerIDs, removed 9.2k cancelled invoices starting with 'C', filtered non-positive quantities and prices, and excluded non-merchandise fees like postage and discounts.

### Q17: Why did you write data using toLocalIterator() instead of df.write.csv()?
**Answer:** On Microsoft Windows, Spark's native write relies on Hadoop `winutils.exe`, which often throws `UnsatisfiedLinkError`. Using `df.toLocalIterator()` streams records partition-by-partition to Python's csv writer, avoiding driver OOM and ensuring cross-platform stability.

### Q18: How did you handle alphanumeric StockCodes in Spark MLlib?
**Answer:** Spark ALS strictly requires integer user and item IDs. We used Spark's `StringIndexer` to map alphanumeric StockCodes into 0-indexed integer itemIds, and maintained a `product_id_mapping` table to translate predictions back to original SKUs.

### Q19: What role does Apache Spark play that Pandas cannot handle?
**Answer:** Pandas is single-threaded and bound to local RAM, causing crashes when scaling to millions of rows. Apache Spark distributes DataFrames across partitions and worker nodes, parallelizing matrix operations, shuffle joins, and aggregations across cluster cores.

### Q20: What are the main pages in your Streamlit dashboard?
**Answer:** Five pages: 1. Overview (KPI metrics and revenue trends), 2. Sales Analytics (country-level filtering), 3. Product Explorer (catalog search), 4. Recommendations (customer lookup and Top-10 ALS recommendations with novelty badges), 5. Model Performance (Plotly comparative charts).

### Q21: How does your Streamlit dashboard achieve sub-10ms page transitions?
**Answer:** Using Streamlit's `@st.cache_data` decorator. It loads and preprocesses the transaction and recommendation datasets into server memory once, avoiding redundant disk I/O on every user interaction.

### Q22: What tests did you write in Pytest?
**Answer:** We wrote tests validating that cleaned transactions have zero missing CustomerIDs, positive quantities/prices, no cancelled orders, exactly 392,692 rows, and that interaction strength strictly matches numpy's `log1p(PurchaseCount)` across 266,110 rows.

### Q23: What is the time complexity of ALS training?
**Answer:** Each ALS iteration takes $O(m \cdot k^3 + |R| \cdot k^2)$, where $m$ is the number of entities, $k$ is the latent rank, and $|R|$ is the number of non-zero interactions. Because $k=20$ is small, $k^3=8000$ is trivial for modern CPUs, making ALS computationally efficient.

### Q24: What are the primary business benefits of this system for an e-commerce company?
**Answer:** Higher average order value (AOV), increased customer retention, reduced cart abandonment, automated discovery of high-margin long-tail inventory, and automated marketing email personalization.

### Q25: What future enhancements would you propose?
**Answer:** Incorporating deep learning Two-Tower Neural Networks, real-time streaming personalization with Apache Kafka, optimizing for serendipity and catalog diversity with Maximal Marginal Relevance (MMR), and session-based transformer models like BERT4Rec.
