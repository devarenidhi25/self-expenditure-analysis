import pandas as pd


def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    df['category'] = df['category'].str.strip().str.title()
    df['category'] = df['category'].replace({
        'Restuarant': 'Restaurant',
        'Coffe': 'Coffee'
    })
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['month'] = df['date'].dt.to_period('M')
    return df
