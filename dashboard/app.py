import requests
import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bank Branch Performance",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "data/processed/branch_performance_with_nlp.csv"
)

# =========================================================
# FASTAPI CONNECTION
# =========================================================

API_URL = "http://127.0.0.1:8001"

api_response = requests.get(
    f"{API_URL}/branches"
)

if api_response.status_code == 200:
    api_branches = pd.DataFrame(api_response.json())
else:
    st.error("FastAPI connection failed.")
    api_branches = pd.DataFrame()


overview_response = requests.get(
    f"{API_URL}/analytics/overview"
)

if overview_response.status_code == 200:
    overview_data = overview_response.json()
else:
    st.error("Could not load overview data from FastAPI.")
    overview_data = {}


# =========================================================
# HEADER
# =========================================================

st.title("🏦 Bank Branch Performance Dashboard")

st.markdown(
    """
    **Branch-level banking performance, customer satisfaction
    and NLP-based customer feedback analysis**
    """
)

st.success("Analytics data loaded successfully.")


# =========================================================
# SIDEBAR — BRANCH SELECTION
# =========================================================

st.sidebar.header("Dashboard Filters")
selected_branch = st.sidebar.selectbox(
    "Select Branch",
    api_branches["Branch_Name"].unique()
)

selected_branch_id = int(
    api_branches[
        api_branches["Branch_Name"] == selected_branch
    ]["Branch_ID"].iloc[0]
)

branch_response = requests.get(
    f"{API_URL}/branches/{selected_branch_id}"
)

if branch_response.status_code == 200:
    selected_data = pd.DataFrame(
        [branch_response.json()]
    )
else:
    st.error("Could not load branch data from FastAPI.")
    selected_data = pd.DataFrame()


# =========================================================
# OVERALL KPIs
# =========================================================

st.subheader("📊 Overall Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{df['Customers'].sum():,}"
)

col2.metric(
    "Total Deposits",
    f"{df['Deposits'].sum():,.0f}"
)

col3.metric(
    "Total Loans",
    f"{df['Loans'].sum():,.0f}"
)

col4.metric(
    "Total Profit",
    f"{df['Profit'].sum():,.0f}"
)


# =========================================================
# SELECTED BRANCH
# =========================================================

st.divider()

st.subheader(
    f"🏢 {selected_branch} — Branch Performance"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{overview_data['total_customers']:,}"
)

col2.metric(
    "Total Deposits",
    f"{overview_data['total_deposits']:,.0f}"
)

col3.metric(
    "Total Loans",
    f"{overview_data['total_loans']:,.0f}"
)

col4.metric(
    "Total Profit",
    f"{overview_data['total_profit']:,.0f}"
)

# =========================================================
# BRANCH FINANCIAL ANALYSIS
# =========================================================

st.divider()

st.subheader("💰 Branch Financial Analysis")



col1, col2 = st.columns(2)

with col1:

    st.markdown("**Profit by Branch**")

    st.bar_chart(
        df.set_index("Branch_Name")["Profit"]
    )


with col2:

    st.markdown("**Profit Margin by Branch**")

    st.bar_chart(
        df.set_index("Branch_Name")["Profit_Margin"]
    )


# =========================================================
# LOANS VS DEPOSITS
# =========================================================

st.subheader("🏦 Loans vs Deposits")

loan_deposit_data = df[
    ["Branch_Name", "Deposits", "Loans"]
].set_index("Branch_Name")

st.bar_chart(loan_deposit_data)


# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

st.divider()

st.subheader("👥 Customer Analysis")

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Customer Satisfaction by Branch**")

    st.bar_chart(
        df.set_index("Branch_Name")[
            "Customer_Satisfaction"
        ]
    )


with col2:

    st.markdown("**Complaints by Branch**")

    st.bar_chart(
        df.set_index("Branch_Name")[
            "Complaints"
        ]
    )


# =========================================================
# NLP / CUSTOMER FEEDBACK
# =========================================================

st.divider()

st.subheader("💬 Customer Feedback — NLP Analysis")

st.markdown("### 🔎 Analyze New Customer Feedback")

feedback_text = st.text_area(
    "Enter customer feedback",
    placeholder="Example: The waiting time was too long."
)

if st.button("Analyze Feedback"):

    feedback_response = requests.post(
        f"{API_URL}/feedback/analyze",
        json={
            "feedback": feedback_text
        }
    )

    if feedback_response.status_code == 200:

        feedback_result = feedback_response.json()

        st.success(
            f"Sentiment: {feedback_result['sentiment']}"
        )

        st.write(
            f"Polarity: {feedback_result['polarity']}"
        )

    else:
        st.error("Could not analyze feedback.")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Positive Feedback",
    int(selected_data["Positive"].iloc[0])
)

col2.metric(
    "Negative Feedback",
    int(selected_data["Negative"].iloc[0])
)

col3.metric(
    "Neutral Feedback",
    int(selected_data["Neutral"].iloc[0])
)


st.markdown(
    f"**Negative Feedback Rate — {selected_branch}**"
)

st.metric(
    "Negative Feedback Rate",
    f"{selected_data['Negative_Feedback_Rate'].iloc[0]:.2f}%"
)


# =========================================================
# SENTIMENT CHART
# =========================================================

sentiment_chart = pd.DataFrame({
    "Sentiment": [
        "Positive",
        "Negative",
        "Neutral"
    ],
    "Count": [
        selected_data["Positive"].iloc[0],
        selected_data["Negative"].iloc[0],
        selected_data["Neutral"].iloc[0]
    ]
})

st.bar_chart(
    sentiment_chart.set_index("Sentiment")
)


# =========================================================
# REGIONAL ANALYSIS
# =========================================================

st.divider()

st.subheader("🌍 Regional Revenue Analysis")

region_revenue = (
    df.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(region_revenue)


# =========================================================
# PERFORMANCE SCORE
# =========================================================

st.subheader("⭐ Branch Performance Score")

performance_data = df[
    ["Branch_Name", "Performance_Score"]
].set_index("Branch_Name")

st.bar_chart(performance_data)


# =========================================================
# COMPLETE PERFORMANCE TABLE
# =========================================================

st.divider()

st.subheader("📋 Detailed Branch Performance")

performance_columns = [
    "Branch_ID",
    "Branch_Name",
    "Region",
    "Customers",
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
    "Positive",
    "Negative",
    "Neutral",
    "Negative_Feedback_Rate",
    "Performance_Score"
]

st.dataframe(
    df[performance_columns],
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "P_143 — Bank Branch Performance Analytics | "
    "Data Analytics + NLP + Streamlit"
)