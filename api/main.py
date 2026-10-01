from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

from src.database import engine
from src.models import BranchPerformance
from src.nlp.sentiment import analyze_sentiment


app = FastAPI(
    title="Bank Branch Performance API",
    description="API for branch performance and customer feedback analytics",
    version="1.0.0"
)


# --------------------------------------------------
# Load branch data from PostgreSQL
# --------------------------------------------------

def get_data():
    with engine.connect() as connection:
        df = pd.read_sql(
            BranchPerformance.__table__.select(),
            connection
        )

    # Convert database column names to existing API names
    df = df.rename(columns={
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

    return df


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Bank Branch Performance API is running",
        "database": "PostgreSQL"
    }


# --------------------------------------------------
# Branches
# --------------------------------------------------

@app.get("/branches")
def get_branches():

    df = get_data()

    return df[
        [
            "Branch_ID",
            "Branch_Name",
            "Region"
        ]
    ].to_dict(orient="records")


@app.get("/branches/{branch_id}")
def get_branch(branch_id: int):

    df = get_data()

    branch = df[df["Branch_ID"] == branch_id]

    if branch.empty:
     raise HTTPException(
        status_code=404,
        detail="Branch not found"
    )

    return branch.iloc[0].to_dict()


# --------------------------------------------------
# Overall Analytics
# --------------------------------------------------

@app.get("/analytics/overview")
def get_overview():

    df = get_data()

    return {
        "total_customers": int(df["Customers"].sum()),
        "total_deposits": float(df["Deposits"].sum()),
        "total_loans": float(df["Loans"].sum()),
        "total_revenue": float(df["Revenue"].sum()),
        "total_expenses": float(df["Expenses"].sum()),
        "total_profit": float(df["Profit"].sum()),
        "average_customer_satisfaction": float(
            df["Customer_Satisfaction"].mean()
        ),
        "total_complaints": int(df["Complaints"].sum())
    }


# --------------------------------------------------
# NLP Feedback
# --------------------------------------------------

class FeedbackRequest(BaseModel):
    feedback: str


@app.post("/feedback/analyze")
def analyze_feedback(request: FeedbackRequest):

    sentiment, confidence = analyze_sentiment(
        request.feedback
    )

    return {
        "feedback": request.feedback,
        "sentiment": sentiment,
        "confidence": confidence
    }


# --------------------------------------------------
# Monthly Trends
# --------------------------------------------------

@app.get("/analytics/trends")
def get_trends():

    df = get_data()

    monthly = (
        df.groupby("Month")
        .agg(
            Revenue=("Revenue", "sum"),
            Expenses=("Expenses", "sum"),
            Profit=("Profit", "sum"),
            Deposits=("Deposits", "sum"),
            Loans=("Loans", "sum"),
            Customers=("Customers", "sum")
        )
        .reset_index()
    )

    return monthly.to_dict(orient="records")


# --------------------------------------------------
# Top Branches
# --------------------------------------------------

@app.get("/analytics/top-branches")
def get_top_branches():

    df = get_data()

    branch_summary = (
        df.groupby(
            ["Branch_ID", "Branch_Name", "Region"]
        )
        .agg(
            Total_Profit=("Profit", "sum"),
            Avg_Profit_Margin=("Profit_Margin", "mean"),
            Avg_Customer_Satisfaction=(
                "Customer_Satisfaction",
                "mean"
            ),
            Total_Complaints=("Complaints", "sum")
        )
        .reset_index()
    )

    top = branch_summary.sort_values(
        "Total_Profit",
        ascending=False
    ).head(10)

    return top.to_dict(orient="records")


# --------------------------------------------------
# Bottom Branches
# --------------------------------------------------

@app.get("/analytics/bottom-branches")
def get_bottom_branches():

    df = get_data()

    branch_summary = (
        df.groupby(
            ["Branch_ID", "Branch_Name", "Region"]
        )
        .agg(
            Total_Profit=("Profit", "sum"),
            Avg_Profit_Margin=("Profit_Margin", "mean"),
            Avg_Customer_Satisfaction=(
                "Customer_Satisfaction",
                "mean"
            ),
            Total_Complaints=("Complaints", "sum")
        )
        .reset_index()
    )

    bottom = branch_summary.sort_values(
        "Total_Profit",
        ascending=True
    ).head(10)

    return bottom.to_dict(orient="records")


# --------------------------------------------------
# Regional Analysis
# --------------------------------------------------

@app.get("/analytics/regional")
def get_regional_analysis():

    df = get_data()

    regional = (
        df.groupby("Region")
        .agg(
            Total_Revenue=("Revenue", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Deposits=("Deposits", "sum"),
            Total_Loans=("Loans", "sum"),
            Avg_Customer_Satisfaction=("Customer_Satisfaction", "mean"),
            Total_Complaints=("Complaints", "sum")
        )
        .reset_index()
    )

    return regional.to_dict(orient="records")


@app.get("/analytics/data")
def get_all_data():

    df = get_data()

    return df.to_dict(orient="records")