import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def plot_monthly_expenses_by_category(df):
    monthly = (
        df.groupby(['month', 'category'])['amount']
        .sum()
        .unstack()
        .fillna(0)
    )
    fig, ax = plt.subplots(figsize=(15, 7))
    monthly.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_title('Monthly Expenses by Category')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount Spent')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


def plot_income_vs_expense(df):
    user_income = st.number_input(
        "Enter your monthly income",
        min_value=0.0,
        value=2000.0,
        step=100.0
    )

    monthly_total = df.groupby('month')['amount'].sum().reset_index()
    monthly_total['income'] = user_income
    monthly_total['savings'] = (
        monthly_total['income'] - monthly_total['amount']
    )

    fig, ax = plt.subplots(figsize=(13, 7))
    monthly_total.set_index('month')[['income', 'amount']].plot(
        kind='bar', stacked=True, ax=ax, colormap='tab20'
    )
    ax.set_title('Income vs Expenses')
    ax.set_ylabel('Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


def plot_total_expenses_by_category_pie(df):
    category_expense = df.groupby('category')['amount'].sum()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        category_expense,
        labels=category_expense.index,
        autopct='%1.1f%%',
        startangle=140,
        shadow=True,
        colors=plt.cm.tab20.colors
    )
    ax.set_title('Total Expenses by Category')
    ax.axis('equal')  # Makes the pie circular
    st.pyplot(fig)
