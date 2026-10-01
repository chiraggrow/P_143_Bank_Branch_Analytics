from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Text,
    UniqueConstraint
)

from src.database import Base


class BranchPerformance(Base):

    __tablename__ = "branch_performance"

    __table_args__ = (
        UniqueConstraint(
            "branch_id",
            "month",
            name="uq_branch_performance_branch_month"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    month = Column(
        String(7)
    )

    branch_id = Column(
        Integer,
        index=True
    )

    branch_name = Column(
        String(100)
    )

    region = Column(
        String(50),
        index=True
    )

    customers = Column(Integer)
    new_customers = Column(Integer)

    deposits = Column(
        Numeric(15, 2)
    )

    loans = Column(
        Numeric(15, 2)
    )

    revenue = Column(
        Numeric(15, 2)
    )

    expenses = Column(
        Numeric(15, 2)
    )

    employees = Column(Integer)
    transactions = Column(Integer)
    complaints = Column(Integer)

    customer_satisfaction = Column(
        Numeric(5, 2)
    )

    profit = Column(
        Numeric(15, 2)
    )

    profit_margin = Column(
        Numeric(10, 2)
    )

    loan_to_deposit_ratio = Column(
        Numeric(10, 2)
    )

    complaint_rate = Column(
        Numeric(10, 2)
    )

    revenue_per_employee = Column(
        Numeric(15, 2)
    )

    customers_per_employee = Column(
        Numeric(15, 2)
    )

    performance_score = Column(
        Numeric(10, 2)
    )

    customer_feedback = Column(
        Text
    )

    sentiment = Column(
        String(20)
    )

    polarity = Column(
        Numeric(10, 4)
    )

    issue_category = Column(
        String(100)
    )

    positive = Column(Integer)
    negative = Column(Integer)
    neutral = Column(Integer)

    negative_feedback_rate = Column(
        Numeric(10, 2)
    )