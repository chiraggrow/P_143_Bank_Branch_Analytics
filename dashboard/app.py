import requests
import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Bank Branch Performance | P_143",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PROFESSIONAL BANKING UI
# =========================================================
st.markdown(
    """
    <style>
    /* ---------- APP ---------- */
    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(30, 136, 229, 0.10), transparent 28%),
            radial-gradient(circle at 5% 25%, rgba(0, 188, 212, 0.06), transparent 25%),
            #07111f;
        color: #e8eef7;
    }

    [data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.92);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1728 0%, #08111e 100%);
        border-right: 1px solid #1c3047;
    }

    [data-testid="stSidebar"] * {
        color: #dbe7f5;
    }

    /* ---------- TYPOGRAPHY ---------- */
    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    .hero {
        padding: 8px 0 20px 0;
    }

    .hero-title {
        font-size: 36px;
        line-height: 1.05;
        font-weight: 850;
        color: #f7fbff;
        letter-spacing: -1.2px;
    }

    .hero-subtitle {
        margin-top: 9px;
        color: #91a4bb;
        font-size: 14px;
    }

    .hero-meta {
        margin-top: 14px;
        display: flex;
        gap: 9px;
        flex-wrap: wrap;
    }

    .pill {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: #0d2034;
        border: 1px solid #23405e;
        color: #9fc7ed;
        font-size: 11px;
        font-weight: 750;
    }

    .pill-green {
        color: #6ee7b7;
        border-color: #1e5b4a;
        background: #0c2924;
    }

    /* ---------- KPI CARDS ---------- */
    .kpi-card {
        background: linear-gradient(145deg, rgba(18, 32, 51, .96), rgba(10, 23, 38, .96));
        border: 1px solid #213750;
        border-radius: 17px;
        padding: 17px 18px 15px;
        min-height: 116px;
        box-shadow: 0 10px 30px rgba(0,0,0,.20);
    }

    .kpi-label {
        color: #8ea3ba;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 800;
    }

    .kpi-value {
        color: #f7fbff;
        font-size: 26px;
        font-weight: 850;
        margin-top: 8px;
    }

    .kpi-note {
        color: #61768d;
        font-size: 11px;
        margin-top: 4px;
    }

    /* ---------- SECTION HEADERS ---------- */
    .section-kicker {
        color: #5eb6ff;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-size: 10px;
        font-weight: 850;
        margin-bottom: 4px;
    }

    .section-title {
        color: #f3f7fc;
        font-size: 23px;
        font-weight: 820;
        margin-bottom: 2px;
    }

    .section-subtitle {
        color: #8094aa;
        font-size: 12px;
        margin-bottom: 16px;
    }

    /* ---------- CHART CONTAINERS ---------- */
    .chart-title {
        color: #e9f1fa;
        font-size: 15px;
        font-weight: 750;
        margin: 4px 0 8px;
    }

    /* ---------- INSIGHT CARDS ---------- */
    .insight {
        background: #0d1a2b;
        border: 1px solid #20364f;
        border-radius: 14px;
        padding: 13px 15px;
        margin-bottom: 9px;
    }

    .insight-title {
        color: #dcecff;
        font-weight: 750;
        font-size: 13px;
    }

    .insight-text {
        color: #8398ae;
        font-size: 12px;
        margin-top: 4px;
    }

    /* ---------- TABLE / METRICS ---------- */
    div[data-testid="stMetric"] {
        background: #0d1a2b;
        border: 1px solid #20364f;
        border-radius: 13px;
        padding: 12px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #20364f;
        border-radius: 13px;
        overflow: hidden;
    }

    /* ---------- SIDEBAR ---------- */
    .sidebar-brand {
        padding: 5px 0 12px;
    }

    .sidebar-brand-title {
        font-size: 18px;
        font-weight: 850;
        color: #f5f9ff;
    }

    .sidebar-brand-sub {
        color: #71869d;
        font-size: 11px;
        margin-top: 2px;
    }

    .status-online {
        background: #0b2a24;
        border: 1px solid #1c604f;
        color: #69e5b0;
        border-radius: 10px;
        padding: 9px 11px;
        font-size: 11px;
        font-weight: 750;
    }

    .status-offline {
        background: #321719;
        border: 1px solid #6b292e;
        color: #ff9a9f;
        border-radius: 10px;
        padding: 9px 11px;
        font-size: 11px;
        font-weight: 750;
    }

    .footer {
        text-align: center;
        color: #53677d;
        font-size: 11px;
        padding: 28px 0 8px;
    }

    /* ---------- STREAMLIT POLISH ---------- */
    .stButton > button {
        border-radius: 10px;
        font-weight: 750;
        border: 1px solid #2d6ea8;
    }

    .stSelectbox label,
    .stTextArea label {
        color: #a9bad0 !important;
        font-weight: 650;
    }

    hr {
        border-color: #1a2d43;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# CONSTANTS
API_URL = "http://127.0.0.1:8001"


@st.cache_data(ttl=60)
def load_data():

    response = requests.get(
        f"{API_URL}/analytics/data",
        timeout=10
    )

    response.raise_for_status()

    data = pd.DataFrame(response.json())

    data = data.rename(columns={
        "month": "Month",
        "branch_id": "Branch_ID",
        "branch_name": "Branch_Name",
        "region": "Region",
        "customers": "Customers",
        "new_customers": "New_Customers",
        "deposits": "Deposits",
        "loans": "Loans",
        "revenue": "Revenue",
        "expenses": "Expenses",
        "employees": "Employees",
        "transactions": "Transactions",
        "complaints": "Complaints",
        "customer_satisfaction": "Customer_Satisfaction",
        "profit": "Profit",
        "profit_margin": "Profit_Margin",
        "loan_to_deposit_ratio": "Loan_to_Deposit_Ratio",
        "complaint_rate": "Complaint_Rate",
        "revenue_per_employee": "Revenue_per_Employee",
        "customers_per_employee": "Customers_per_Employee",
        "performance_score": "Performance_Score",
        "customer_feedback": "Customer_Feedback",
        "sentiment": "Sentiment",
        "polarity": "Polarity",
        "issue_category": "Issue_Category",
        "positive": "Positive",
        "negative": "Negative",
        "neutral": "Neutral",
        "negative_feedback_rate": "Negative_Feedback_Rate"
    })

    data["Month"] = pd.to_datetime(
        data["Month"],
        format="%Y-%m"
    )

    return data


@st.cache_data(ttl=60)
def get_api_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None


def money(value):
    return f"{value:,.0f}"


def pct(value):
    return f"{value:.2f}%"


def section(title, subtitle="", kicker=""):
    if kicker:
        st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def kpi_card(container, label, value, note):
    with container:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# LOAD DATA
# =========================================================
df = load_data()

# =========================================================
# API CONNECTION CHECK
# =========================================================
api_branches = get_api_data("/branches")

if api_branches is None:
    st.error(
        "FastAPI is not running. Start it using: "
        "`uvicorn api.main:app --reload --port 8001`"
    )
    st.stop()

api_branches = pd.DataFrame(api_branches)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🏦 P_143 Analytics</div>
            <div class="sidebar-brand-sub">Bank Branch Intelligence Platform</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 🎛 Dashboard Filters")

    regions = ["All Regions"] + sorted(df["Region"].dropna().unique().tolist())
    selected_region = st.selectbox("Region", regions)

    months = sorted(df["Month"].dt.strftime("%Y-%m").unique())
    selected_month = st.selectbox("Month", ["All Months"] + months)

    branch_options = sorted(api_branches["Branch_Name"].unique().tolist())
    selected_branch = st.selectbox(
        "Branch Explorer",
        ["All Branches"] + branch_options,
    )

    st.divider()

    st.markdown("### System Status")
    st.markdown(
        '<div class="status-online">● FASTAPI CONNECTED</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("Data Analytics • NLP • FastAPI • Streamlit")
    st.caption("P_143 | Bank Branch Performance")

# =========================================================
# FILTER DATA
# =========================================================
filtered_df = df.copy()

if selected_region != "All Regions":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if selected_month != "All Months":
    filtered_df = filtered_df[
        filtered_df["Month"].dt.strftime("%Y-%m") == selected_month
    ]

# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Bank Branch Performance</div>
        <div class="hero-subtitle">
            Executive intelligence dashboard for financial performance,
            operational efficiency and customer experience.
        </div>
        <div class="hero-meta">
            <span class="pill pill-green">● LIVE API</span>
            <span class="pill">P_143</span>
            <span class="pill">Financial Analytics</span>
            <span class="pill">Customer NLP</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# EXECUTIVE KPIs
# =========================================================
section(
    "Executive Overview",
    "Network-level financial and customer KPIs based on the active filters.",
    "Management Snapshot",
)

total_customers = filtered_df["Customers"].sum()
total_deposits = filtered_df["Deposits"].sum()
total_loans = filtered_df["Loans"].sum()
total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()

k1, k2, k3, k4, k5 = st.columns(5)

kpi_card(k1, "Customers", f"{total_customers:,.0f}", "Total customer base")
kpi_card(k2, "Deposits", money(total_deposits), "Deposit portfolio")
kpi_card(k3, "Loans", money(total_loans), "Loan portfolio")
kpi_card(k4, "Revenue", money(total_revenue), "Generated revenue")
kpi_card(k5, "Net Profit", money(total_profit), "Revenue − expenses")

# =========================================================
# FINANCIAL PERFORMANCE
# =========================================================
st.divider()

section(
    "Financial Performance",
    "Track revenue and profitability trends across the selected period.",
    "Financial Intelligence",
)

monthly_trend = (
    filtered_df.groupby("Month")
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
    )
    .sort_index()
)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-title">Revenue Trend</div>', unsafe_allow_html=True)
    st.line_chart(monthly_trend[["Revenue"]], height=300)

with col2:
    st.markdown('<div class="chart-title">Profit Trend</div>', unsafe_allow_html=True)
    st.line_chart(monthly_trend[["Profit"]], height=300)

# =========================================================
# REGIONAL PERFORMANCE
# =========================================================
st.divider()

section(
    "Regional Performance",
    "Compare profitability, revenue and lending activity by region.",
    "Geographic Intelligence",
)

regional_data = (
    filtered_df.groupby("Region")
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Deposits=("Deposits", "sum"),
        Loans=("Loans", "sum"),
    )
    .sort_values("Profit", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-title">Regional Profit</div>', unsafe_allow_html=True)
    st.bar_chart(regional_data[["Profit"]], height=280)

with col2:
    st.markdown('<div class="chart-title">Regional Revenue</div>', unsafe_allow_html=True)
    st.bar_chart(regional_data[["Revenue"]], height=280)

st.markdown('<div class="chart-title">Loans vs Deposits by Region</div>', unsafe_allow_html=True)
st.bar_chart(regional_data[["Deposits", "Loans"]], height=280)

# =========================================================
# BRANCH PERFORMANCE
# =========================================================
st.divider()

section(
    "Branch Performance",
    "Compare branches using profit, margin, satisfaction and the project performance score.",
    "Branch Intelligence",
)

branch_summary = (
    filtered_df.groupby(["Branch_ID", "Branch_Name", "Region"])
    .agg(
        Total_Profit=("Profit", "sum"),
        Avg_Profit_Margin=("Profit_Margin", "mean"),
        Avg_Satisfaction=("Customer_Satisfaction", "mean"),
        Total_Complaints=("Complaints", "sum"),
        Avg_Performance_Score=("Performance_Score", "mean"),
    )
    .reset_index()
)

top_10 = branch_summary.sort_values("Total_Profit", ascending=False).head(10)
bottom_10 = branch_summary.sort_values("Total_Profit", ascending=True).head(10)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Highest Profit Branches")
    st.bar_chart(
        top_10.set_index("Branch_Name")[["Total_Profit"]],
        height=280,
    )
    st.dataframe(
        top_10[
            [
                "Branch_Name",
                "Region",
                "Total_Profit",
                "Avg_Profit_Margin",
                "Avg_Satisfaction",
            ]
        ],
        hide_index=True,
        width="stretch",
    )

with col2:
    st.markdown("### ⚠️ Lowest Profit Branches")
    st.bar_chart(
        bottom_10.set_index("Branch_Name")[["Total_Profit"]],
        height=280,
    )
    st.dataframe(
        bottom_10[
            [
                "Branch_Name",
                "Region",
                "Total_Profit",
                "Avg_Profit_Margin",
                "Avg_Satisfaction",
            ]
        ],
        hide_index=True,
        width="stretch",
    )

# =========================================================
# BRANCH EXPLORER
# =========================================================
if selected_branch != "All Branches":

    st.divider()

    section(
        f"{selected_branch} — Branch Explorer",
        "Detailed financial, customer and efficiency metrics for the selected branch.",
        "Drill Down",
    )

    branch_df = df[df["Branch_Name"] == selected_branch].copy()

    branch_customers = branch_df["Customers"].sum()
    branch_deposits = branch_df["Deposits"].sum()
    branch_loans = branch_df["Loans"].sum()
    branch_profit = branch_df["Profit"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Customers", f"{branch_customers:,.0f}")
    c2.metric("Total Deposits", money(branch_deposits))
    c3.metric("Total Loans", money(branch_loans))
    c4.metric("Total Profit", money(branch_profit))

    branch_monthly = (
        branch_df.groupby("Month")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Customers=("Customers", "sum"),
        )
        .sort_index()
    )

    st.markdown("### 📈 Branch Monthly Trend")
    st.line_chart(branch_monthly, height=320)

    avg_profit_margin = branch_df["Profit_Margin"].mean()
    avg_ltd = branch_df["Loan_to_Deposit_Ratio"].mean()
    avg_complaint_rate = branch_df["Complaint_Rate"].mean()
    avg_satisfaction = branch_df["Customer_Satisfaction"].mean()

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Avg Profit Margin", pct(avg_profit_margin))
    e2.metric("Avg Loan / Deposit", pct(avg_ltd))
    e3.metric("Avg Complaint Rate", pct(avg_complaint_rate))
    e4.metric("Customer Satisfaction", f"{avg_satisfaction:.2f}/5")

# =========================================================
# CUSTOMER EXPERIENCE
# =========================================================
st.divider()

section(
    "Customer Experience",
    "Monitor satisfaction and complaints across the branch network.",
    "Customer Intelligence",
)

customer_analysis = (
    filtered_df.groupby("Region")
    .agg(
        Satisfaction=("Customer_Satisfaction", "mean"),
        Complaints=("Complaints", "sum"),
    )
)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-title">Customer Satisfaction by Region</div>', unsafe_allow_html=True)
    st.bar_chart(customer_analysis[["Satisfaction"]], height=280)

with col2:
    st.markdown('<div class="chart-title">Complaints by Region</div>', unsafe_allow_html=True)
    st.bar_chart(customer_analysis[["Complaints"]], height=280)

# =========================================================
# NLP ANALYSIS
# =========================================================
st.divider()

section(
    "Customer Feedback — NLP Analysis",
    "Sentiment and issue-category analysis using the project's NLP module.",
    "Natural Language Intelligence",
)

sentiment_counts = (
    filtered_df["Sentiment"]
    .value_counts()
    .reindex(["Positive", "Negative", "Neutral"], fill_value=0)
)

s1, s2, s3 = st.columns(3)
s1.metric("Positive Feedback", int(sentiment_counts["Positive"]))
s2.metric("Negative Feedback", int(sentiment_counts["Negative"]))
s3.metric("Neutral Feedback", int(sentiment_counts["Neutral"]))

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-title">Sentiment Distribution</div>', unsafe_allow_html=True)
    st.bar_chart(sentiment_counts, height=280)

with col2:
    st.markdown('<div class="chart-title">Customer Issue Categories</div>', unsafe_allow_html=True)
    issue_counts = filtered_df["Issue_Category"].value_counts().head(10)
    st.bar_chart(issue_counts, height=280)

# =========================================================
# LIVE NLP ANALYZER
# =========================================================
st.markdown("### 🔎 Analyze New Customer Feedback")

feedback_text = st.text_area(
    "Customer feedback",
    placeholder="Example: The waiting time was too long and the staff was not helpful.",
    height=120,
)

if st.button("Analyze Feedback", type="primary"):

    if not feedback_text.strip():
        st.warning("Please enter customer feedback.")
    else:
        try:
            feedback_response = requests.post(
                f"{API_URL}/feedback/analyze",
                json={"feedback": feedback_text},
                timeout=5,
            )

            if feedback_response.status_code == 200:
                feedback_result = feedback_response.json()

                result_col1, result_col2 = st.columns(2)

                with result_col1:
                    st.success(
                        f"Sentiment: {feedback_result['sentiment']}"
                    )

                with result_col2:
                    st.info(
                        f"Polarity: {feedback_result['polarity']:.4f}"
                    )

            else:
                st.error("Could not analyze feedback.")

        except requests.exceptions.RequestException:
            st.error("FastAPI connection failed.")

# =========================================================
# PERFORMANCE SCORE
# =========================================================
st.divider()

section(
    "Branch Performance Score",
    "Composite score used in this project to compare branch performance.",
    "Performance Intelligence",
)

performance_ranking = (
    branch_summary.sort_values(
        "Avg_Performance_Score",
        ascending=False,
    )
    .head(10)
)

st.bar_chart(
    performance_ranking.set_index("Branch_Name")[["Avg_Performance_Score"]],
    height=320,
)

# =========================================================
# DETAILED DATA
# =========================================================
st.divider()

section(
    "Detailed Branch Performance",
    "Full analytical dataset after the active region and month filters.",
    "Data Explorer",
)

display_columns = [
    "Month",
    "Branch_ID",
    "Branch_Name",
    "Region",
    "Customers",
    "New_Customers",
    "Deposits",
    "Loans",
    "Revenue",
    "Expenses",
    "Profit",
    "Profit_Margin",
    "Loan_to_Deposit_Ratio",
    "Complaint_Rate",
    "Revenue_per_Employee",
    "Customers_per_Employee",
    "Customer_Satisfaction",
    "Complaints",
    "Sentiment",
    "Issue_Category",
    "Negative_Feedback_Rate",
    "Performance_Score",
]

st.dataframe(
    filtered_df[display_columns],
    hide_index=True,
    width="stretch",
)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        P_143 — Bank Branch Performance Analytics
        &nbsp;•&nbsp; Python + Pandas + NLP + FastAPI + Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
