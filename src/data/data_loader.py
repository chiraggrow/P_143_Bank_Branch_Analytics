import pandas as pd

def load_data(data):
    if isinstance(data, pd.DataFrame):
        return data.copy()

    if isinstance(data, dict):
        return pd.DataFrame(data)

    raise TypeError("Data must be a DataFrame or dictionary.")