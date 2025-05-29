from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd


def predict_next_month_expense(df):
    monthly_total = df.groupby('month')['amount'].sum().reset_index()
    monthly_total['month_idx'] = range(1, len(monthly_total)+1)

    X = monthly_total[['month_idx']]
    y = monthly_total['amount']

    model = LinearRegression().fit(X, y)
    next_month_idx = [[X['month_idx'].max() + 1]]
    prediction = model.predict(next_month_idx)[0]
    return round(prediction, 2)
