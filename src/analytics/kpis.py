import pandas as pd


def calculate_kpis(df):
    df = df.copy()

    df["Profit"] = df["Revenue"] - df["Expenses"]

    df["Profit_Margin"] = (
        df["Profit"] / df["Revenue"]
    ) * 100

    df["Loan_to_Deposit_Ratio"] = (
        df["Loans"] / df["Deposits"]
    ) * 100

    df["Complaint_Rate"] = (
        df["Complaints"] / df["Customers"]
    ) * 100

    df["Revenue_per_Employee"] = (
        df["Revenue"] / df["Employees"]
    )

    df["Customers_per_Employee"] = (
        df["Customers"] / df["Employees"]
    )

    return df
