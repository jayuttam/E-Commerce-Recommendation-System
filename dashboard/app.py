
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Recommendation System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

CLEANED_DATA_PATH = PROCESSED_DIR / "cleaned_retail.csv"

RECOMMENDATIONS_PATH = (
    PROCESSED_DIR / "top_10_recommendations.csv"
)

MAPPING_PATH = (
    PROCESSED_DIR / "product_id_mapping.csv"
)


# ============================================================
# 3. LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    # Load cleaned retail transactions
    transactions = pd.read_csv(
        CLEANED_DATA_PATH,
        low_memory=False
    )

    # Convert data types
    transactions["CustomerID"] = pd.to_numeric(
        transactions["CustomerID"],
        errors="coerce"
    )

    transactions["Quantity"] = pd.to_numeric(
        transactions["Quantity"],
        errors="coerce"
    )

    transactions["UnitPrice"] = pd.to_numeric(
        transactions["UnitPrice"],
        errors="coerce"
    )

    transactions["InvoiceDate"] = pd.to_datetime(
        transactions["InvoiceDate"],
        dayfirst=True,
        errors="coerce"
    )

    # Calculate revenue
    transactions["Revenue"] = (
        transactions["Quantity"] *
        transactions["UnitPrice"]
    )

    # Load ALS recommendations
    recommendations = pd.read_csv(
        RECOMMENDATIONS_PATH
    )

    # Load product ID mapping
    mapping = pd.read_csv(
        MAPPING_PATH
    )

    return transactions, recommendations, mapping


try:

    transactions, recommendations, mapping = load_data()

except Exception as e:

    st.error(f"Unable to load project data: {e}")

    st.info(
        "Make sure these files exist inside data/processed:\n"
        "- cleaned_retail.csv\n"
        "- top_10_recommendations.csv\n"
        "- product_id_mapping.csv"
    )

    st.stop()


# ============================================================
# 4. DATA PREPROCESSING
# ============================================================

transactions = transactions.dropna(
    subset=["CustomerID", "InvoiceDate"]
).copy()

transactions["CustomerID"] = (
    transactions["CustomerID"].astype(int)
)

transactions["Country"] = (
    transactions["Country"].fillna("Unknown")
)

transactions["Description"] = (
    transactions["Description"].fillna("Unknown Product")
)

transactions["StockCode"] = (
    transactions["StockCode"].astype(str).str.strip()
)

transactions["InvoiceNo"] = (
    transactions["InvoiceNo"].astype(str)
)

# Prepare recommendation data
recommendations["userId"] = pd.to_numeric(
    recommendations["userId"],
    errors="coerce"
)

recommendations["itemId"] = pd.to_numeric(
    recommendations["itemId"],
    errors="coerce"
)

recommendations = recommendations.dropna(
    subset=["userId", "itemId"]
).copy()

recommendations["userId"] = (
    recommendations["userId"].astype(int)
)

recommendations["itemId"] = (
    recommendations["itemId"].astype(int)
)

if "StockCode" in recommendations.columns:

    recommendations["StockCode"] = (
        recommendations["StockCode"].astype(str).str.strip()
    )

else:

    # Recover StockCode through the item mapping
    recommendations = recommendations.merge(
        mapping[["itemId", "StockCode"]],
        on="itemId",
        how="left"
    )

if "predictedScore" in recommendations.columns:

    recommendations["predictedScore"] = pd.to_numeric(
        recommendations["predictedScore"],
        errors="coerce"
    )

else:

    recommendations["predictedScore"] = 0.0

if "rank" not in recommendations.columns:

    recommendations["rank"] = (
        recommendations
        .groupby("userId")["predictedScore"]
        .rank(method="first", ascending=False)
    )

recommendations["rank"] = pd.to_numeric(
    recommendations["rank"],
    errors="coerce"
)

recommendations = recommendations.dropna(
    subset=["rank"]
).copy()


# ============================================================
# 5. PRODUCT CATALOG
# ============================================================

products = (
    transactions
    .groupby("StockCode")
    .agg(
        Description=("Description", "first"),
        TotalQuantity=("Quantity", "sum"),
        TotalRevenue=("Revenue", "sum"),
        TotalOrders=("InvoiceNo", "nunique")
    )
    .reset_index()
)

