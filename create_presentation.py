import sys
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PATH = Path(r"c:\Users\Jay Uttam\Documents\ecommerce-recommendation\Ecommerce_Recommendation_System_Presentation.pptx")

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # completely blank

    # Color definitions
    NAVY = RGBColor(15, 23, 42)       # #0F172A
    SLATE = RGBColor(30, 41, 59)      # #1E293B
    BLUE = RGBColor(37, 99, 235)      # #2563EB
    CYAN = RGBColor(14, 165, 233)     # #0EA5E9
    GREEN = RGBColor(16, 185, 129)    # #10B981
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    TEXT_DARK = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139)
    ACCENT_RED = RGBColor(239, 68, 68)

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="E-COMMERCE RECOMMENDATION SYSTEM"):
        # Category pill/tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = NAVY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    def add_speaker_note(slide, note_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = note_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY)

    # Decorative glow bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(1.2), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN
    bar.line.fill.background()

    # Title text box
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.3), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Big Data E-Commerce Recommendation System"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "Scalable Collaborative Filtering using Apache Spark ALS & Interactive Analytics Dashboard"
    p2.font.size = Pt(18)
    p2.font.color.rgb = CYAN
    p2.space_before = Pt(12)

    # Info card box
    info_card = add_card(s1, Inches(1.0), Inches(4.7), Inches(11.3), Inches(1.8), bg_color=SLATE, border_color=BLUE)
    tb_info = s1.shapes.add_textbox(Inches(1.3), Inches(4.9), Inches(10.7), Inches(1.4))
    tf_info = tb_info.text_frame
    
    p = tf_info.paragraphs[0]
    p.text = "Project Highlights & Technology Stack:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p_tech = tf_info.add_paragraph()
    p_tech.text = "• Core Technologies: Python 3.13, Apache Spark (PySpark MLlib), Pandas, Streamlit, Plotly, Pytest\n• Algorithm: Implicit Alternating Least Squares (ALS) Matrix Factorization (Hu, Koren, Volinsky formulation)\n• Dataset: UCI Online Retail (541k+ transactions) | Benchmark: 2.71x Precision & 2.99x Recall improvement over baseline"
    p_tech.font.size = Pt(12)
    p_tech.font.color.rgb = RGBColor(203, 213, 225)
    p_tech.space_before = Pt(6)

    add_speaker_note(s1, 
        "Good morning/afternoon respected examiners and professors. Today I am presenting my project: 'Big Data E-Commerce Recommendation System using Apache Spark ALS and Interactive Streamlit Dashboard'. "
        "In modern retail, personalization is critical for conversion and user engagement. In this project, I engineered an end-to-end distributed machine learning pipeline that handles large-scale transaction data, profiles quality anomalies, extracts implicit behavioral signals, trains an Implicit ALS Collaborative Filtering model, rigorously evaluates ranking metrics against a global popularity baseline, and serves live interactive recommendations via a multi-page Streamlit web platform."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Problem Statement & Industry Motivation", "BACKGROUND & CONTEXT")

    # 3 Cards
    c1 = add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0))
    tb1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🛒 Information Overload"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p_sub = tf1.add_paragraph()
    p_sub.text = "\n• Massive Catalogs: Thousands of SKUs make manual browsing impossible for customers.\n\n• Cognitive Fatigue: Decision paralysis leads to abandoned shopping carts and lost sales.\n\n• Business Need: E-commerce platforms require algorithmic matchmaking between consumer preferences and relevant inventory."
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_DARK

    c2 = add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0))
    tb2 = s2.shapes.add_textbox(Inches(5.0), Inches(2.0), Inches(3.2), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🔍 Implicit vs Explicit Data"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p_sub = tf2.add_paragraph()
    p_sub.text = "\n• Scarcity of Ratings: >98% of e-commerce users never leave 1-to-5 star product ratings.\n\n• Real-World Signals: All transaction histories consist of implicit signals (clicks, orders, quantities, spend).\n\n• Algorithmic Challenge: Implicit data lacks explicit negative feedback (non-purchase != dislike; may simply mean unawareness)."
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_DARK

    c3 = add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0))
    tb3 = s2.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.3), Inches(4.6))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "⚡ Scalability & Latency"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p_sub = tf3.add_paragraph()
    p_sub.text = "\n• Big Data Scale: Real retailers process millions of interaction pairs, crashing traditional single-node Scikit-Learn algorithms.\n\n• Solution: Distributed computing with Apache Spark to parallelize matrix operations across cluster nodes.\n\n• Production Serving: Pre-computing and indexing recommendations for sub-millisecond retrieval."
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_DARK

    add_speaker_note(s2,
        "Why do we need this project? In e-commerce, customers face severe catalog overload. Traditional recommendation algorithms like basic SVD or k-NN rely on explicit star ratings, but online retail data is almost 100% implicit: purchases, repeat visits, and quantities. Furthermore, implicit data has no explicit negative signals—if someone hasn't bought an item, it doesn't mean they hate it; they probably haven't seen it. Finally, matrix calculations over hundreds of thousands of transactions quickly overwhelm single-node memory. Apache Spark solves this by distributing computation across partitions."
    )

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & END-TO-END PIPELINE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "System Architecture & End-to-End Pipeline", "ARCHITECTURE")

    # 4 horizontal flow cards
    steps = [
        ("1. Data Ingestion\n& Quality Profiling", "• Raw Excel to CSV conversion\n• 541,909 transactions\n• 8 automated anomaly checks\n• Duplicate & cancellation audits", BLUE),
        ("2. Spark Distributed\nData Cleaning", "• Filter null CustomerIDs (135k)\n• Filter cancelled 'C' invoices\n• Remove negative quantities & prices\n• Result: 392,692 clean records", CYAN),
        ("3. Implicit Feature\nEngineering & ALS", "• Filter non-product fees\n• Aggregate (User, Item) pairs\n• Strength: ln(1 + PurchaseCount)\n• Train Spark MLlib ALS model", GREEN),
        ("4. Evaluation &\nInteractive Dashboard", "• Unseen Top-10 re-ranking\n• Precision@10 & Recall@10\n• 2.71x gain vs Popularity\n• Streamlit + Plotly visual UI", SLATE)
    ]

    card_width = Inches(2.7)
    card_gap = Inches(0.3)
    start_left = Inches(0.8)

    for i, (title, desc, accent) in enumerate(steps):
        x = start_left + i * (card_width + card_gap)
        c = add_card(s3, x, Inches(1.8), card_width, Inches(5.0))
        
        # Color bar top
        t_bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), card_width, Inches(0.12))
        t_bar.fill.solid()
        t_bar.fill.fore_color.rgb = accent
        t_bar.line.fill.background()

        tb = s3.shapes.add_textbox(x + Inches(0.2), Inches(2.1), card_width - Inches(0.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = TEXT_DARK
        p_desc.space_before = Pt(12)

    add_speaker_note(s3,
        "Here is the high-level engineering pipeline. It consists of four distinct phases: "
        "First, Data Ingestion and Quality Profiling, where 541k records are profiled for anomalies. "
        "Second, Distributed Spark Cleaning, which eliminates missing customer keys and cancelled transactions, leaving 392,692 reliable rows. "
        "Third, Feature Engineering and ALS Model Training, where we convert transaction logs into an implicit interaction matrix using a logarithmic formulation and train the matrix factorization model. "
        "Fourth, Evaluation and Dashboard Serving, benchmarking against global popularity and presenting interactive insights via Streamlit."
    )

    # =========================================================================
    # SLIDE 4: DATASET OVERVIEW & QUALITY AUDIT
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Dataset Profiling & Quality Audit", "DATA ENGINEERING")

    # Left Card: Dataset Overview
    c_left = add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_left = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Dataset Characteristics (UCI Online Retail)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_body = tf_l.add_paragraph()
    p_body.text = (
        "• Source: Transnational e-commerce transactions from a UK-based registered gift retailer between 01/12/2010 and 09/12/2011.\n\n"
        "• Raw Record Count: 541,909 transactions\n"
        "• Geographic Reach: 37 countries (majority UK, Germany, France)\n"
        "• Cleaned Total Revenue: £8,887,208.89 (~£8.89 Million)\n"
        "• Distinct Invoices: 18,532 orders | 4,338 unique customers\n"
        "• Catalog Size: 3,665 unique product StockCodes\n\n"
        "• Key Fields: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country."
    )
    p_body.font.size = Pt(12)
    p_body.font.color.rgb = TEXT_DARK
    p_body.space_before = Pt(8)

    # Right Card: Data Quality Audit Table
    c_right = add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_right = s4.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Automated Data Quality Audit Results"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p_table = tf_r.add_paragraph()
    p_table.text = (
        "Anomaly Detected                  Affected Rows    Impact & Treatment\n"
        "─────────────────────────────────────────────────────────────\n"
        "Missing CustomerID                135,080 rows     Guest checkouts -> Filtered\n"
        "Cancelled Invoices ('C')           9,288 rows      Returns/refunds -> Removed\n"
        "Non-Positive Quantities           10,624 rows      Damages/adjustments -> Filtered\n"
        "Non-Positive UnitPrice             2,517 rows      Free samples/debts -> Filtered\n"
        "Duplicate Rows                     5,268 rows      Redundant submissions -> Dropped\n"
        "Operational Fees (Postage/Amazon)      8 types     Non-merchandise -> Excluded\n"
        "─────────────────────────────────────────────────────────────\n"
        "Net Cleaned Records:              392,692 rows     100% Validated Data"
    )
    p_table.font.name = "Consolas"
    p_table.font.size = Pt(11)
    p_table.font.color.rgb = TEXT_DARK
    p_table.space_before = Pt(10)

    add_speaker_note(s4,
        "In script 03_data_quality.py, we performed a thorough data quality audit across seven critical dimensions. "
        "Out of 541,909 raw rows, over 135,000 lacked Customer IDs—representing guest checkouts that cannot be personalized. "
        "We also discovered 9,288 cancellations starting with letter 'C', negative quantities representing inventory adjustments, and zero prices representing company gifts or postage fees. "
        "Cleaning these issues gave us exactly 392,692 reliable purchase events, verified through our Pytest test suite."
    )

    # =========================================================================
    # SLIDE 5: EXPLORATORY DATA ANALYSIS (EDA) INSIGHTS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Exploratory Data Analysis & Business Intelligence", "DATA DISCOVERY")

    # 4 Metric Cards Across Top
    metrics = [
        ("Total Net Revenue", "£8.89 M", GREEN),
        ("Total Invoices", "18,532", BLUE),
        ("Active Customers", "4,338", CYAN),
        ("Unique SKUs", "3,665", SLATE)
    ]
    m_w = Inches(2.7)
    m_gap = Inches(0.3)
    for i, (label, val, color) in enumerate(metrics):
        mx = Inches(0.8) + i * (m_w + m_gap)
        c = add_card(s5, mx, Inches(1.8), m_w, Inches(1.3))
        tb = s5.shapes.add_textbox(mx, Inches(1.9), m_w, Inches(1.1))
        tf = tb.text_frame
        p_val = tf.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(28)
        p_val.font.bold = True
        p_val.font.color.rgb = color
        p_val.alignment = PP_ALIGN.CENTER
        p_lbl = tf.add_paragraph()
        p_lbl.text = label
        p_lbl.font.size = Pt(11)
        p_lbl.font.color.rgb = TEXT_MUTED
        p_lbl.alignment = PP_ALIGN.CENTER

    # Bottom Left: Pareto Distribution & Seasonality
    c_bl = add_card(s5, Inches(0.8), Inches(3.4), Inches(5.7), Inches(3.4))
    tb_bl = s5.shapes.add_textbox(Inches(1.0), Inches(3.6), Inches(5.3), Inches(3.0))
    tf_bl = tb_bl.text_frame
    tf_bl.word_wrap = True
    p = tf_bl.paragraphs[0]
    p.text = "📈 Seasonality & Geographic Concentration"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p_desc = tf_bl.add_paragraph()
    p_desc.text = (
        "• Q4 Holiday Surge: Revenue peaks dramatically in October-November (~£1.1M - £1.4M/mo) due to corporate gift buying and Christmas retail stocking.\n\n"
        "• UK Market Dominance: The United Kingdom accounts for ~89% of gross revenue, followed by the Netherlands, EIRE (Ireland), and Germany.\n\n"
        "• Wholesale Whales: Top 10 customers contribute over 15% of total revenue (Customer 14646 alone accounted for over £280k)."
    )
    p_desc.font.size = Pt(12)
    p_desc.font.color.rgb = TEXT_DARK
    p_desc.space_before = Pt(6)

    # Bottom Right: Catalog Sparsity & Power Law
    c_br = add_card(s5, Inches(6.8), Inches(3.4), Inches(5.7), Inches(3.4))
    tb_br = s5.shapes.add_textbox(Inches(7.0), Inches(3.6), Inches(5.3), Inches(3.0))
    tf_br = tb_br.text_frame
    tf_br.word_wrap = True
    p = tf_br.paragraphs[0]
    p.text = "📊 The Long Tail & Catalog Sparsity"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p_desc = tf_br.add_paragraph()
    p_desc.text = (
        "• Extreme Sparsity: Total possible user-item matrix entries = 4,334 × 3,657 = 15,849,438. Observed interactions = 266,110 (Matrix Density = 1.68%, Sparsity = 98.32%).\n\n"
        "• Long-Tail Distribution: A small fraction of items (e.g., 'White Hanging Heart T-Light Holder', 'Jumbo Bag Red Retrospot') sell tens of thousands of units.\n\n"
        "• Implication: A naive popularity baseline only recommends the top 10 blockbuster items, ignoring the long-tail where true personalization adds value."
    )
    p_desc.font.size = Pt(12)
    p_desc.font.color.rgb = TEXT_DARK
    p_desc.space_before = Pt(6)

    add_speaker_note(s5,
        "From our Exploratory Data Analysis in script 05_eda.py, we uncovered two crucial findings: "
        "First, extreme seasonal demand in Q4 due to holiday stocking. "
        "Second, massive catalog sparsity: the user-item interaction matrix is 98.32% empty! "
        "Furthermore, product demand follows a heavy power-law distribution. Recommending only the top bestselling products fails to personalize to individual tastes, which is exactly why Collaborative Filtering is necessary."
    )

    # =========================================================================
    # SLIDE 6: FEATURE ENGINEERING & IMPLICIT INTERACTION FORMULATION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Feature Engineering: Implicit Interaction Matrix", "FEATURE ENGINEERING")

    c_f1 = add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_f1 = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_f1 = tb_f1.text_frame
    tf_f1.word_wrap = True
    p = tf_f1.paragraphs[0]
    p.text = "Transforming Transaction Logs into Interactions"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_f1 = tf_f1.add_paragraph()
    p_f1.text = (
        "1. Filtering Non-Product Items:\n"
        "   Removed postage, carriage, manual fees, bank charges, and discounts using regular expression filtering.\n\n"
        "2. Multi-Order Aggregation:\n"
        "   Grouped transactions by (CustomerID, StockCode) to calculate:\n"
        "   • PurchaseCount: Distinct invoices containing the item.\n"
        "   • TotalQuantity: Cumulative units purchased.\n"
        "   • TotalSpend: Total monetary investment.\n\n"
        "3. Resulting Interaction Dataset:\n"
        "   • 266,110 distinct customer-product interaction records\n"
        "   • 4,334 active customers and 3,657 product items."
    )
    p_f1.font.size = Pt(12)
    p_f1.font.color.rgb = TEXT_DARK
    p_f1.space_before = Pt(8)

    c_f2 = add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_f2 = s6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_f2 = tb_f2.text_frame
    tf_f2.word_wrap = True
    p = tf_f2.paragraphs[0]
    p.text = "Mathematical Formulation of Interaction Strength"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p_f2 = tf_f2.add_paragraph()
    p_f2.text = (
        "Interaction Strength Equation:\n\n"
        "             r_{u,i} = ln(1 + PurchaseCount_{u,i})\n\n"
        "Why Logarithmic Scaling [log1p]?\n\n"
        "• Diminishing Marginal Utility: A customer buying an item 10 times does not like it 10x more than someone buying it once.\n\n"
        "• Outlier Mitigation: Wholesale bulk buyers who buy 500 units in 20 orders would otherwise skew latent gradient descent.\n\n"
        "• Smooth Confidence Mapping: ln(1 + 1) = 0.693, ln(1 + 2) = 1.098, ln(1 + 10) = 2.397. This compresses extreme values while preserving natural preference rank."
    )
    p_f2.font.size = Pt(12)
    p_f2.font.color.rgb = TEXT_DARK
    p_f2.space_before = Pt(10)

    add_speaker_note(s6,
        "In script 06_create_interactions.py, we transformed raw transaction logs into an implicit interaction matrix. "
        "A critical viva question is: 'Why did you use log1p of PurchaseCount instead of raw quantities?' "
        "The answer is twofold: First, raw quantities are distorted by wholesale buyers who purchase hundreds of items in a single order. "
        "Second, repeated distinct orders represent stronger genuine preference than a single accidental bulk purchase. "
        "Applying ln(1 + PurchaseCount) provides a smooth, bounded confidence rating that stabilizes matrix factorization."
    )

    # =========================================================================
    # SLIDE 7: ALGORITHM DEEP DIVE: IMPLICIT ALS MATRIX FACTORIZATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Algorithm Deep Dive: Collaborative Filtering with ALS", "MACHINE LEARNING")

    c_m1 = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_m1 = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True
    p = tf_m1.paragraphs[0]
    p.text = "Matrix Factorization Concept"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_m1 = tf_m1.add_paragraph()
    p_m1.text = (
        "• Goal: Decompose the massive, sparse User-Item interaction matrix R (m × n) into two dense, low-rank matrices:\n\n"
        "               R ≈ U · V^T\n\n"
        "• User Matrix U (m × k): Latent vector u_i representing customer preference archetypes.\n"
        "• Item Matrix V (n × k): Latent vector v_j representing hidden product characteristics.\n"
        "• Latent Factor Dimension (k = 20): Captures subtle hidden concepts (e.g., vintage kitchenware, holiday gifts, children's toys).\n"
        "• Prediction: Inner product u_i^T · v_j gives the affinity score."
    )
    p_m1.font.size = Pt(12)
    p_m1.font.color.rgb = TEXT_DARK
    p_m1.space_before = Pt(8)

    c_m2 = add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_m2 = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True
    p = tf_m2.paragraphs[0]
    p.text = "Why Alternating Least Squares (ALS)?"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p_m2 = tf_m2.add_paragraph()
    p_m2.text = (
        "• Non-Convex Problem: Simultaneously optimizing U and V is a non-convex optimization problem.\n\n"
        "• The ALS Trick: If we hold Item Matrix V fixed, the loss function becomes strictly quadratic (convex) and solvable in closed form! Then we fix U and solve for V.\n\n"
        "• Alternating Iterations: Repeating this process (10 iterations) guarantees monotonic convergence to a local minimum.\n\n"
        "• Massively Parallelizable: Each user vector u_i can be computed independently of all other users, making it ideal for Apache Spark's distributed architecture."
    )
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = TEXT_DARK
    p_m2.space_before = Pt(8)

    add_speaker_note(s7,
        "Why ALS over Stochastic Gradient Descent (SGD)? "
        "SGD updates parameters sequentially, which creates synchronization bottlenecks in distributed clusters. "
        "ALS, on the other hand, converts a non-convex problem into two alternating linear least squares problems. "
        "When matrix V is fixed, every user's latent vector can be computed independently in parallel across Spark worker nodes without inter-thread locking! "
        "This makes ALS the industry standard for distributed recommendation engines on Apache Spark."
    )

    # =========================================================================
    # SLIDE 8: MATHEMATICAL LOSS FUNCTION & HYPERPARAMETERS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Mathematical Loss Function & Spark Hyperparameters", "MATHEMATICS & CONFIG")

    c_top = add_card(s8, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2))
    tb_top = s8.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(2.0))
    tf_t = tb_top.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "Hu, Koren, Volinsky Implicit Feedback Loss Function"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_eq = tf_t.add_paragraph()
    p_eq.text = (
        "min_{U,V} ∑_{u,i} c_{u,i} ( p_{u,i} - u_u^T v_i )^2  +  λ ( ∑_u ||u_u||^2 + ∑_i ||v_i||^2 )\n\n"
        "Where:\n"
        "• Binary Preference p_{u,i} = 1 if r_{u,i} > 0 (purchased), and 0 if r_{u,i} == 0 (unobserved)\n"
        "• Confidence Weight c_{u,i} = 1 + α · r_{u,i} (Zero interactions have confidence 1; purchases scale up confidence)\n"
        "• Regularization λ: Prevents overfitting on high-frequency purchasers."
    )
    p_eq.font.name = "Consolas"
    p_eq.font.size = Pt(11)
    p_eq.font.color.rgb = TEXT_DARK
    p_eq.space_before = Pt(4)

    # Bottom Table of Hyperparameters
    c_bot = add_card(s8, Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.6))
    tb_bot = s8.shapes.add_textbox(Inches(1.0), Inches(4.3), Inches(11.3), Inches(2.4))
    tf_b = tb_bot.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "Tuned Model Hyperparameters (Spark MLlib ALS)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p_param = tf_b.add_paragraph()
    p_param.text = (
        "Parameter          Value      Technical Justification\n"
        "─────────────────────────────────────────────────────────────────────────────\n"
        "rank               20         Optimal latent dimensionality balancing expressive power vs overfitting.\n"
        "maxIter            10         Empirical convergence reached with minimal residual loss reduction.\n"
        "regParam (λ)       0.1        L2 penalty preventing vector norm explosion on popular items.\n"
        "implicitPrefs      True       Activates implicit feedback formulation (c_{u,i} confidence weighting).\n"
        "alpha (α)          1.0        Rate of confidence increase per purchase interaction.\n"
        "nonnegative        True       Constrains factors to ≥ 0 (produces interpretable additive part-based features).\n"
        "coldStartStrategy  'drop'     Drops test users/items not seen during training to avoid evaluation NaNs."
    )
    p_param.font.name = "Consolas"
    p_param.font.size = Pt(11)
    p_param.font.color.rgb = TEXT_DARK
    p_param.space_before = Pt(6)

    add_speaker_note(s8,
        "Let's focus on the mathematics. This is the Hu, Koren, and Volinsky implicit feedback formulation. "
        "Notice two variables: p_ui, which is binary (1 if purchased, 0 otherwise), and c_ui, which is the confidence weight equal to 1 + alpha * r_ui. "
        "If a customer hasn't interacted with an item, p_ui is 0, but confidence is 1. If they bought it multiple times, confidence increases. "
        "We set nonnegative=True because it forces latent representations to be additive, meaning latent factors represent pure additive customer taste categories rather than canceling out negative numbers."
    )

    # =========================================================================
    # SLIDE 9: EVALUATION METHODOLOGY: RANKING VS RATING METRICS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Evaluation Methodology: Ranking vs Rating Metrics", "VALIDATION")

    c_ev1 = add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_ev1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_ev1 = tb_ev1.text_frame
    tf_ev1.word_wrap = True
    p = tf_ev1.paragraphs[0]
    p.text = "Why RMSE Fails on Implicit Data"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p_ev1 = tf_ev1.add_paragraph()
    p_ev1.text = (
        "• Common Student Mistake: Evaluating implicit models using Root Mean Squared Error (RMSE).\n\n"
        "• Flaw 1: Implicit feedback does not have true ratings. Predicting whether an interaction strength is 0.69 or 1.10 does not reflect recommendation quality.\n\n"
        "• Flaw 2: An algorithm predicting 0 for all unobserved items achieves an artificially great RMSE, but is useless as a recommender.\n\n"
        "• True Business Goal: In real life, users only see the Top-N items on screen. What matters is Ranking Accuracy: did the customer actually buy the recommended items?"
    )
    p_ev1.font.size = Pt(12)
    p_ev1.font.color.rgb = TEXT_DARK
    p_ev1.space_before = Pt(8)

    c_ev2 = add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_ev2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_ev2 = tb_ev2.text_frame
    tf_ev2.word_wrap = True
    p = tf_ev2.paragraphs[0]
    p.text = "Rigorous Top-10 Ranking Pipeline"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN

    p_ev2 = tf_ev2.add_paragraph()
    p_ev2.text = (
        "1. Train/Test Split: 80% train / 20% test split (seed=42).\n\n"
        "2. Candidate Generation: model.recommendForAllUsers(50) generates 50 candidates per user.\n\n"
        "3. Novelty Filtering (left_anti join): Products the customer already purchased in the training set are strictly removed. The model must recommend UNSEEN products!\n\n"
        "4. Top-10 Re-ranking: Re-indexed by rank 1..10.\n\n"
        "5. Metrics Calculated:\n"
        "   • Precision@10 = Hits in Test / 10\n"
        "   • Recall@10 = Hits in Test / Total Eligible Test Items"
    )
    p_ev2.font.size = Pt(12)
    p_ev2.font.color.rgb = TEXT_DARK
    p_ev2.space_before = Pt(8)

    add_speaker_note(s9,
        "This slide answers one of the most critical viva questions: 'Why did you evaluate using Precision@10 and Recall@10 instead of RMSE?' "
        "In implicit recommendation, RMSE is mathematically meaningless because unobserved items are not negative ratings—they are mostly unseen items. "
        "More importantly, we enforce strict Novelty: in script 09_evaluate_als.py, we perform a left_anti join to filter out items the customer already purchased in the training set. "
        "This tests true discovery: can the model predict future purchases of new items?"
    )

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL RESULTS: ALS VS POPULARITY BASELINE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "Experimental Results: ALS vs Popularity Baseline", "RESULTS & BENCHMARK")

    # 2 Comparison Cards Left & Right
    c_als = add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(3.4), border_color=BLUE)
    tb_a = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(3.0))
    tf_a = tb_a.text_frame
    p = tf_a.paragraphs[0]
    p.text = "🎯 ALS Collaborative Filtering"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p_a = tf_a.add_paragraph()
    p_a.text = (
        "\n• Precision@10:  0.1181  (11.81%)\n"
        "• Recall@10:     0.1145  (11.45%)\n"
        "• Evaluated Users: 4,026 active customers\n"
        "• Personalization: High (tailored to individual taste archetypes across 20 latent factors)"
    )
    p_a.font.size = Pt(14)
    p_a.font.color.rgb = TEXT_DARK

    c_pop = add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(3.4), border_color=TEXT_MUTED)
    tb_p = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(3.0))
    tf_p = tb_p.text_frame
    p = tf_p.paragraphs[0]
    p.text = "📦 Global Popularity Baseline"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p_p = tf_p.add_paragraph()
    p_p.text = (
        "\n• Precision@10:  0.0435  (4.35%)\n"
        "• Recall@10:     0.0383  (3.83%)\n"
        "• Evaluated Users: 4,026 active customers\n"
        "• Personalization: Zero (recommends the exact same top sellers to all users after filtering prior buys)"
    )
    p_p.font.size = Pt(14)
    p_p.font.color.rgb = TEXT_DARK

    # Bottom Improvement Callout Card
    c_gain = add_card(s10, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.5), bg_color=SLATE, border_color=GREEN)
    tb_g = s10.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.3))
    tf_g = tb_g.text_frame
    p_g = tf_g.paragraphs[0]
    p_g.text = "🚀 Quantifiable Algorithmic Improvement Over Baseline:"
    p_g.font.size = Pt(15)
    p_g.font.bold = True
    p_g.font.color.rgb = WHITE
    p_stat = tf_g.add_paragraph()
    p_stat.text = (
        "• Precision Improvement: 2.71x Multiplier (from 4.35% -> 11.81%, an increase of +171.5%)\n"
        "• Recall Improvement:    2.99x Multiplier (from 3.83% -> 11.45%, an increase of +198.9%)\n"
        "Conclusion: Personalized matrix factorization statistically crushes naive popularity in discovery and relevance."
    )
    p_stat.font.size = Pt(12)
    p_stat.font.color.rgb = RGBColor(167, 243, 208)
    p_stat.space_before = Pt(4)

    add_speaker_note(s10,
        "Here are the definitive quantitative results. "
        "A common viva question is: 'How do you know ALS is actually good? What is your baseline?' "
        "We implemented script 10_evaluate_popularity.py to evaluate a global popularity baseline under the exact same 80/20 train/test split. "
        "Popularity achieves 4.35% Precision@10 and 3.83% Recall@10. "
        "Our ALS model achieves 11.81% Precision@10 and 11.45% Recall@10. "
        "That is an extraordinary 2.71 times higher precision and nearly 3 times higher recall!"
    )

    # =========================================================================
    # SLIDE 11: INTERACTIVE STREAMLIT DASHBOARD ARCHITECTURE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_header(s11, "Interactive Analytics Dashboard Architecture", "USER INTERFACE")

    c_d1 = add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_d1 = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_d1 = tb_d1.text_frame
    tf_d1.word_wrap = True
    p = tf_d1.paragraphs[0]
    p.text = "Dashboard Design & 5 Functional Modules"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_d1 = tf_d1.add_paragraph()
    p_d1.text = (
        "1. Executive Overview:\n"
        "   KPI scorecards (Revenue, Orders, Customers, SKUs), interactive date-range filter, and monthly revenue trends.\n\n"
        "2. Sales Analytics:\n"
        "   Country-level revenue breakdown and monthly order volume distributions.\n\n"
        "3. Product Explorer:\n"
        "   Full catalog search engine with revenue and unit sales.\n\n"
        "4. Personalized Recommendations:\n"
        "   Customer selector (4,000+ IDs), purchase history inspection, and Top-10 ALS recommendations with novelty badges.\n\n"
        "5. Model Performance:\n"
        "   Visual comparison of ALS vs Popularity with interactive Plotly bar charts."
    )
    p_d1.font.size = Pt(11)
    p_d1.font.color.rgb = TEXT_DARK
    p_d1.space_before = Pt(6)

    c_d2 = add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_d2 = s11.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_d2 = tb_d2.text_frame
    tf_d2.word_wrap = True
    p = tf_d2.paragraphs[0]
    p.text = "Technical Engineering & UI Optimization"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p_d2 = tf_d2.add_paragraph()
    p_d2.text = (
        "• In-Memory Caching (@st.cache_data):\n"
        "   Caches preprocessed transactions, ALS recommendations, and product mapping tables to ensure instantaneous page transitions.\n\n"
        "• High-Performance Data Join:\n"
        "   Recommendation IDs are mapped back to human-readable product descriptions in sub-5ms.\n\n"
        "• Responsive Plotly Charts:\n"
        "   Custom tooltip formatting, dynamic re-sorting, and interactive zoom/pan capabilities.\n\n"
        "• Business Transparency:\n"
        "   Every recommendation explicitly flags whether the customer has previously purchased the item or if it is a brand-new discovery."
    )
    p_d2.font.size = Pt(11)
    p_d2.font.color.rgb = TEXT_DARK
    p_d2.space_before = Pt(6)

    add_speaker_note(s11,
        "To bridge the gap between machine learning engineering and business stakeholders, we developed an enterprise-grade web application using Streamlit and Plotly. "
        "It features five distinct modules: Overview, Sales Analytics, Product Explorer, Personalized Recommendations, and Model Performance. "
        "We used st.cache_data to load the datasets into memory once, ensuring instantaneous rendering for over 4,300 customers without lag."
    )

    # =========================================================================
    # SLIDE 12: PERSONALIZED RECOMMENDATION WORKFLOW (PAGE 4)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, LIGHT_BG)
    add_header(s12, "Deep Dive: Recommendation Workflow & Customer View", "USER EXPERIENCE")

    # Step by step UI flow
    steps_ui = [
        ("Step 1: Select Customer ID", "Manager selects any customer (e.g., Customer 17850) from the interactive dropdown.", BLUE),
        ("Step 2: Profile Purchase History", "System aggregates past orders: Total Spend, Total Orders, and Top 10 most purchased items.", CYAN),
        ("Step 3: Retrieve ALS Top 10", "System looks up the user's pre-computed latent dot products and ranks top 10 items.", GREEN),
        ("Step 4: Novelty Verification", "Labels each product with 'Previously Purchased: Yes/No' to guarantee catalog discovery.", SLATE)
    ]

    for i, (title, desc, accent) in enumerate(steps_ui):
        y = Inches(1.8) + i * Inches(1.25)
        c = add_card(s12, Inches(0.8), y, Inches(11.7), Inches(1.1))
        # left accent bar
        bar = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.15), Inches(1.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb = s12.shapes.add_textbox(Inches(1.2), y + Inches(0.1), Inches(11.1), Inches(0.9))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = TEXT_DARK
        p_desc.space_before = Pt(2)

    add_speaker_note(s12,
        "Here is what happens on the Recommendations page: When a store manager or customer selects an ID, the dashboard first computes their historical baseline—what they previously bought, their average order value, and their top categories. "
        "Then it surfaces their top 10 ALS recommendations with their predicted scores. "
        "Notice the novelty verification metric: it splits recommendations into 'New Product Discoveries' versus 'Re-order Reminders', providing complete algorithmic transparency."
    )

    # =========================================================================
    # SLIDE 13: SOFTWARE TESTING & QUALITY ASSURANCE
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, LIGHT_BG)
    add_header(s13, "Automated Testing & Pipeline Verification", "QUALITY ASSURANCE")

    c_t1 = add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_t1 = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]
    p.text = "Automated Pytest Test Suite"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_t1 = tf_t1.add_paragraph()
    p_t1.text = (
        "• Testing Framework: pytest 9.2.0\n\n"
        "• Data Contract Validation:\n"
        "  Every pipeline output is covered by deterministic assertion tests to prevent silent data corruption.\n\n"
        "• Execution: Tests run automatically in CI/CD or local test harnesses before model training is initiated.\n\n"
        "• Status: 100% of pipeline tests pass with 0 warnings or failures."
    )
    p_t1.font.size = Pt(12)
    p_t1.font.color.rgb = TEXT_DARK
    p_t1.space_before = Pt(8)

    c_t2 = add_card(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_t2 = s13.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_t2 = tb_t2.text_frame
    tf_t2.word_wrap = True
    p = tf_t2.paragraphs[0]
    p.text = "Key Test Assertions & Invariants"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN

    p_t2 = tf_t2.add_paragraph()
    p_t2.text = (
        "1. test_cleaned_data.py:\n"
        "   ✓ All 8 mandatory schema columns exist\n"
        "   ✓ Zero null CustomerIDs allowed\n"
        "   ✓ All Quantities and UnitPrices are strictly > 0\n"
        "   ✓ No cancelled invoice numbers ('C') remain\n"
        "   ✓ No duplicate rows exist\n"
        "   ✓ Exactly 392,692 cleaned records asserted\n\n"
        "2. test_interactions.py:\n"
        "   ✓ Zero null User or Product IDs\n"
        "   ✓ Interaction pairs are strictly unique\n"
        "   ✓ Math check: InteractionStrength == np.log1p(PurchaseCount) within 1e-5 tolerance\n"
        "   ✓ Exactly 266,110 interaction records asserted"
    )
    p_t2.font.name = "Consolas"
    p_t2.font.size = Pt(11)
    p_t2.font.color.rgb = TEXT_DARK
    p_t2.space_before = Pt(6)

    add_speaker_note(s13,
        "Software quality assurance is critical in data engineering. "
        "We built an automated test suite under tests/ using Pytest. "
        "It validates that our cleaned dataset adheres strictly to invariants: zero nulls, strictly positive quantities, no cancelled orders, and exactly 392,692 rows. "
        "It also mathematically verifies that our InteractionStrength matches numpy's log1p to within 10^-5 precision across all 266,110 interaction pairs."
    )

    # =========================================================================
    # SLIDE 14: ENGINEERING CHALLENGES & WINDOWS COMPATIBILITY
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, LIGHT_BG)
    add_header(s14, "Key Engineering Challenges & Solutions", "CHALLENGES SOLVED")

    challenges = [
        ("Challenge 1: Windows Hadoop Winutils Dependency",
         "Problem: Spark's native .write.csv() relies on native Hadoop Windows binaries (winutils.exe), which throw UnsatisfiedLinkError on Windows.\n"
         "Solution: Engineered a streaming export pipeline using Python's native csv.writer and Spark's df.toLocalIterator(). This streams rows sequentially from Spark partitions without loading the entire dataset into driver memory, achieving robust platform independence.", BLUE),
        
        ("Challenge 2: Alphanumeric StockCodes in PySpark MLlib",
         "Problem: Spark MLlib ALS requires integer user and item IDs, but retail StockCodes are alphanumeric strings (e.g., '85123A', 'POST').\n"
         "Solution: Implemented Spark's StringIndexer to generate a contiguous 0-indexed itemId mapping, trained the model, and created a bidirectional lookup table (product_id_mapping.csv) to restore original SKUs for serving.", CYAN),

        ("Challenge 3: Driver Memory Pressures During Candidate Cross-Joins",
         "Problem: Generating candidate recommendations for thousands of users can cause Out-Of-Memory (OOM) errors during Cartesian cross-joins.\n"
         "Solution: Leveraged Spark's native model.recommendForAllUsers(50), filtered prior items using left_anti join on partitioned data, and applied Window ranking functions partitioned by userId.", GREEN)
    ]

    for i, (title, desc, accent) in enumerate(challenges):
        y = Inches(1.8) + i * Inches(1.65)
        c = add_card(s14, Inches(0.8), y, Inches(11.7), Inches(1.5))
        # left accent bar
        bar = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.15), Inches(1.5))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb = s14.shapes.add_textbox(Inches(1.2), y + Inches(0.1), Inches(11.1), Inches(1.3))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_DARK
        p_desc.space_before = Pt(2)

    add_speaker_note(s14,
        "Examiners frequently ask: 'What technical challenges did you face and how did you resolve them?' "
        "We solved three major engineering hurdles: "
        "First, on Windows, PySpark's default file writer crashes due to missing Hadoop native winutils.exe. Rather than relying on brittle third-party binaries, we wrote an incremental streamer using df.toLocalIterator(), keeping memory usage low. "
        "Second, retail StockCodes are alphanumeric, but ALS requires integers. We used PySpark's StringIndexer and created a two-way mapping table. "
        "Third, we eliminated OOM risks during recommendation generation by using Spark's built-in recommendForAllUsers and Window functions."
    )

    # =========================================================================
    # SLIDE 15: COLD START PROBLEM & MITIGATION STRATEGY
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, LIGHT_BG)
    add_header(s15, "The Cold Start Problem & Industry Mitigations", "SYSTEM DESIGN")

    c_cs1 = add_card(s15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_cs1 = s15.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_cs1 = tb_cs1.text_frame
    tf_cs1.word_wrap = True
    p = tf_cs1.paragraphs[0]
    p.text = "Understanding Cold Start"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p_cs1 = tf_cs1.add_paragraph()
    p_cs1.text = (
        "• New User Problem:\n"
        "  When a customer signs up, they have zero interaction history (r_{u,i} = 0). The model has no latent vector u_u for them.\n\n"
        "• New Item Problem:\n"
        "  When a newly launched SKU enters the catalog, it has no purchase history. It will never be recommended by pure collaborative filtering.\n\n"
        "• Spark's Cold Start Strategy ('drop'):\n"
        "  In Spark MLlib, coldStartStrategy='drop' ensures unobserved test entities are dropped from metric calculation to prevent NaN distortion during offline evaluation."
    )
    p_cs1.font.size = Pt(12)
    p_cs1.font.color.rgb = TEXT_DARK
    p_cs1.space_before = Pt(8)

    c_cs2 = add_card(s15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_cs2 = s15.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_cs2 = tb_cs2.text_frame
    tf_cs2.word_wrap = True
    p = tf_cs2.paragraphs[0]
    p.text = "Production Mitigation Architecture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN

    p_cs2 = tf_cs2.add_paragraph()
    p_cs2.text = (
        "1. Hierarchical Fallback Strategy:\n"
        "   • If User is Known -> Serve Personalized ALS Model (11.8% precision).\n"
        "   • If User is Unknown -> Fallback to Popularity Baseline (4.35% precision) or Country-Specific Best Sellers.\n\n"
        "2. Content-Based Hybrid Augmentation:\n"
        "   • Extract TF-IDF or BERT embeddings from product Descriptions.\n"
        "   • Recommend items semantically similar to viewed products even with zero sales.\n\n"
        "3. Session-Based Onboarding:\n"
        "   • Capture the first 2-3 clicks in a session to instantly assign a provisional user vector."
    )
    p_cs2.font.size = Pt(12)
    p_cs2.font.color.rgb = TEXT_DARK
    p_cs2.space_before = Pt(8)

    add_speaker_note(s15,
        "Every recommender system viva asks: 'How does your model handle cold start?' "
        "Be ready with this 3-tier answer: "
        "First, offline: Spark ALS sets coldStartStrategy='drop' so evaluation metrics don't fail due to NaNs. "
        "Second, online: For new users, we use a hierarchical fallback—falling back to the Global or Country-wise Popularity baseline that we proved in script 10. "
        "Third, future hybrid expansion: For new items with zero purchases, we utilize content-based embeddings on product descriptions."
    )

    # =========================================================================
    # SLIDE 16: CLOUD & DISTRIBUTED PRODUCTION DEPLOYMENT
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, LIGHT_BG)
    add_header(s16, "Production Deployment & Cluster Scalability", "DEPLOYMENT")

    c_p1 = add_card(s16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_p1 = s16.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    p = tf_p1.paragraphs[0]
    p.text = "From Local to Distributed Cluster"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_p1 = tf_p1.add_paragraph()
    p_p1.text = (
        "• Local Development: Master local[*] spawns worker threads matching local CPU cores.\n\n"
        "• Cloud Cluster Migration:\n"
        "  Deployable on AWS EMR (Elastic MapReduce) or Databricks with zero code changes—only changing master to spark:// or yarn.\n\n"
        "• Distributed Storage:\n"
        "  Replace local CSV paths with S3 (s3a://) or Azure Data Lake (abfss://).\n\n"
        "• Data Lakehouse Format:\n"
        "  Transition CSV storage to Delta Lake / Apache Parquet for column pruning, compression, and ACID transactions."
    )
    p_p1.font.size = Pt(12)
    p_p1.font.color.rgb = TEXT_DARK
    p_p1.space_before = Pt(8)

    c_p2 = add_card(s16, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb_p2 = s16.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    p = tf_p2.paragraphs[0]
    p.text = "Real-Time Serving Architecture"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p_p2 = tf_p2.add_paragraph()
    p_p2.text = (
        "• Two-Tier Architecture:\n\n"
        "  1. Batch Layer (Apache Spark):\n"
        "     Runs nightly or hourly on a scheduled job to re-train ALS factor matrices and precompute Top-N recommendations.\n\n"
        "  2. Speed / Serving Layer (Redis / Cassandra):\n"
        "     Precomputed recommendations are exported to a high-speed in-memory key-value store (e.g., Redis). Lookup: GET user:17850:recs -> < 2ms latency.\n\n"
        "  3. API Gateway:\n"
        "     FastAPI microservice exposing /recommendations/{user_id} for frontend web and mobile apps."
    )
    p_p2.font.size = Pt(12)
    p_p2.font.color.rgb = TEXT_DARK
    p_p2.space_before = Pt(8)

    add_speaker_note(s16,
        "Examiners love to ask: 'How would you scale this to 100 million transactions in production?' "
        "Explain that PySpark is inherently cluster-ready. By switching the Spark master configuration from local[*] to YARN or Kubernetes on AWS EMR, the exact same scripts scale horizontally across hundreds of worker nodes. "
        "For serving, you don't calculate matrix multiplications live per HTTP request—you batch-compute recommendations in Spark, dump them into Redis or DynamoDB, and serve them with sub-millisecond response times."
    )

    # =========================================================================
    # SLIDE 17: FUTURE WORK & RESEARCH EXTENSIONS
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17, LIGHT_BG)
    add_header(s17, "Future Work & Advanced Roadmap", "INNOVATION")

    extensions = [
        ("1. Neural Hybrid Recommenders (Deep Learning)",
         "Incorporate Deep Learning models like Two-Tower Neural Networks, Neural Collaborative Filtering (NCF), or transformers (BERT4Rec) to fuse textual item descriptions, image embeddings, and collaborative signals.", BLUE),
        
        ("2. Real-Time Streaming Personalization with Kafka",
         "Implement Spark Structured Streaming + Apache Kafka to ingest clickstream events in real time, updating dynamic user affinity vectors instantly within the active user session.", CYAN),

        ("3. Beyond-Accuracy Objectives (Diversity & Serendipity)",
         "Optimize for catalog coverage, serendipity, and fairness rather than pure precision. Implement Maximal Marginal Relevance (MMR) re-ranking to ensure customers aren't recommended 10 identical items.", GREEN),

        ("4. Contextual & Temporal Awareness",
         "Incorporate time-of-day, day-of-week, seasonal holidays, and device context (mobile vs desktop) into the feature space using Factorization Machines.", SLATE)
    ]

    for i, (title, desc, accent) in enumerate(extensions):
        y = Inches(1.8) + i * Inches(1.25)
        c = add_card(s17, Inches(0.8), y, Inches(11.7), Inches(1.1))
        bar = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.15), Inches(1.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb = s17.shapes.add_textbox(Inches(1.2), y + Inches(0.1), Inches(11.1), Inches(0.9))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_DARK
        p_desc.space_before = Pt(2)

    add_speaker_note(s17,
        "For future enhancements, we have identified four impactful directions: "
        "First, Deep Learning Two-Tower models combining text/image embeddings with matrix factorization. "
        "Second, real-time streaming with Apache Kafka and Spark Streaming. "
        "Third, optimizing for serendipity and catalog diversity using Maximal Marginal Relevance to prevent recommendation monotony. "
        "Fourth, contextual bandit optimization."
    )

    # =========================================================================
    # SLIDE 18: SUMMARY, CONCLUSION & VIVA DEFENSE
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18, NAVY)

    # Decorative glow bar
    bar = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.5), Inches(1.2), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN
    bar.line.fill.background()

    tb = s18.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Summary of Key Contributions"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE

    # Card with bullet points
    c_fin = add_card(s18, Inches(1.0), Inches(3.2), Inches(11.3), Inches(3.4), bg_color=SLATE, border_color=BLUE)
    tb_fin = s18.shapes.add_textbox(Inches(1.3), Inches(3.4), Inches(10.7), Inches(3.0))
    tf_f = tb_fin.text_frame
    tf_f.word_wrap = True

    points = [
        "✓ Big Data Pipeline: Engineered robust ingestion, quality profiling, and distributed cleaning across 541k+ transactions.",
        "✓ Implicit Formulation: Transformed multi-order purchase histories into mathematically grounded implicit interaction strengths.",
        "✓ High-Performance ALS: Trained PySpark MLlib ALS model (rank=20, nonnegative=True) to factorize sparse user-item matrix.",
        "✓ Proven Outperformance: Statistically validated 2.71x Precision and 2.99x Recall improvement over popularity baseline.",
        "✓ Enterprise Dashboard: Built a 5-page responsive Streamlit & Plotly platform for real-time recommendation serving.",
        "✓ Software Reliability: 100% test coverage of critical data invariants using automated Pytest assertions."
    ]

    for i, pt_txt in enumerate(points):
        p = tf_f.paragraphs[0] if i == 0 else tf_f.add_paragraph()
        p.text = pt_txt
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(8)

    add_speaker_note(s18,
        "In conclusion, this project delivers a complete, production-grade recommendation and analytics system. "
        "We successfully proved that personalized collaborative filtering delivers nearly triple the accuracy of standard retail popularity baselines, while maintaining high scalability through Apache Spark. "
        "Thank you for your time and attention. I am now eager and ready to answer any questions!"
    )

    # Save presentation
    prs.save(str(OUTPUT_PATH))
    print(f"Presentation successfully created at: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_presentation()
