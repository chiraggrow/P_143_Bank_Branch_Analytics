import pandas as pd

from src.analytics.kpis import calculate_kpis


def test_profit_calculation():

    data = pd.DataFrame({
        "Revenue": [1000],
        "Expenses": [400],
        "Loans": [500],
        "Deposits": [1000],
        "Complaints": [10],
        "Customers": [1000],
        "Employees": [10]
    })

    result = calculate_kpis(data)

    assert result["Profit"].iloc[0] == 600