# Remove duplicate StockCodes if any
products = products.drop_duplicates(
    subset=["StockCode"]
)

# Product lookup
product_lookup = products.set_index("StockCode")


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🛍️ E-Commerce Analytics")

st.sidebar.markdown(
    """
    Explore business analytics and discover
    personalized product recommendations.
    """
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Sales Analytics",
        "Product Explorer",
        "Recommendations",
        "Model Performance"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    **Technology Stack**

    - Python
    - Apache Spark
    - PySpark
    - Spark MLlib
    - Pandas
    - Streamlit
    - Plotly
    """
)


# ============================================================
# 7. COMMON HEADER
# ============================================================

st.title("🛍️ E-Commerce Recommendation System")

st.caption(
    "An interactive analytics and personalized product "
    "recommendation platform powered by Apache Spark ALS."
)

st.divider()


# ============================================================
# 8. OVERVIEW PAGE
# ============================================================

if page == "Overview":

    st.header("Business Overview")

    # Date filters
    min_date = transactions["InvoiceDate"].min().date()

    max_date = transactions["InvoiceDate"].max().date()

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

    with col2:

        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    if start_date > end_date:

        st.error(
            "Start date cannot be after end date."
        )

        st.stop()

    filtered = transactions[
        (transactions["InvoiceDate"].dt.date >= start_date) &
        (transactions["InvoiceDate"].dt.date <= end_date)
    ]

    if filtered.empty:

        st.warning(
            "No transactions found for the selected date range."
        )

        st.stop()

    # KPI calculations
    total_revenue = filtered["Revenue"].sum()

    total_orders = filtered["InvoiceNo"].nunique()

    total_customers = filtered["CustomerID"].nunique()

    total_products = filtered["StockCode"].nunique()

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Revenue",
        f"{total_revenue:,.2f}"
    )

    c2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    c3.metric(
        "Unique Customers",
        f"{total_customers:,}"
    )

    c4.metric(
        "Unique Products",
        f"{total_products:,}"
    )

    st.divider()

    # Monthly revenue
    st.subheader("Monthly Revenue")

    monthly = (
        filtered
        .assign(
            Month=filtered["InvoiceDate"].dt.to_period("M").astype(str)
        )
        .groupby("Month")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Top products and countries
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top 10 Products")

        top_products = (
            filtered
            .groupby("Description")["Quantity"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

        fig = px.bar(
            top_products,
            x="Quantity",
            y="Description",
            orientation="h",
            title="Top Products by Quantity"
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Revenue by Country")

        country_sales = (
            filtered
            .groupby("Country")["Revenue"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

        fig = px.bar(
            country_sales,
            x="Country",
            y="Revenue",
            title="Top 10 Countries by Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# 9. SALES ANALYTICS PAGE
# ============================================================

elif page == "Sales Analytics":

    st.header("Sales Analytics")

    country_list = sorted(
        transactions["Country"].dropna().unique().tolist()
    )

    selected_country = st.selectbox(
        "Select Country",
        ["All Countries"] + country_list
    )

    sales_data = transactions.copy()

    if selected_country != "All Countries":

        sales_data = sales_data[
            sales_data["Country"] == selected_country
        ]

    if sales_data.empty:

        st.warning("No sales data available.")

        st.stop()

    # Revenue by country
    st.subheader("Country-wise Revenue")

    country_revenue = (
        sales_data
        .groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        country_revenue.head(15),
        x="Country",
        y="Revenue",
        title="Revenue by Country"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Monthly sales
    st.subheader("Monthly Sales Trend")

    monthly_sales = (
        sales_data
        .assign(
            Month=sales_data["InvoiceDate"].dt.to_period("M").astype(str)
        )
        .groupby("Month")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("InvoiceNo", "nunique")
        )
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.bar(
        monthly_sales,
        x="Month",
        y="Orders",
        title="Monthly Order Volume"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 10. PRODUCT EXPLORER PAGE
# ============================================================

elif page == "Product Explorer":

    st.header("Product Explorer")

    st.write(
        "Search and explore products using their name or StockCode."
    )

    search = st.text_input(
        "Search Product",
        placeholder="Enter product name or StockCode..."
    )

    product_data = products.copy()

    if search:

        product_data = product_data[
            product_data["Description"].str.contains(
                search,
                case=False,
                na=False,
                regex=False
            )
            |
            product_data["StockCode"].str.contains(
                search,
                case=False,
                na=False,
                regex=False
            )
        ]

    product_data = product_data.sort_values(
        "TotalRevenue",
        ascending=False
    )

    st.write(
        f"Found {len(product_data):,} matching products."
    )

    st.dataframe(
        product_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 11. PERSONALIZED RECOMMENDATIONS PAGE
# ============================================================

elif page == "Recommendations":

    st.header("Personalized Product Recommendations")

    st.write(
        "Explore customer purchase behavior and discover "
        "personalized products generated using the ALS model."
    )

    st.divider()

    # --------------------------------------------------------
    # CUSTOMER SELECTION
    # --------------------------------------------------------

    customer_ids = sorted(
        recommendations["userId"].unique().tolist()
    )

    if not customer_ids:

        st.warning(
            "No customers are available in the recommendation dataset."
        )

        st.stop()

    customer_id = st.selectbox(
        "Select Customer ID",
        customer_ids
    )

    # --------------------------------------------------------
    # CUSTOMER PURCHASE HISTORY
    # --------------------------------------------------------

    customer_transactions = transactions[
        transactions["CustomerID"] == customer_id
    ].copy()

    if customer_transactions.empty:

        st.warning(
            "No purchase history found for this customer."
        )

    else:

        # ----------------------------------------------------
        # CUSTOMER OVERVIEW
        # ----------------------------------------------------

        st.subheader(
            f"Customer Overview — {customer_id}"
        )

        total_orders = customer_transactions[
            "InvoiceNo"
        ].nunique()

        total_spent = customer_transactions[
            "Revenue"
        ].sum()

        unique_products = customer_transactions[
            "StockCode"
        ].nunique()

        total_items = customer_transactions[
            "Quantity"
        ].sum()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

        c2.metric(
            "Total Spending",
            f"{total_spent:,.2f}"
        )

        c3.metric(
            "Unique Products",
            f"{unique_products:,}"
        )

        c4.metric(
            "Total Items Purchased",
            f"{total_items:,.0f}"
        )

        st.divider()

        # ----------------------------------------------------
        # CUSTOMER PURCHASE HISTORY
        # ----------------------------------------------------

        st.subheader("Customer Purchase History")

        purchase_history = (
            customer_transactions
            .groupby("StockCode")
            .agg(
                ProductName=("Description", "first"),
                TotalQuantity=("Quantity", "sum"),
                TotalSpent=("Revenue", "sum"),
                NumberOfOrders=("InvoiceNo", "nunique"),
                LastPurchase=("InvoiceDate", "max")
            )
            .reset_index()
            .sort_values(
                "TotalSpent",
                ascending=False
            )
        )

        st.write(
            f"Products purchased: {len(purchase_history):,}"
        )

        st.dataframe(
            purchase_history.rename(
                columns={
                    "StockCode": "Product Code",
                    "ProductName": "Product Name",
                    "TotalQuantity": "Quantity Purchased",
                    "TotalSpent": "Total Spending",
                    "NumberOfOrders": "Orders",
                    "LastPurchase": "Last Purchase Date"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # MOST PURCHASED PRODUCTS
        # ----------------------------------------------------

        st.subheader("Most Purchased Products")

        top_purchased = (
            purchase_history
            .nlargest(10, "TotalQuantity")
            .sort_values("TotalQuantity")
        )

        fig = px.bar(
            top_purchased,
            x="TotalQuantity",
            y="ProductName",
            orientation="h",
            title="Customer's Top 10 Purchased Products"
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ----------------------------------------------------
        # PERSONALIZED RECOMMENDATIONS
        # ----------------------------------------------------

        st.subheader(
            "Recommended Products For This Customer"
        )

        customer_recommendations = recommendations[
            recommendations["userId"] == customer_id
        ].copy()

        customer_recommendations = (
            customer_recommendations
            .sort_values("rank")
            .head(10)
        )

        if customer_recommendations.empty:

            st.warning(
                "No recommendations available for this customer."
            )

        else:

            # Attach product descriptions
            customer_recommendations = (
                customer_recommendations
                .merge(
                    products[
                        [
                            "StockCode",
                            "Description",
                            "TotalRevenue",
                            "TotalQuantity"
                        ]
                    ],
                    on="StockCode",
                    how="left"
                )
            )

            # Check if recommended products were previously purchased
            purchased_codes = set(
                customer_transactions["StockCode"].astype(str)
            )

            customer_recommendations[
                "Previously Purchased"
            ] = (
                customer_recommendations["StockCode"]
                .astype(str)
                .isin(purchased_codes)
                .map({
                    True: "Yes",
                    False: "No"
                })
            )

            st.success(
                f"Generated {len(customer_recommendations)} "
                f"recommendations for Customer {customer_id}"
            )

            st.dataframe(
                customer_recommendations[
                    [
                        "rank",
                        "StockCode",
                        "Description",
                        "predictedScore",
                        "Previously Purchased"
                    ]
                ].rename(
                    columns={
                        "rank": "Rank",
                        "StockCode": "Product Code",
                        "Description": "Recommended Product",
                        "predictedScore": "ALS Score"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # RECOMMENDATION SUMMARY
            # ------------------------------------------------

            new_recommendations = (
                customer_recommendations[
                    customer_recommendations[
                        "Previously Purchased"
                    ] == "No"
                ]
            )

            already_purchased = (
                customer_recommendations[
                    customer_recommendations[
                        "Previously Purchased"
                    ] == "Yes"
                ]
            )

            c1, c2 = st.columns(2)

            c1.metric(
                "New Product Recommendations",
                len(new_recommendations)
            )

            c2.metric(
                "Previously Purchased Products",
                len(already_purchased)
            )

            st.caption(
                "ALS scores indicate relative model preference, "
                "not purchase probabilities. Recommendations "
                "are generated using the model's training data."
            )


# ============================================================
# 12. MODEL PERFORMANCE PAGE
# ============================================================

elif page == "Model Performance":

    st.header("Recommendation Model Performance")

    st.write(
        "Comparison between the personalized ALS model "
        "and the global popularity baseline."
    )

    # Evaluation results
    performance = pd.DataFrame(
        {
            "Model": [
                "ALS Recommendation Model",
                "Popularity Baseline"
            ],
            "Precision@10": [
                0.1181,
                0.0435
            ],
            "Recall@10": [
                0.1145,
                0.0383
            ]
        }
    )

    # KPI comparison
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("ALS Model")

        st.metric(
            "Precision@10",
            "0.1181"
        )

        st.metric(
            "Recall@10",
            "0.1145"
        )

    with col2:

        st.subheader("Popularity Baseline")

        st.metric(
            "Precision@10",
            "0.0435"
        )

        st.metric(
            "Recall@10",
            "0.0383"
        )

    st.divider()

    # Precision comparison
    st.subheader("Precision Comparison")

    fig = px.bar(
        performance,
        x="Model",
        y="Precision@10",
        color="Model",
        title="Precision@10 Comparison",
        text_auto=".4f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Recall comparison
    st.subheader("Recall Comparison")

    fig = px.bar(
        performance,
        x="Model",
        y="Recall@10",
        color="Model",
        title="Recall@10 Comparison",
        text_auto=".4f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Detailed metrics
    st.subheader("Detailed Evaluation Metrics")

    st.dataframe(
        performance,
        use_container_width=True,
        hide_index=True
    )

    # Improvement calculations
    precision_improvement = (
        0.1181 / 0.0435
    )

    recall_improvement = (
        0.1145 / 0.0383
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Precision Improvement",
        f"{precision_improvement:.2f}x"
    )

    c2.metric(
        "Recall Improvement",
        f"{recall_improvement:.2f}x"
    )

    st.info(
        "The ALS model outperforms the global popularity baseline "
        "on both Precision@10 and Recall@10 for this evaluation split."
    )

    st.caption(
        "Evaluation uses a random 80/20 interaction-level split "
        "with seed 42 and 4,026 evaluated users. These are "
        "offline evaluation metrics, not guarantees of live performance."
    )


# ============================================================
# 13. FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Recommendation System | "
    "Built with Python, Apache Spark, PySpark MLlib, "
    "Pandas, Streamlit and Plotly"
)
