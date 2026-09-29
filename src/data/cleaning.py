import pandas as pd

def clean_data(df):
    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean column names
    df.columns = df.columns.str.strip()

    return df