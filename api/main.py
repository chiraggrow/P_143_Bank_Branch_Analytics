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
    with engine.connect() as connection:
        query = BranchPerformance.__table__.select().where(
            BranchPerformance.branch_id == branch_id
        )

        df = pd.read_sql(query, connection)

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

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

    return df.iloc[0].to_dict()


# --------------------------------------------------
# Overall Analytics
# --------------------------------------------------

@app.get("/analytics/overview")
def get_overview():
    with engine.connect() as connection:
        query = """
            SELECT
                COALESCE(SUM(customers), 0) AS total_customers,
                COALESCE(SUM(deposits), 0) AS total_deposits,
                COALESCE(SUM(loans), 0) AS total_loans,
                COALESCE(SUM(revenue), 0) AS total_revenue,
                COALESCE(SUM(expenses), 0) AS total_expenses,
                COALESCE(SUM(profit), 0) AS total_profit,
                COALESCE(AVG(customer_satisfaction), 0) AS average_customer_satisfaction,
                COALESCE(SUM(complaints), 0) AS total_complaints
            FROM branch_performance;
        """

        result = connection.exec_driver_sql(query).mappings().one()

    return {
        "total_customers": int(result["total_customers"]),
        "total_deposits": float(result["total_deposits"]),
        "total_loans": float(result["total_loans"]),
        "total_revenue": float(result["total_revenue"]),
        "total_expenses": float(result["total_expenses"]),
        "total_profit": float(result["total_profit"]),
        "average_customer_satisfaction": float(
            result["average_customer_satisfaction"]
        ),
        "total_complaints": int(result["total_complaints"])
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
    with engine.connect() as connection:
        query = """
            SELECT
                month AS "Month",
                SUM(revenue) AS "Revenue",
                SUM(expenses) AS "Expenses",
                SUM(profit) AS "Profit",
                SUM(deposits) AS "Deposits",
                SUM(loans) AS "Loans",
                SUM(customers) AS "Customers"
            FROM branch_performance
            GROUP BY month
            ORDER BY month;
        """

        result = connection.exec_driver_sql(query).mappings().all()

    return [dict(row) for row in result]

# --------------------------------------------------
# Top Branches
# --------------------------------------------------

@app.get("/analytics/top-branches")
def get_top_branches():
    with engine.connect() as connection:
        query = """
            SELECT
                branch_id AS "Branch_ID",
                branch_name AS "Branch_Name",
                region AS "Region",
                SUM(profit) AS "Total_Profit",
                AVG(profit_margin) AS "Avg_Profit_Margin",
                AVG(customer_satisfaction) AS "Avg_Customer_Satisfaction",
                SUM(complaints) AS "Total_Complaints"
            FROM branch_performance
            GROUP BY branch_id, branch_name, region
            ORDER BY SUM(profit) DESC
            LIMIT 10;
        """

        result = connection.exec_driver_sql(query).mappings().all()

    return [dict(row) for row in result]

# --------------------------------------------------
# Bottom Branches
# --------------------------------------------------

@app.get("/analytics/bottom-branches")
def get_bottom_branches():
    with engine.connect() as connection:
        query = """
            SELECT
                branch_id AS "Branch_ID",
                branch_name AS "Branch_Name",
                region AS "Region",
                SUM(profit) AS "Total_Profit",
                AVG(profit_margin) AS "Avg_Profit_Margin",
                AVG(customer_satisfaction) AS "Avg_Customer_Satisfaction",
                SUM(complaints) AS "Total_Complaints"
            FROM branch_performance
            GROUP BY branch_id, branch_name, region
            ORDER BY SUM(profit) ASC
            LIMIT 10;
        """

        result = connection.exec_driver_sql(query).mappings().all()

    return [dict(row) for row in result]


# --------------------------------------------------
# Regional Analysis
# --------------------------------------------------
@app.get("/analytics/regional")
def get_regional_analysis():
    with engine.connect() as connection:
        query = """
            SELECT
                region AS "Region",
                SUM(revenue) AS "Total_Revenue",
                SUM(profit) AS "Total_Profit",
                SUM(deposits) AS "Total_Deposits",
                SUM(loans) AS "Total_Loans",
                AVG(customer_satisfaction) AS "Avg_Customer_Satisfaction",
                SUM(complaints) AS "Total_Complaints"
            FROM branch_performance
            GROUP BY region
            ORDER BY region;
        """

        result = connection.exec_driver_sql(query).mappings().all()

    return [dict(row) for row in result]


@app.get("/analytics/data")
def get_all_data():

    df = get_data()

    return df.to_dict(orient="records")