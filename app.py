import streamlit as st
from modules.data_utils import load_and_clean_data
from modules.predictor import predict_next_month_expense
from modules.chatbot import classify_query
from modules.visualizer import (
    plot_monthly_expenses_by_category,
    plot_income_vs_expense,
    plot_total_expenses_by_category_pie,
)

from assets.styles import app_header

st.title("💸 Spending Chatbot Assistant")
app_header()  # At the top of your Streamlit app

# section_title("📊 Visual Insights")

# chatbot_message("What did I spend most on last month?", sender="user")
# chatbot_message("You spent the most on Food last month.", sender="bot")

uploaded_file = st.file_uploader("Upload your spending CSV", type="csv")
if uploaded_file:
    df = load_and_clean_data(uploaded_file)
    st.sidebar.subheader("📊 Visualizations")
    vis_option = st.sidebar.radio(
        "Choose a visualization:",
        [
            "Monthly Expenses by Category",
            "Income vs Expenses",
            "Total Expenses by Category (Pie)"
        ]
    )

    # Based on selection
    if vis_option == "Monthly Expenses by Category":
        plot_monthly_expenses_by_category(df)
    elif vis_option == "Income vs Expenses":
        plot_income_vs_expense(df)
    elif vis_option == "Total Expenses by Category (Pie)":
        plot_total_expenses_by_category_pie(df)
    query = st.text_input(
        "Ask something like: 'What did I spend most on last month?'"
    )
    if query:
        intent = classify_query(query)

        if intent == "predict":
            pred = predict_next_month_expense(df)
            st.success(f"📈 You are likely to spend around ₹{pred} next month.")

        elif intent == "chart":
            st.subheader("🧾 Your Monthly Spending Breakdown")
            plot_monthly_expenses_by_category(df)

        elif intent == "max_category":
            last_month = df['month'].max()
            top = (
                df[df['month'] == last_month]
                .groupby('category')['amount']
                .sum()
                .idxmax()
            )
            st.info(f"📊 You spent the most on **{top}** last month.")

        elif intent == "total_spent":
            total = df.groupby('month')['amount'].sum().iloc[-1]
            st.info(f"💰 You spent ₹{total:.2f} last month.")

        elif intent == "bye":
            st.success("👋 Goodbye! Hope to see you again soon!")
        else:
            st.warning(
                "🤖 Sorry, I didn't understand that. Try asking differently."
            )
