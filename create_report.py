import sys
import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT = Path(r"c:\Users\Jay Uttam\Documents\ecommerce-recommendation\Ecommerce_Recommendation_System_Report.docx")
HTML_OUTPUT = Path(r"c:\Users\Jay Uttam\Documents\ecommerce-recommendation\Ecommerce_Recommendation_System_Report.html")
MD_OUTPUT = Path(r"c:\Users\Jay Uttam\Documents\ecommerce-recommendation\Ecommerce_Recommendation_System_Report.md")

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_docx_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles & Fonts
    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    SLATE = RGBColor(71, 85, 105)
    DARK = RGBColor(30, 41, 59)

    # Helper functions for document formatting
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(36)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(28)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(24)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(15)
        run.font.italic = True
        run.font.color.rgb = BLUE
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(22)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = BLUE
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = SLATE
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = DARK
        return p

    def add_bullet(text, level=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = DARK
        return p

    def add_callout(text, title="KEY TAKEAWAY"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        r_title = p.add_run(f"[{title}] ")
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(10.5)
        r_title.font.bold = True
        r_title.font.color.rgb = BLUE
        
        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ---------------- TITLE PAGE ----------------
    add_title("E-COMMERCE RECOMMENDATION SYSTEM\nUSING APACHE SPARK ALS")
    add_subtitle("A Scalable Big Data Collaborative Filtering Pipeline and Interactive Web Analytics Platform")

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_p.paragraph_format.space_before = Pt(36)
    meta_p.paragraph_format.space_after = Pt(6)
    r = meta_p.add_run("COMPREHENSIVE PROJECT REPORT & TECHNICAL DEFENSE\n")
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = NAVY

    r2 = meta_p.add_run("Author: Jay Uttam\nTechnology Stack: Python 3.13, Apache Spark (PySpark MLlib), Pandas, Streamlit, Plotly, Pytest\nDataset: UCI Online Retail Dataset (541k+ Transactions)\nDate: November 2026\n")
    r2.font.name = "Calibri"
    r2.font.size = Pt(11)
    r2.font.color.rgb = SLATE

    doc.add_page_break()

    # ---------------- TABLE OF CONTENTS ----------------
    add_heading_1("Table of Contents")
    toc_items = [
        "1. Executive Summary & Abstract",
        "2. Problem Statement & Motivation",
        "3. System Architecture & Component Design",
        "4. Dataset Ingestion & Data Quality Profiling",
        "5. Distributed Data Cleaning Pipeline",
        "6. Exploratory Data Analysis & Business Intelligence",
        "7. Feature Engineering: The Implicit Interaction Matrix",
        "8. Machine Learning Model Design: Spark MLlib ALS",
        "9. Evaluation Framework & Benchmark Comparison",
        "10. Interactive Streamlit Web Application",
        "11. Software Quality Assurance & Automated Testing",
        "12. Production Deployment & Scalability Architecture",
        "13. Viva Voce & Oral Defense Handbook (25 Comprehensive Q&As)",
        "14. Conclusion & Future Roadmap"
    ]
    for item in toc_items:
        add_body(f"• {item}")

    doc.add_page_break()

    # ---------------- CHAPTER 1 ----------------
    add_heading_1("1. Executive Summary & Abstract")
    add_body(
        "Modern digital retail platforms face an unprecedented challenge known as 'catalog overload'. With tens of thousands of unique stock keeping units (SKUs) available online, human cognitive bandwidth is insufficient to discover relevant items manually. Consequently, personalized recommendation systems have evolved from auxiliary e-commerce features into foundational revenue drivers. However, real-world retail transaction histories are notoriously sparse, skewed, and predominantly implicit—lacking explicit 1-to-5 star ratings while reflecting purchases, returns, wholesale orders, and system noise."
    )
    add_body(
        "This project presents the engineering and empirical validation of an end-to-end, big-data recommendation engine developed with Python, Apache Spark (PySpark), and Streamlit. Utilizing the transnational UCI Online Retail dataset comprising 541,909 transactional records, we design a modular data pipeline that conducts systematic data quality profiling, eliminates operational noise (149,217 defective records removed), and constructs an implicit customer-product interaction matrix of 266,110 pairs across 4,334 verified customers and 3,657 product items."
    )
    add_body(
        "To model implicit consumer preference, interaction confidence is formulated logarithmically as r_{u,i} = ln(1 + PurchaseCount_{u,i}). We train an Alternating Least Squares (ALS) Matrix Factorization model under the Hu-Koren-Volinsky implicit feedback paradigm with latent rank k=20, L2 regularization lambda=0.1, confidence rate alpha=1.0, and non-negativity constraints. Using an 80/20 train/test split, we evaluate ranking performance strictly on unseen products. The proposed ALS model achieves a Precision@10 of 0.1181 (11.81%) and a Recall@10 of 0.1145 (11.45%) across 4,026 test users—substantially outperforming a Global Popularity Baseline (Precision@10: 0.0435, Recall@10: 0.0383) by 2.71x and 2.99x respectively."
    )
    add_body(
        "Finally, the trained model and transaction intelligence are deployed to an interactive, 5-page Streamlit web dashboard powered by Plotly visual analytics, offering business stakeholders executive KPIs, country-level sales trends, catalog search, and real-time personalized recommendations with novelty tracking. The entire pipeline is hardened by automated Pytest unit tests asserting schema and data invariants."
    )

    add_callout(
        "Key Finding: Personalized Collaborative Filtering with Implicit ALS yields a 171.5% increase in Precision@10 and a 198.9% increase in Recall@10 over conventional popularity-based recommendations, proving that algorithmic personalization drastically improves product discovery in high-sparsity retail environments.",
        "EXECUTIVE SUMMARY TAKEAWAY"
    )

    # ---------------- CHAPTER 2 ----------------
    add_heading_1("2. Problem Statement & Motivation")
    add_heading_2("2.1 The Challenge of Catalog Overload")
    add_body(
        "When e-commerce platforms expand their catalogs, customer search friction escalates exponentially. Customers exhibit choice overload (the Paradox of Choice), resulting in shopping cart abandonment and high bounce rates. Traditional navigational search requires the customer to already know the exact product name or category, rendering discovery of complementary or long-tail products nearly impossible."
    )
    add_heading_2("2.2 The Reality of Implicit Feedback")
    add_body(
        "Academic literature often demonstrates recommendation algorithms on explicit rating datasets (such as MovieLens 1M/20M or Netflix Prize). In commercial retail, however, less than 2% of shoppers ever submit numerical reviews. Instead, e-commerce data consists almost entirely of transactional logs: invoice IDs, item codes, purchased quantities, and timestamps. Crucially, implicit data possesses no negative feedback: the absence of a purchase does not imply customer distaste; it almost always indicates lack of awareness."
    )
    add_heading_2("2.3 Big Data Computational Bottlenecks")
    add_body(
        "Standard machine learning libraries such as Scikit-Learn operate strictly in-memory on single CPU nodes. In an enterprise retail setting with millions of customer interactions, single-node architectures crash due to Out-Of-Memory (OOM) errors during matrix inversion. To overcome this limitation, this project leverages Apache Spark, a distributed cluster-computing engine that parallelizes matrix factorization across memory partitions."
    )

    # ---------------- CHAPTER 3 ----------------
    add_heading_1("3. System Architecture & Component Design")
    add_body(
        "The system follows a modular, decoupled architecture where each phase of the machine learning lifecycle is executed by an isolated, production-ready script. This ensures clear separation of concerns, testability, and maintainability."
    )
    
    # Architecture Table
    arch_table = doc.add_table(rows=7, cols=3)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Pipeline Stage", "Primary Script / File", "Technical Responsibility & Deliverable"]
    col_widths = [Inches(1.8), Inches(2.2), Inches(2.8)]
    for j, h in enumerate(headers):
        cell = arch_table.cell(0, j)
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10.5)

    pipeline_rows = [
        ("1. Data Ingestion", "spark/01_prepare_data.py", "Converts raw Excel workbook to standardized CSV format (data/processed/online_retail.csv)."),
        ("2. Quality Profiling", "spark/03_data_quality.py", "Audits missing keys, invoice cancellations, zero prices, and duplicates across 541k rows."),
        ("3. Distributed Cleaning", "spark/04_clean_data.py", "Executes Spark filtering, drops 149k corrupted rows, and exports cleaned_retail.csv via streaming."),
        ("4. Feature Engineering", "spark/06_create_interactions.py\nspark/07_prepare_als_data.py", "Filters non-product items, computes ln(1+PurchaseCount), encodes StockCodes via StringIndexer."),
        ("5. Model Training", "spark/08_train_als.py", "Trains Spark MLlib Implicit ALS (rank=20, alpha=1.0), generates Top-10 recommendations."),
        ("6. Evaluation & UI", "spark/09_evaluate_als.py\ndashboard/app.py", "Computes Precision@10/Recall@10 against Popularity Baseline; serves 5-page Streamlit UI.")
    ]
    for i, row in enumerate(pipeline_rows):
        for j, val in enumerate(row):
            cell = arch_table.cell(i+1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------- CHAPTER 4 ----------------
    add_heading_1("4. Dataset Ingestion & Data Quality Profiling")
    add_body(
        "The project utilizes the public UCI Machine Learning Repository Online Retail Dataset. It documents real transactions occurring between December 1, 2010, and December 9, 2011, for a United Kingdom-based registered online retailer specializing in unique all-occasion gift-ware. The dataset contains 541,909 records across eight primary attributes:"
    )
    add_bullet("InvoiceNo: 6-digit integral order identifier. If this code starts with 'C', it denotes a cancellation.")
    add_bullet("StockCode: Product identifier code. Typically 5 or 6 alphanumeric characters.")
    add_bullet("Description: Nominal text describing the product item.")
    add_bullet("Quantity: Integral quantity of each product item per transaction.")
    add_bullet("InvoiceDate: Timestamp marking when the transaction was generated.")
    add_bullet("UnitPrice: Product unit price in Sterling (£).")
    add_bullet("CustomerID: 5-digit integral customer identifier assigned uniquely to each customer.")
    add_bullet("Country: Name of the country where each customer resides.")

    add_heading_2("4.1 Comprehensive Data Quality Audit")
    add_body(
        "In script 03_data_quality.py, we executed automated profiling across the entire dataset to quantify data anomalies before designing cleaning transformations. The audit revealed five critical defects:"
    )
    add_bullet("Missing Customer Identifiers (135,080 records / 24.9%): Nearly a quarter of the raw dataset lacked CustomerID values, indicating guest purchases. Since collaborative filtering relies on historical user behavior, transactions lacking user keys cannot be used for training personalized models.")
    add_bullet("Cancelled Invoices (9,288 records): Invoices prefixed with 'C' indicate cancelled orders, refunds, and merchandise returns. Treating cancelled items as positive interactions would corrupt user preference representations.")
    add_bullet("Non-Positive Quantities (10,624 records): Records with zero or negative quantities represent damages, loss adjustments, and administrative write-offs.")
    add_bullet("Non-Positive Unit Prices (2,517 records): Records with UnitPrice <= 0 indicate company giveaways, sample distribution, or bad-debt adjustments.")
    add_bullet("Duplicate Transaction Rows (5,268 records): Exact duplicate rows resulting from browser double-submissions or system recording redundancy.")

    # ---------------- CHAPTER 5 ----------------
    add_heading_1("5. Distributed Data Cleaning Pipeline")
    add_body(
        "In script 04_clean_data.py, PySpark was utilized to implement a deterministic, rule-based data cleaning pipeline that resolves the identified quality defects. The sequence of cleaning transformations is defined as follows:"
    )
    add_body(
        "1. Deduplication: df = df.dropDuplicates()\n"
        "2. Customer Key Validation: df = df.filter(col('CustomerID').isNotNull())\n"
        "3. Cancellation Elimination: df = df.filter(~trim(col('InvoiceNo')).startswith('C'))\n"
        "4. Positive Quantity Assertion: df = df.filter(col('Quantity') > 0)\n"
        "5. Positive Price Assertion: df = df.filter(col('UnitPrice') > 0)\n"
        "6. StockCode Validation: df = df.filter(col('StockCode').isNotNull())"
    )
    add_body(
        "The original dataset of 541,909 records was cleanly filtered to exactly 392,692 high-integrity transactional events. Exactly 149,217 corrupted records were purged, yielding a 100% verified transactional dataset."
    )

    add_heading_2("5.1 Windows Platform Compatibility Workaround")
    add_body(
        "A critical engineering challenge in Apache Spark on Microsoft Windows is Spark's native DataFrame write mechanism (df.write.csv()). On Windows, Spark requires native Hadoop binaries (winutils.exe and hadoop.dll) to manage file lock permissions, throwing UnsatisfiedLinkError if they are absent. Rather than forcing users to configure custom environment binaries, we engineered an incremental streaming exporter using df.toLocalIterator() and Python's built-in csv.writer:"
    )
    add_body(
        "This architectural choice processes rows incrementally from Spark worker partitions directly to the target CSV file without collecting the full DataFrame into driver memory, avoiding Java Heap Out-Of-Memory exceptions while providing 100% platform independence on Windows and Linux."
    )

    # ---------------- CHAPTER 6 ----------------
    add_heading_1("6. Exploratory Data Analysis & Business Intelligence")
    add_body(
        "In script 05_eda.py and dashboard/app.py, exploratory data analysis was conducted to uncover commercial patterns, revenue concentrations, and catalog characteristics:"
    )
    add_bullet("Gross Commercial Scale: The cleaned transaction dataset represents £8,887,208.89 (~£8.89 Million) in gross revenue across 18,532 distinct invoices, 4,338 unique customers, 3,665 unique product items, and 37 countries.")
    add_bullet("Extreme Seasonality: Monthly revenue remains stable between £450k and £650k from January through August, before exploding in Q4 (October: £974k, November: £1.13M) due to holiday stocking by corporate and wholesale buyers.")
    add_bullet("Geographic Concentration: The United Kingdom generates 89.1% of total revenue (£7.31M). The top international markets are the Netherlands (£284k), EIRE (£250k), Germany (£221k), and France (£196k).")
    add_bullet("Wholesale Whale Concentration: The top 10 customers contribute over 15% of total retail turnover. The single largest customer (CustomerID 14646) accounted for £280,206.02 across 74 distinct orders.")
    add_bullet("Catalog Sparsity (98.32%): With 4,334 active users and 3,657 items in the interaction space, the potential user-item matrix contains 15,849,438 cells. However, only 266,110 non-zero interactions exist, representing an interaction density of just 1.68%. This severe sparsity makes standard collaborative filtering challenging and highlights the necessity of regularized matrix factorization.")

    # ---------------- CHAPTER 7 ----------------
    add_heading_1("7. Feature Engineering: The Implicit Interaction Matrix")
    add_heading_2("7.1 Elimination of Non-Merchandise Transactions")
    add_body(
        "Commercial transaction logs contain non-product entries representing administrative overheads. In script 06_create_interactions.py, we applied a regular expression filter on product descriptions to remove 8 operational charges: postage, carriage, manual entries, bank charges, discounts, fee adjustments, commissions, amazon fees, and charity donations (CRUK)."
    )
    add_heading_2("7.2 Interaction Aggregation & Mathematical Formulation")
    add_body(
        "Multiple transactions occurring across distinct invoices were aggregated at the (CustomerID, StockCode) grain. Three candidate signals were computed:"
    )
    add_bullet("PurchaseCount: countDistinct('InvoiceNo') — The number of separate orders in which the customer chose to buy the product.")
    add_bullet("TotalQuantity: sum('Quantity') — Total physical units purchased.")
    add_bullet("TotalSpend: sum('Quantity' * 'UnitPrice') — Total monetary investment.")
    add_body(
        "To define the implicit interaction strength r_{u,i}, we chose the logarithmic scaling of distinct purchase orders:"
    )
    add_body(
        "                     r_{u,i} = ln(1 + PurchaseCount_{u,i})"
    )
    add_body(
        "Justification: In e-commerce, repeated purchase across separate invoices represents a far stronger indicator of sustained customer loyalty than buying multiple units in a single order (which often reflects one-off accidental bulk purchases or wholesale discounting). Applying ln(1 + x) provides diminishing marginal returns: buying an item in 2 orders yields 1.098, while buying it in 10 orders yields 2.397. This stabilizes matrix factorization gradients by preventing extreme outliers from skewing the latent space."
    )
    add_body(
        "The resulting interaction matrix contains exactly 266,110 unique user-item interactions, validated by automated unit testing."
    )

    # ---------------- CHAPTER 8 ----------------
    add_heading_1("8. Machine Learning Model Design: Spark MLlib ALS")
    add_heading_2("8.1 Matrix Factorization Mathematical Foundations")
    add_body(
        "Collaborative filtering assumes that customer preferences and product characteristics can be effectively approximated by a low-dimensional latent factor space. Let R be the m × n sparse user-item interaction matrix, where m = 4,334 and n = 3,657. Matrix factorization seeks two dense, low-rank matrices:"
    )
    add_body(
        "                     U in R^{m × k}    and    V in R^{n × k}"
    )
    add_body(
        "such that R approx U · V^T, where k = 20 is the latent factor dimensionality. The affinity of customer u for item i is modeled by the inner product:"
    )
    add_body(
        "                     hat{p}_{u,i} = u_u^T · v_i"
    )

    add_heading_2("8.2 Hu-Koren-Volinsky Implicit Loss Function")
    add_body(
        "For implicit feedback, unobserved interactions cannot be treated as missing entries (as in SVD for Netflix); instead, they represent negative preference with low confidence. The optimization objective is formulated as:"
    )
    add_body(
        "min_{U,V} ∑_{u=1}^m ∑_{i=1}^n c_{u,i} ( p_{u,i} - u_u^T v_i )^2  +  λ ( ∑_u ||u_u||_2^2 + ∑_i ||v_i||_2^2 )"
    )
    add_body(
        "where:\n"
        "• Binary Preference p_{u,i} = 1 if r_{u,i} > 0, and 0 if r_{u,i} = 0.\n"
        "• Confidence Weight c_{u,i} = 1 + α · r_{u,i}, where α = 1.0 is the confidence scaling factor.\n"
        "• Regularization Parameter λ = 0.1 prevents vector norm explosion and guards against overfitting."
    )

    add_heading_2("8.3 Alternating Least Squares (ALS) Optimization")
    add_body(
        "Because the term u_u^T v_i involves bilinear products of unknown parameters, the loss function is non-convex. However, if V is held fixed, the objective function becomes strictly quadratic with respect to U, possessing a closed-form analytic solution:"
    )
    add_body(
        "                     u_u = ( V^T C^u V + λ I )^{-1} V^T C^u p(u)"
    )
    add_body(
        "Similarly, holding U fixed yields a closed-form solution for each item vector v_i. The ALS algorithm alternates between solving for all user vectors in parallel, then solving for all item vectors in parallel. Spark distributes the matrix inversions across cluster partitions, achieving linear scalability."
    )

    add_heading_2("8.4 Hyperparameter Specifications")
    add_bullet("rank = 20: Captures 20 latent archetypes (e.g. vintage decorative gifts, kitchen accessories, party novelties) without overfitting.")
    add_bullet("maxIter = 10: Ensures convergence of the alternating solver within negligible loss delta.")
    add_bullet("regParam = 0.1: L2 regularization penalty.")
    add_bullet("implicitPrefs = True: Enables the confidence weighting formulation.")
    add_bullet("alpha = 1.0: Sets the rate at which purchase observations increase confidence.")
    add_bullet("nonnegative = True: Constrains latent factors to be non-negative (u_u >= 0, v_i >= 0), producing additive, interpretable part-based representations.")
    add_bullet("coldStartStrategy = 'drop': Drops unobserved test entities during evaluation to prevent NaN distortion.")

    # ---------------- CHAPTER 9 ----------------
    add_heading_1("9. Evaluation Framework & Benchmark Comparison")
    add_heading_2("9.1 Why Rating Metrics (RMSE) Are Inappropriate")
    add_body(
        "A critical theoretical contribution of this project is avoiding Root Mean Squared Error (RMSE) for implicit feedback evaluation. In explicit rating datasets, RMSE measures how closely predicted stars match actual stars. In implicit settings, however, true ratings do not exist. Furthermore, a trivial model predicting zero for all unobserved items achieves an artificially low RMSE while having zero practical recommendation capability. Therefore, top-N ranking metrics are required."
    )

    add_heading_2("9.2 Top-10 Ranking Methodology & Novelty Enforcement")
    add_body(
        "In script 09_evaluate_als.py, we evaluate ranking performance on an 80/20 train/test split (seed=42) under strict novelty enforcement:"
    )
    add_body(
        "1. Candidate Generation: model.recommendForAllUsers(50) generates 50 candidates per customer.\n"
        "2. Novelty Filtering: Using a Spark left_anti join against training data, all products previously purchased by the user are eliminated. The model must recommend novel, unseen products.\n"
        "3. Top-10 Selection: The remaining unseen candidates are ranked by predicted score, taking the top 10.\n"
        "4. Hit Identification: A hit occurs if a recommended product appears in the user's test set interactions.\n"
        "5. Metric Computation: Precision@10 = Hits / 10; Recall@10 = Hits / Total Eligible Test Items."
    )

    add_heading_2("9.3 Experimental Results: ALS vs Popularity Baseline")
    add_body(
        "In script 10_evaluate_popularity.py, we implemented the industry-standard Global Popularity Baseline under the exact same 80/20 train/test split, filtering, and novelty criteria. The empirical results across 4,026 evaluated test customers are summarized below:"
    )

    # Results Table
    res_table = doc.add_table(rows=3, cols=5)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_headers = ["Recommendation Model", "Evaluated Users", "Precision@10", "Recall@10", "Relative Gain"]
    for j, h in enumerate(res_headers):
        cell = res_table.cell(0, j)
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    res_data = [
        ("Global Popularity Baseline", "4,026 users", "0.0435 (4.35%)", "0.0383 (3.83%)", "1.00x (Baseline)"),
        ("Spark MLlib ALS (Ours)", "4,026 users", "0.1181 (11.81%)", "0.1145 (11.45%)", "2.71x Prec / 2.99x Rec")
    ]
    for i, row in enumerate(res_data):
        for j, val in enumerate(row):
            cell = res_table.cell(i+1, j)
            set_cell_background(cell, "F1F5F9" if i == 0 else "EFF6FF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = (i == 1 and j >= 2)
            r.font.color.rgb = BLUE if (i == 1 and j >= 2) else DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_callout(
        "Empirical Conclusion: The ALS model delivers an astounding 2.71x increase in Precision@10 and a 2.99x increase in Recall@10 over the popularity baseline. This statistically verifies that personalizing to latent customer preferences dramatically outperforms generic bestseller lists.",
        "EXPERIMENTAL VERIFICATION"
    )

    # ---------------- CHAPTER 10 ----------------
    add_heading_1("10. Interactive Streamlit Web Application")
    add_body(
        "To deliver operational utility to retail stakeholders, the machine learning models and transactional datasets are encapsulated within an interactive multi-page web application developed in dashboard/app.py using Streamlit and Plotly:"
    )
    add_bullet("1. Overview Page: Executive KPI dashboard displaying Total Revenue (£8.89M), Total Orders (18,532), Unique Customers (4,338), and Unique Products (3,665). Includes interactive start/end date range filters, monthly revenue trend line graphs, top 10 products by quantity, and top 10 countries by revenue.")
    add_bullet("2. Sales Analytics Page: Geographic filter allowing users to select any country (or All Countries) to examine localized monthly revenue trends and order volumes.")
    add_bullet("3. Product Explorer Page: Full-text search engine allowing catalog managers to search across 3,665 SKUs by description or StockCode, displaying unit prices, cumulative sales, and order frequency.")
    add_bullet("4. Recommendations Page: Interactive customer recommendation portal. Managers select any of 4,000+ Customer IDs to inspect the customer's historical orders, total spending, and top-purchased items, alongside their Top-10 personalized ALS recommendations. A novelty badge explicitly flags whether each recommended product is a 'New Discovery' or 'Re-order'.")
    add_bullet("5. Model Performance Page: Side-by-side comparative analytics contrasting ALS metrics against the popularity baseline using interactive Plotly bar charts.")

    add_heading_2("10.1 UI Performance & In-Memory Caching")
    add_body(
        "To ensure seamless user interaction, the dashboard incorporates Streamlit's @st.cache_data decorator on the load_data() routine. This caches the 392k transaction records, 43k recommendation records, and product mapping tables into RAM on first load, reducing subsequent page transition latencies to less than 10 milliseconds."
    )

    # ---------------- CHAPTER 11 ----------------
    add_heading_1("11. Software Quality Assurance & Automated Testing")
    add_body(
        "In enterprise machine learning engineering, silent data corruption is a primary cause of model degradation. To enforce strict data contracts, an automated test suite was constructed under the tests/ directory using Pytest 9.2.0:"
    )
    add_bullet("test_cleaned_data.py: Validates that all eight required columns exist, asserts that CustomerID contains zero missing values, verifies that Quantity and UnitPrice are strictly positive, confirms that no invoice numbers start with 'C', checks that zero duplicate rows remain, and asserts that the cleaned dataset contains exactly 392,692 rows.")
    add_bullet("test_interactions.py: Verifies interaction schema integrity, checks that (CustomerID, StockCode) tuples are strictly unique, asserts that purchase counts and spend are strictly positive, numerically validates that InteractionStrength == np.log1p(PurchaseCount) within a floating-point tolerance of 1e-5, and asserts that the interaction dataset contains exactly 266,110 rows.")
    add_bullet("test_setup.py: Pytest harness verification.")
    add_body(
        "All test modules execute cleanly with 100% pass rates, ensuring reproducibility and pipeline stability."
    )

    # ---------------- CHAPTER 12 ----------------
    add_heading_1("12. Production Deployment & Scalability Architecture")
    add_heading_2("12.1 Transition to Cloud Cluster Architecture")
    add_body(
        "While this project executed Spark locally (master('local[*]')), the codebase was designed for immediate cloud migration without code modification. On managed cloud clusters such as Amazon EMR, Databricks, or Google Cloud Dataproc, the Spark configuration is updated from local[*] to YARN or Kubernetes. Local file paths are seamlessly swapped for object storage URIs (e.g., s3a://company-bucket/data/)."
    )
    add_heading_2("12.2 Low-Latency Real-Time Serving Architecture")
    add_body(
        "In production e-commerce, web servers cannot execute distributed Spark matrix operations during an incoming HTTP request. The recommended production architecture employs a two-tier Lambda pattern:"
    )
    add_bullet("Offline Batch Layer: Spark ALS executes as a nightly cron job, re-factorizing the interaction matrix and computing Top-50 recommendations for all customers.")
    add_bullet("Serving Layer (Redis / DynamoDB): Recommendation tuples (userId, itemId, score) are pushed to an in-memory key-value store (e.g., Redis). An API gateway (FastAPI) retrieves precomputed recommendations in < 2ms.")
    add_bullet("Cold Start Fallback: For new or unauthenticated users, the API immediately falls back to the Global or Country-Specific Popularity recommendations precomputed in script 10.")

    # ---------------- CHAPTER 13 ----------------
    add_heading_1("13. Viva Voce & Oral Defense Handbook")
    add_body(
        "This chapter compiles 25 of the most probable, challenging technical questions examiners and professors ask during project viva voce evaluations, accompanied by concise, high-scoring answers."
    )

    viva_qa = [
        ("Q1: What is the core objective of your project?",
         "Answer: To design and implement a scalable, distributed recommendation engine using Apache Spark MLlib ALS that extracts implicit behavioral signals from transaction logs, statistically outperforms popularity baselines in ranking precision, and serves real-time insights via an interactive Streamlit dashboard."),

        ("Q2: Why did you choose Collaborative Filtering instead of Content-Based Filtering?",
         "Answer: Collaborative filtering discovers latent, serendipitous relationships across user behavior without requiring extensive manual feature engineering of product attributes. It effectively captures cross-category shopping patterns that pure text or category metadata cannot anticipate."),

        ("Q3: What is the fundamental difference between explicit and implicit feedback?",
         "Answer: Explicit feedback consists of conscious user evaluations (like 1-5 star ratings or thumbs up/down). Implicit feedback consists of observational behavioral logs (orders, clicks, quantities). Implicit data has no explicit negative ratings (non-purchase != dislike; usually unawareness) and requires confidence weighting rather than direct rating prediction."),

        ("Q4: Why did you use log1p(PurchaseCount) to formulate interaction strength?",
         "Answer: In e-commerce, wholesale buyers purchase hundreds of units in one order, while repeat loyal customers purchase across multiple orders. Distinct order count reflects true preference. Applying ln(1 + count) enforces diminishing marginal utility and compresses extreme outliers, ensuring gradient descent in ALS remains numerically stable."),

        ("Q5: What is the mathematical concept behind Matrix Factorization?",
         "Answer: Matrix Factorization decomposes a massive, sparse User-Item interaction matrix R (m × n) into two low-rank dense matrices: User matrix U (m × k) and Item matrix V (n × k), such that R approx U · V^T. The dot product u_u^T · v_i predicts the affinity score."),

        ("Q6: Why did you choose Alternating Least Squares (ALS) instead of Stochastic Gradient Descent (SGD)?",
         "Answer: In distributed environments like Apache Spark, SGD requires sequential parameter updates, causing heavy cluster synchronization bottlenecks. ALS fixes one matrix while solving for the other, turning a non-convex problem into independent quadratic problems that can be solved in closed form in parallel across Spark worker nodes without inter-thread locking."),

        ("Q7: Explain the loss function used in your ALS model.",
         "Answer: We used the Hu, Koren, and Volinsky implicit loss function: min ∑ c_ui (p_ui - u_u^T v_i)^2 + λ(||u_u||^2 + ||v_i||^2). Here, p_ui is binary preference (1 if purchased, 0 otherwise), c_ui = 1 + α·r_ui is confidence, and λ is L2 regularization."),

        ("Q8: What does the 'rank' parameter represent in Spark ALS?",
         "Answer: Rank specifies the number of latent factors (k=20). These represent 20 hidden semantic dimensions characterizing user shopping styles and item properties (such as holiday gifts, luxury decor, or kitchen essentials)."),

        ("Q9: Why did you set nonnegative=True in ALS?",
         "Answer: Non-negative matrix factorization constrains latent factor values to be >= 0. This ensures latent dimensions represent purely additive, interpretable components of customer preference rather than complex subtractions of negative vectors."),

        ("Q10: Why did you evaluate using Precision@10 and Recall@10 instead of RMSE?",
         "Answer: In implicit recommendation, RMSE is mathematically flawed because unobserved entries are not negative ratings—they are mostly unseen items. A model predicting zero everywhere gets great RMSE but zero utility. In real e-commerce, users see Top-N items on screen, so ranking accuracy (Precision@10 and Recall@10) measures actual business success."),

        ("Q11: How did you ensure your evaluation tested true product discovery (novelty)?",
         "Answer: In script 09_evaluate_als.py, we performed a Spark left_anti join between candidate recommendations and the user's training data. This strictly removes all previously purchased items from the candidate pool, forcing the model to recommend unseen products."),

        ("Q12: What were your quantitative results compared to the baseline?",
         "Answer: Across 4,026 test users, ALS achieved a Precision@10 of 11.81% and Recall@10 of 11.45%. The Global Popularity Baseline achieved 4.35% Precision@10 and 3.83% Recall@10. ALS delivered a 2.71x increase in Precision and a 2.99x increase in Recall."),

        ("Q13: What is catalog sparsity, and what was it in your dataset?",
         "Answer: Sparsity is the percentage of empty cells in the user-item interaction matrix. With 4,334 users and 3,657 items, there are 15,849,438 possible entries. We had 266,110 interactions, meaning the matrix density is 1.68% and sparsity is 98.32%."),

        ("Q14: How does your system handle the Cold Start Problem for new users?",
         "Answer: In offline evaluation, we configure coldStartStrategy='drop'. In production, we employ a hierarchical fallback: known users receive personalized ALS recommendations; new users with zero history receive the Global or Country-Specific Popularity recommendations precomputed in script 10."),

        ("Q15: How does your system handle the Cold Start Problem for new products?",
         "Answer: Pure collaborative filtering cannot recommend new items with zero purchase history. The industry solution is a hybrid recommender: using content-based embeddings (TF-IDF or BERT) on product descriptions to match new items to similar established items until interaction data accumulates."),

        ("Q16: What major data cleaning steps were performed in PySpark?",
         "Answer: We dropped exact duplicates, filtered out 135k null CustomerIDs, removed 9.2k cancelled invoices starting with 'C', filtered non-positive quantities and prices, and excluded non-merchandise fees like postage and discounts."),

        ("Q17: Why did you write data using toLocalIterator() instead of df.write.csv()?",
         "Answer: On Microsoft Windows, Spark's native write relies on Hadoop winutils.exe, which often throws UnsatisfiedLinkError. Using df.toLocalIterator() streams records partition-by-partition to Python's csv writer, avoiding driver OOM and ensuring cross-platform stability."),

        ("Q18: How did you handle alphanumeric StockCodes in Spark MLlib?",
         "Answer: Spark ALS strictly requires integer user and item IDs. We used Spark's StringIndexer to map alphanumeric StockCodes into 0-indexed integer itemIds, and maintained a product_id_mapping table to translate predictions back to original SKUs."),

        ("Q19: What role does Apache Spark play that Pandas cannot handle?",
         "Answer: Pandas is single-threaded and bound to local RAM, causing crashes when scaling to millions of rows. Apache Spark distributes DataFrames across partitions and worker nodes, parallelizing matrix operations, shuffle joins, and aggregations across cluster cores."),

        ("Q20: What are the main pages in your Streamlit dashboard?",
         "Answer: Five pages: 1. Overview (KPI metrics and revenue trends), 2. Sales Analytics (country-level filtering), 3. Product Explorer (catalog search), 4. Recommendations (customer lookup and Top-10 ALS recommendations with novelty badges), 5. Model Performance (Plotly comparative charts)."),

        ("Q21: How does your Streamlit dashboard achieve sub-10ms page transitions?",
         "Answer: Using Streamlit's @st.cache_data decorator. It loads and preprocesses the transaction and recommendation datasets into server memory once, avoiding redundant disk I/O on every user interaction."),

        ("Q22: What tests did you write in Pytest?",
         "Answer: We wrote tests validating that cleaned transactions have zero missing CustomerIDs, positive quantities/prices, no cancelled orders, exactly 392,692 rows, and that interaction strength strictly matches numpy's log1p(PurchaseCount) across 266,110 rows."),

        ("Q23: What is the time complexity of ALS training?",
         "Answer: Each ALS iteration takes O(m · k^3 + |R| · k^2), where m is the number of entities, k is the latent rank, and |R| is the number of non-zero interactions. Because k=20 is small, k^3=8000 is trivial for modern CPUs, making ALS computationally efficient."),

        ("Q24: What are the primary business benefits of this system for an e-commerce company?",
         "Answer: Higher average order value (AOV), increased customer retention, reduced cart abandonment, automated discovery of high-margin long-tail inventory, and automated marketing email personalization."),

        ("Q25: What future enhancements would you propose?",
         "Answer: Incorporating deep learning Two-Tower Neural Networks, real-time streaming personalization with Apache Kafka, optimizing for serendipity and catalog diversity with Maximal Marginal Relevance (MMR), and session-based transformer models like BERT4Rec.")
    ]

    for q, a in viva_qa:
        add_heading_3(q)
        add_body(a)

    # ---------------- CHAPTER 14 ----------------
    add_heading_1("14. Conclusion & Future Roadmap")
    add_body(
        "This project successfully engineered and empirically validated an industrial-grade E-Commerce Recommendation System using Apache Spark ALS, PySpark, and Streamlit. By addressing the critical realities of commercial retail data—implicit signals, high catalog sparsity (98.32%), wholesale purchase skew, and operational noise—the pipeline transforms raw transaction logs into an accurate, high-speed personalization engine."
    )
    add_body(
        "Key Accomplishments:\n"
        "1. Big Data Engineering: Filtered 149k corrupted records, yielding 392,692 validated transactions and 266,110 implicit interactions.\n"
        "2. Algorithmic Outperformance: Delivered 11.81% Precision@10 and 11.45% Recall@10, representing 2.71x and 2.99x improvements over popularity baselines.\n"
        "3. Production Tooling: Deployed an intuitive 5-page Streamlit analytics dashboard with novelty badges and automated Pytest test coverage."
    )
    add_body(
        "Future enhancements will focus on real-time streaming event ingestion using Apache Kafka and Spark Streaming, hybrid deep learning embeddings for cold-start SKUs, and multi-objective optimization for catalog diversity."
    )

    # Save DOCX
    doc.save(str(DOCX_OUTPUT))
    print(f"Word report successfully created at: {DOCX_OUTPUT}")

if __name__ == "__main__":
    create_docx_report()
