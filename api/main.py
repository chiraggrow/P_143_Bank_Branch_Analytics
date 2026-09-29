from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from src.nlp.sentiment import analyze_sentiment

app = FastAPI(
    title="Bank Branch Performance API",
    description="API for branch performance and customer feedback analytics",
    version="1.0.0"
)


# Load processed branch data
df = pd.read_csv(
    "data/processed/branch_performance_with_nlp.csv"
)


@app.get("/")
def home():
    return {
        "message": "Bank Branch Performance API is running"
    }


@app.get("/branches")
def get_branches():
    return df[
        [
            "Branch_ID",
            "Branch_Name",
            "Region"
        ]
    ].to_dict(orient="records")


@app.get("/branches/{branch_id}")
def get_branch(branch_id: int):

    branch = df[df["Branch_ID"] == branch_id]

    if branch.empty:
        return {
            "error": "Branch not found"
        }

    return branch.iloc[0].to_dict()


@app.get("/analytics/overview")
def get_overview():

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


class FeedbackRequest(BaseModel):
    feedback: str


@app.post("/feedback/analyze")
def analyze_feedback(request: FeedbackRequest):

    sentiment, polarity = analyze_sentiment(
        request.feedback
    )

    return {
        "feedback": request.feedback,
        "sentiment": sentiment,
        "polarity": polarity
    }