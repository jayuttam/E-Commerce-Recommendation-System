import sys
from pathlib import Path

BASE_DIR = Path(r"c:\Users\Jay Uttam\Documents\ecommerce-recommendation")
HTML_FILE = BASE_DIR / "Ecommerce_Recommendation_System_Report.html"
MD_FILE = BASE_DIR / "Ecommerce_Recommendation_System_Report.md"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>E-Commerce Recommendation System — Project Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');
  
  :root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --navy: #0f172a;
    --slate: #1e293b;
    --slate-light: #64748b;
    --bg-light: #f8fafc;
    --border: #e2e8f0;
    --card-bg: #ffffff;
    --green: #10b981;
    --cyan: #0ea5e9;
    --red: #ef4444;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-light);
    color: var(--navy);
    line-height: 1.65;
    padding: 40px 20px;
  }

  .container {
    max-width: 960px;
    margin: 0 auto;
    background: var(--card-bg);
    padding: 60px 80px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid var(--border);
  }

  @media print {
    body { background: #fff; padding: 0; }
    .container { box-shadow: none; border: none; padding: 20px 40px; max-width: 100%; }
    .no-print { display: none; }
    h1, h2, h3 { page-break-after: avoid; }
    .page-break { page-break-before: always; }
  }

  .print-btn {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(37, 99, 235, 0.3);
    transition: all 0.2s;
  }
  .print-btn:hover { background: var(--primary-dark); }

  .header {
    border-bottom: 2px solid var(--border);
    padding-bottom: 30px;
    margin-bottom: 40px;
  }
  .badge {
    display: inline-block;
    padding: 4px 12px;
    background: #eff6ff;
    color: var(--primary);
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 12px;
  }
  h1 { font-size: 2.3rem; font-weight: 800; color: var(--navy); line-height: 1.25; margin-bottom: 12px; }
  .subtitle { font-size: 1.15rem; color: var(--slate-light); margin-bottom: 20px; }
  .meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    padding: 16px;
    background: #f1f5f9;
    border-radius: 8px;
    font-size: 0.9rem;
  }
  .meta-item strong { color: var(--slate); display: block; }

  h2 { font-size: 1.5rem; font-weight: 700; color: var(--navy); margin: 35px 0 16px 0; border-left: 4px solid var(--primary); padding-left: 12px; }
  h3 { font-size: 1.18rem; font-weight: 600; color: var(--slate); margin: 24px 0 10px 0; }
  p { margin-bottom: 14px; color: #334155; font-size: 1rem; }
  ul, ol { margin-left: 24px; margin-bottom: 16px; color: #334155; }
  li { margin-bottom: 6px; }

  .callout {
    background: #eff6ff;
    border-left: 4px solid var(--primary);
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 24px 0;
  }
  .callout strong { color: var(--primary-dark); display: block; margin-bottom: 4px; }

  .callout-success {
    background: #ecfdf5;
    border-left: 4px solid var(--green);
  }
  .callout-success strong { color: #065f46; }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 0.92rem;
  }
  th, td {
    padding: 12px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }
  th { background: #f8fafc; font-weight: 600; color: var(--slate); }
  tr:hover { background: #f8fafc; }

  .metric-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 24px 0;
  }
  .metric-card {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
  }
  .metric-card .val { font-size: 1.8rem; font-weight: 800; color: var(--primary); }
  .metric-card .lbl { font-size: 0.8rem; font-weight: 600; color: var(--slate-light); text-transform: uppercase; margin-top: 4px; }

  code {
    font-family: 'Fira Code', monospace;
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88rem;
    color: #e11d48;
  }
  pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 18px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: 'Fira Code', monospace;
    font-size: 0.88rem;
    margin: 18px 0;
    line-height: 1.5;
  }

  .qa-box {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
  }
  .qa-box .q { font-weight: 700; color: var(--primary-dark); font-size: 1.05rem; margin-bottom: 8px; }
  .qa-box .a { color: #334155; }
</style>
</head>
<body>

<button class="print-btn no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>

<div class="container">
  <div class="header">
    <div class="badge">Apache Spark &middot; PySpark MLlib &middot; Streamlit &middot; Big Data</div>
    <h1>E-Commerce Recommendation System Using Apache Spark ALS</h1>
    <div class="subtitle">A Scalable Big Data Collaborative Filtering Pipeline and Interactive Web Analytics Platform</div>
    <div class="meta-grid">
      <div class="meta-item"><strong>Author:</strong> Jay Uttam</div>
      <div class="meta-item"><strong>Technology Stack:</strong> Python 3.13, PySpark 4.3.0, Pandas, Streamlit 1.67, Plotly 7.1, Pytest 9.2</div>
      <div class="meta-item"><strong>Dataset:</strong> UCI Online Retail (541k+ Transactions, £8.89M Revenue)</div>
      <div class="meta-item"><strong>Date:</strong> November 2026</div>
    </div>
  </div>

  <h2>1. Executive Summary</h2>
  <p>Modern digital retail platforms face an unprecedented challenge known as <em>catalog overload</em>. With tens of thousands of unique stock keeping units (SKUs) available online, human cognitive bandwidth is insufficient to discover relevant items manually. Consequently, personalized recommendation systems have evolved from auxiliary e-commerce features into foundational revenue drivers. However, real-world retail transaction histories are notoriously sparse, skewed, and predominantly implicit—lacking explicit 1-to-5 star ratings while reflecting purchases, returns, wholesale orders, and system noise.</p>
  <p>This project presents the engineering and empirical validation of an end-to-end, big-data recommendation engine developed with Python, Apache Spark (PySpark), and Streamlit. Utilizing the transnational UCI Online Retail dataset comprising 541,909 transactional records, we design a modular data pipeline that conducts systematic data quality profiling, eliminates operational noise (149,217 defective records removed), and constructs an implicit customer-product interaction matrix of 266,110 pairs across 4,334 verified customers and 3,657 product items.</p>
  
  <div class="metric-cards">
    <div class="metric-card">
      <div class="val">£8.89 M</div>
      <div class="lbl">Cleaned Revenue</div>
    </div>
    <div class="metric-card">
      <div class="val">392,692</div>
      <div class="lbl">Cleaned Transactions</div>
    </div>
    <div class="metric-card">
      <div class="val">266,110</div>
      <div class="lbl">Implicit Interactions</div>
    </div>
    <div class="metric-card">
      <div class="val">2.71x</div>
      <div class="lbl">Precision Gain</div>
    </div>
  </div>

  <div class="callout callout-success">
    <strong>Key Finding & Quantitative Validation</strong>
    Personalized Collaborative Filtering with Implicit ALS achieves <strong>0.1181 Precision@10</strong> and <strong>0.1145 Recall@10</strong> across 4,026 evaluated test users, outperforming the Global Popularity Baseline (0.0435 Precision@10, 0.0383 Recall@10) by <strong>2.71x (+171.5%)</strong> and <strong>2.99x (+198.9%)</strong> respectively.
  </div>

  <h2>2. Problem Statement & Motivation</h2>
  <p>When e-commerce platforms expand their catalogs, customer search friction escalates exponentially. Customers exhibit choice overload (the Paradox of Choice), resulting in shopping cart abandonment and high bounce rates. Traditional navigational search requires the customer to already know the exact product name or category, rendering discovery of complementary or long-tail products nearly impossible.</p>
  <p>Academic literature often demonstrates recommendation algorithms on explicit rating datasets (such as MovieLens 1M/20M or Netflix Prize). In commercial retail, however, less than 2% of shoppers ever submit numerical reviews. Instead, e-commerce data consists almost entirely of transactional logs: invoice IDs, item codes, purchased quantities, and timestamps. Crucially, implicit data possesses no negative feedback: the absence of a purchase does not imply customer distaste; it almost always indicates lack of awareness.</p>

  <h2>3. System Architecture & End-to-End Pipeline</h2>
  <table>
    <thead>
      <tr><th>Pipeline Stage</th><th>Primary Script</th><th>Core Responsibility & Deliverable</th></tr>
    </thead>
    <tbody>
      <tr><td>1. Data Ingestion</td><td><code>spark/01_prepare_data.py</code></td><td>Converts raw Excel workbook to standardized CSV format (<code>data/processed/online_retail.csv</code>).</td></tr>
      <tr><td>2. Quality Profiling</td><td><code>spark/03_data_quality.py</code></td><td>Audits missing keys, invoice cancellations, zero prices, and duplicates across 541k rows.</td></tr>
      <tr><td>3. Distributed Cleaning</td><td><code>spark/04_clean_data.py</code></td><td>Executes Spark filtering, drops 149k corrupted rows, and exports <code>cleaned_retail.csv</code> via streaming.</td></tr>
      <tr><td>4. Feature Engineering</td><td><code>spark/06_create_interactions.py</code><br><code>spark/07_prepare_als_data.py</code></td><td>Filters non-product items, computes <code>ln(1+PurchaseCount)</code>, encodes StockCodes via <code>StringIndexer</code>.</td></tr>
      <tr><td>5. Model Training</td><td><code>spark/08_train_als.py</code></td><td>Trains Spark MLlib Implicit ALS (rank=20, alpha=1.0), generates Top-10 recommendations.</td></tr>
      <tr><td>6. Evaluation & UI</td><td><code>spark/09_evaluate_als.py</code><br><code>dashboard/app.py</code></td><td>Computes Precision@10/Recall@10 against Popularity Baseline; serves 5-page Streamlit UI.</td></tr>
    </tbody>
  </table>

  <h2>4. Data Profiling & Cleaning Pipeline</h2>
  <p>The raw dataset consists of 541,909 records. Automated quality auditing identified severe data anomalies that would corrupt machine learning models if left untreated:</p>
  <ul>
    <li><strong>Missing Customer IDs (135,080 rows / 24.9%):</strong> Guest checkouts lacking customer accounts cannot be personalized via collaborative filtering.</li>
    <li><strong>Cancelled Invoices (9,288 rows):</strong> Invoices starting with 'C' indicate returns, cancellations, and credit refunds.</li>
    <li><strong>Non-Positive Quantities (10,624 rows):</strong> Negative values represent inventory damage, lost stock, and stock adjustments.</li>
    <li><strong>Non-Positive Unit Prices (2,517 rows):</strong> Prices <= £0 indicate promotional samples, bad debt, or company write-offs.</li>
    <li><strong>Duplicate Transactions (5,268 rows):</strong> Exact duplicate rows from browser re-submissions or sync glitches.</li>
  </ul>
  <p>Our PySpark cleaning script purged all 149,217 defective records, producing exactly <strong>392,692 high-integrity transactions</strong>.</p>

  <div class="callout">
    <strong>Windows Platform Compatibility Workaround:</strong>
    On Windows, Spark's native <code>df.write.csv()</code> requires Hadoop <code>winutils.exe</code> and throws <code>UnsatisfiedLinkError</code>. We engineered an incremental streaming exporter using <code>df.toLocalIterator()</code> and Python's built-in <code>csv.writer</code>. This streams partition rows sequentially to disk, avoiding memory bloat and operating smoothly without Hadoop dependencies.
  </div>

  <h2>5. Feature Engineering: The Implicit Interaction Matrix</h2>
  <p>In script <code>06_create_interactions.py</code>, we aggregated transactions at the <code>(CustomerID, StockCode)</code> level after filtering out 8 administrative non-product fees (postage, carriage, bank charges, manual entries, amazon fees, etc.).</p>
  <p>To define interaction strength, we selected the logarithmic scaling of distinct purchase orders:</p>
  <pre>r_{u,i} = ln(1 + PurchaseCount_{u,i})</pre>
  <p><strong>Theoretical Justification:</strong> Distinct order frequency represents true sustained customer preference far better than raw units purchased in a single order (which often reflects one-off accidental bulk buys or wholesale discounting). Applying <code>ln(1 + x)</code> enforces diminishing marginal returns and prevents high-volume purchasers from distorting ALS gradient descent.</p>

  <h2>6. Machine Learning Model Design: Spark MLlib ALS</h2>
  <p>We trained an Alternating Least Squares (ALS) Matrix Factorization model under the Hu-Koren-Volinsky implicit feedback formulation:</p>
  <pre>min_{U,V} ∑_{u,i} c_{u,i} ( p_{u,i} - u_u^T v_i )^2  +  λ ( ∑_u ||u_u||^2 + ∑_i ||v_i||^2 )</pre>
  <ul>
    <li><strong>Binary Preference p_{u,i}:</strong> 1 if r_{u,i} > 0, 0 if unobserved.</li>
    <li><strong>Confidence Weight c_{u,i}:</strong> 1 + α · r_{u,i} (with α = 1.0). Zero interactions carry base confidence 1; purchases scale up confidence.</li>
    <li><strong>Latent Factors (rank = 20):</strong> Captures 20 hidden preference dimensions (vintage decor, kitchen accessories, novelty toys).</li>
    <li><strong>Regularization (λ = 0.1):</strong> L2 penalty preventing parameter vector explosion.</li>
    <li><strong>Non-Negative Constraint (nonnegative = True):</strong> Forces factor matrices to be non-negative, yielding additive, interpretable part-based customer preferences.</li>
  </ul>

  <h2>7. Evaluation Framework & Benchmark Comparison</h2>
  <p>Evaluating implicit recommendation with RMSE is flawed because unobserved items are not negative ratings—they are mostly unseen items. We implemented an 80/20 train/test split with strict <strong>Novelty Enforcement</strong> using a Spark <code>left_anti</code> join to remove previously purchased items from candidate recommendations.</p>
  
  <table>
    <thead>
      <tr><th>Recommendation Model</th><th>Evaluated Users</th><th>Precision@10</th><th>Recall@10</th><th>Relative Multiplier</th></tr>
    </thead>
    <tbody>
      <tr><td>Global Popularity Baseline</td><td>4,026</td><td>0.0435 (4.35%)</td><td>0.0383 (3.83%)</td><td>1.00x (Baseline)</td></tr>
      <tr style="background:#eff6ff; font-weight:600;"><td>Spark MLlib ALS (Ours)</td><td>4,026</td><td>0.1181 (11.81%)</td><td>0.1145 (11.45%)</td><td>2.71x Prec / 2.99x Rec</td></tr>
    </tbody>
  </table>

  <h2>8. Interactive Streamlit Web Application</h2>
  <p>The dashboard in <code>dashboard/app.py</code> provides 5 dedicated modules:</p>
  <ol>
    <li><strong>Overview:</strong> Revenue and order KPIs, interactive date-range filter, and monthly revenue trends.</li>
    <li><strong>Sales Analytics:</strong> Country-level filtering and order volume distributions.</li>
    <li><strong>Product Explorer:</strong> Searchable catalog of 3,665 SKUs with price and order metrics.</li>
    <li><strong>Recommendations:</strong> Customer selector (4,000+ IDs), purchase history inspection, and Top-10 ALS recommendations with novelty badges (New Discovery vs Re-order).</li>
    <li><strong>Model Performance:</strong> Plotly comparative charts benchmarking ALS against Popularity.</li>
  </ol>

  <h2>9. Viva Voce & Oral Defense Handbook (Key Q&As)</h2>
  
  <div class="qa-box">
    <div class="q">Q1: Why did you choose Collaborative Filtering instead of Content-Based Filtering?</div>
    <div class="a">Collaborative filtering discovers latent, cross-category relationships across user shopping behaviors without requiring hand-crafted product feature tagging. It discovers that buyers of vintage clocks also buy floral teacups, even if their metadata keywords share nothing in common.</div>
  </div>

  <div class="qa-box">
    <div class="q">Q2: Why did you use log1p(PurchaseCount) instead of raw quantity?</div>
    <div class="a">Wholesale buyers often purchase 500 units in a single order, which would dominate the matrix. Distinct order count reflects true sustained preference. Applying ln(1 + count) enforces diminishing marginal returns and stabilizes gradient descent.</div>
  </div>

  <div class="qa-box">
    <div class="q">Q3: Why ALS over Stochastic Gradient Descent (SGD)?</div>
    <div class="a">In distributed clusters like Apache Spark, SGD requires sequential parameter updates, creating network synchronization locks. ALS turns a non-convex problem into independent quadratic sub-problems solvable in closed form in parallel across Spark worker nodes without inter-thread locking.</div>
  </div>

  <div class="qa-box">
    <div class="q">Q4: Why evaluate using Precision@10 / Recall@10 instead of RMSE?</div>
    <div class="a">In implicit feedback, RMSE is mathematically meaningless because unobserved items are not negative ratings—they are mostly unseen items. A model predicting zero for all unseen items gets a great RMSE but zero practical utility. In real retail, users only see the Top-N items on screen, making ranking accuracy the true test of commercial value.</div>
  </div>

  <div class="qa-box">
    <div class="q">Q5: How does your system handle the Cold Start Problem?</div>
    <div class="a">In offline evaluation, we configure coldStartStrategy='drop'. In production, we employ a hierarchical fallback: known users receive personalized ALS recommendations; new users with zero history receive the Global or Country-Specific Popularity recommendations precomputed in script 10.</div>
  </div>

  <div class="qa-box">
    <div class="q">Q6: What were your quantitative benchmark results?</div>
    <div class="a">Across 4,026 test users, ALS achieved 11.81% Precision@10 and 11.45% Recall@10, outperforming the Global Popularity baseline (4.35% Precision@10, 3.83% Recall@10) by 2.71x and 2.99x respectively.</div>
  </div>

  <div class="qa-box">
    <div class="q">Q7: How did you handle alphanumeric StockCodes in Spark MLlib?</div>
    <div class="a">Spark ALS strictly requires integer user and item IDs. We used Spark's StringIndexer to map alphanumeric StockCodes into 0-indexed integer itemIds, and maintained a product_id_mapping table to translate predictions back to original SKUs.</div>
  </div>

  <div class="qa-box">
    <div class="q">Q8: How did you bypass Windows Hadoop winutils errors?</div>
    <div class="a">Spark's native write relies on Hadoop winutils.exe on Windows. We avoided this dependency entirely by streaming records partition-by-partition using df.toLocalIterator() directly into Python's native csv.writer, ensuring memory safety and 100% platform independence.</div>
  </div>

  <h2>10. Conclusion</h2>
  <p>This project successfully engineered and empirically validated an industrial-grade E-Commerce Recommendation System using Apache Spark ALS, PySpark, and Streamlit. By addressing the critical realities of commercial retail data—implicit signals, high catalog sparsity (98.32%), wholesale purchase skew, and operational noise—the pipeline transforms raw transaction logs into an accurate, high-speed personalization engine.</p>
</div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML Report generated at: {HTML_FILE}")

# Now generate Markdown Report
md_content = """# E-Commerce Recommendation System Using Apache Spark ALS
### A Scalable Big Data Collaborative Filtering Pipeline and Interactive Web Analytics Platform

**Author:** Jay Uttam  
**Technology Stack:** Python 3.13, Apache Spark (PySpark MLlib 4.3.0), Pandas 3.1.1, Streamlit 1.67.0, Plotly 7.1.0, Pytest 9.2.0  
**Dataset:** UCI Online Retail Dataset (541k+ Transactions, £8.89 Million Cleaned Revenue)  
**Date:** November 2026  

---

## 1. Executive Summary & Abstract
Modern digital retail platforms face an unprecedented challenge known as **catalog overload**. With tens of thousands of unique stock keeping units (SKUs) available online, human cognitive bandwidth is insufficient to discover relevant items manually. Consequently, personalized recommendation systems have evolved from auxiliary e-commerce features into foundational revenue drivers. However, real-world retail transaction histories are notoriously sparse, skewed, and predominantly implicit—lacking explicit 1-to-5 star ratings while reflecting purchases, returns, wholesale orders, and system noise.

This project presents the engineering and empirical validation of an end-to-end, big-data recommendation engine developed with Python, Apache Spark (PySpark), and Streamlit. Utilizing the transnational UCI Online Retail dataset comprising 541,909 transactional records, we design a modular data pipeline that conducts systematic data quality profiling, eliminates operational noise (149,217 defective records removed), and constructs an implicit customer-product interaction matrix of 266,110 pairs across 4,334 verified customers and 3,657 product items.

To model implicit consumer preference, interaction confidence is formulated logarithmically as $r_{u,i} = \\ln(1 + \\text{PurchaseCount}_{u,i})$. We train an Alternating Least Squares (ALS) Matrix Factorization model under the Hu-Koren-Volinsky implicit feedback paradigm with latent rank $k=20$, L2 regularization $\\lambda=0.1$, confidence rate $\\alpha=1.0$, and non-negativity constraints. Using an 80/20 train/test split, we evaluate ranking performance strictly on unseen products. The proposed ALS model achieves a **Precision@10 of 0.1181 (11.81%)** and a **Recall@10 of 0.1145 (11.45%)** across 4,026 test users—substantially outperforming a Global Popularity Baseline (Precision@10: 0.0435, Recall@10: 0.0383) by **2.71x** and **2.99x** respectively.

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

The collaborative filtering matrix factorization objective decomposes the sparse interaction matrix $R$ ($4,334 \\times 3,657$) into User matrix $U \\in \\mathbb{R}^{m \\times 20}$ and Item matrix $V \\in \\mathbb{R}^{n \\times 20}$ using the loss function:

$$\\min_{U, V} \\sum_{u=1}^m \\sum_{i=1}^n c_{u,i} \\left( p_{u,i} - u_u^T v_i \\right)^2 + \\lambda \\left( \\sum_{u=1}^m \\|u_u\\|_2^2 + \\sum_{i=1}^n \\|v_i\\|_2^2 \\right)$$

Where:
1. **Binary Preference ($p_{u,i}$):**
   $$p_{u,i} = \\begin{cases} 1 & \\text{if } r_{u,i} > 0 \\\\ 0 & \\text{if } r_{u,i} = 0 \\end{cases}$$
2. **Confidence Weighting ($c_{u,i}$):**
   $$c_{u,i} = 1 + \\alpha \\cdot r_{u,i} = 1 + 1.0 \\cdot \\ln(1 + \\text{PurchaseCount}_{u,i})$$
   Zero interactions carry a default baseline confidence of 1; observed purchase orders logarithmically scale up confidence.
3. **L2 Regularization ($\\lambda = 0.1$):**
   Guards against vector norm explosion on high-frequency purchasers.
4. **Non-Negativity Constraint ($u_u \\ge 0, v_i \\ge 0$):**
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
**Answer:** In e-commerce, wholesale buyers purchase hundreds of units in one order, while repeat loyal customers purchase across multiple orders. Distinct order count reflects true preference. Applying $\\ln(1 + \\text{count})$ enforces diminishing marginal utility and compresses extreme outliers, ensuring gradient descent in ALS remains numerically stable.

### Q5: What is the mathematical concept behind Matrix Factorization?
**Answer:** Matrix Factorization decomposes a massive, sparse User-Item interaction matrix $R$ ($m \\times n$) into two low-rank dense matrices: User matrix $U$ ($m \\times k$) and Item matrix $V$ ($n \\times k$), such that $R \\approx U \\cdot V^T$. The dot product $u_u^T \\cdot v_i$ predicts the affinity score.

### Q6: Why did you choose Alternating Least Squares (ALS) instead of Stochastic Gradient Descent (SGD)?
**Answer:** In distributed environments like Apache Spark, SGD requires sequential parameter updates, causing heavy cluster synchronization bottlenecks. ALS fixes one matrix while solving for the other, turning a non-convex problem into independent quadratic problems that can be solved in closed form in parallel across Spark worker nodes without inter-thread locking.

### Q7: Explain the loss function used in your ALS model.
**Answer:** We used the Hu, Koren, and Volinsky implicit loss function: $\\min \\sum c_{ui} (p_{ui} - u_u^T v_i)^2 + \\lambda(||u_u||^2 + ||v_i||^2)$. Here, $p_{ui}$ is binary preference (1 if purchased, 0 otherwise), $c_{ui} = 1 + \\alpha r_{ui}$ is confidence, and $\\lambda$ is L2 regularization.

### Q8: What does the 'rank' parameter represent in Spark ALS?
**Answer:** Rank specifies the number of latent factors ($k=20$). These represent 20 hidden semantic dimensions characterizing user shopping styles and item properties (such as holiday gifts, luxury decor, or kitchen essentials).

### Q9: Why did you set nonnegative=True in ALS?
**Answer:** Non-negative matrix factorization constrains latent factor values to be $\\ge 0$. This ensures latent dimensions represent purely additive, interpretable components of customer preference rather than complex subtractions of negative vectors.

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
**Answer:** Each ALS iteration takes $O(m \\cdot k^3 + |R| \\cdot k^2)$, where $m$ is the number of entities, $k$ is the latent rank, and $|R|$ is the number of non-zero interactions. Because $k=20$ is small, $k^3=8000$ is trivial for modern CPUs, making ALS computationally efficient.

### Q24: What are the primary business benefits of this system for an e-commerce company?
**Answer:** Higher average order value (AOV), increased customer retention, reduced cart abandonment, automated discovery of high-margin long-tail inventory, and automated marketing email personalization.

### Q25: What future enhancements would you propose?
**Answer:** Incorporating deep learning Two-Tower Neural Networks, real-time streaming personalization with Apache Kafka, optimizing for serendipity and catalog diversity with Maximal Marginal Relevance (MMR), and session-based transformer models like BERT4Rec.
"""

with open(MD_FILE, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Markdown Report generated at: {MD_FILE}")
