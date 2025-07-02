# app.py  ⟶  streamlined chatbot interface
import streamlit as st
from modules.data_utils import load_and_clean_data
from modules.predictor import predict_next_month_expense
from modules.chatbot import classify_query
from modules.visualizer import (
    plot_monthly_expenses_by_category,
    plot_income_vs_expense,
    plot_total_expenses_by_category_pie,
)
from modules.gemini_chat import get_gemini_response
from assets.styles import app_header

st.set_page_config(
    page_title="FinZen – Your Spending Chatbot",
    page_icon="assets/money-logo.jpg"  # or "./assets/money-logo.jpg"
)

app_header()

# ───────────────────────────── Session state ──────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content":
         "👋 Hi! I’m your Spending Assistant.\n\n"
         "• Upload a spending CSV so I can crunch your numbers, **or**\n"
         "• Just ask me anything about budgeting, saving, or expenses.\n\n"
         "What would you like to do first?"}
    ]
if "df" not in st.session_state:
    st.session_state.df = None

# ─────────────────────────── Sidebar: file upload ─────────────────────────
with st.sidebar:
    st.subheader("📂 Upload your spending CSV")
    uploaded_file = st.file_uploader("Choose a file", type="csv", label_visibility="collapsed")
    if uploaded_file:
        st.session_state.df = load_and_clean_data(uploaded_file)
        st.success("Data loaded! Feel free to ask data questions or choose a visual below. 🎉")

    # Offer visualisations only when data is present
    if st.session_state.df is not None:
        vis_option = st.radio(
            "Quick visual:",
            ["Monthly Expenses by Category",
             "Income vs Expenses",
             "Total Expenses by Category (Pie)"],
            index=0
        )
        if vis_option == "Monthly Expenses by Category":
            plot_monthly_expenses_by_category(st.session_state.df)
        elif vis_option == "Income vs Expenses":
            plot_income_vs_expense(st.session_state.df)
        elif vis_option == "Total Expenses by Category (Pie)":
            plot_total_expenses_by_category_pie(st.session_state.df)

# ─────────────────────────── Chat history display ────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────── Chat input ──────────────────────────────
user_query = st.chat_input("Type your message here…")
if user_query:
    # Show user bubble immediately
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    df = st.session_state.df
    intent = classify_query(user_query)

    # ───────── Data‑driven intents (require df) ──────────
    if intent in ("predict", "chart", "max_category", "total_spent") and df is None:
        bot_reply = "📂 Please upload a spending CSV before I can do that analysis."
    elif intent == "greet":
        bot_reply = "👋 Hi there! I’m your Spending Assistant. How can I help you today?"
    elif intent == "predict":
        pred = predict_next_month_expense(df)
        bot_reply = f"📈 You’re likely to spend around **₹{pred}** next month."
    elif intent == "chart":
        bot_reply = "🧾 Here’s your spending breakdown:"
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
            plot_monthly_expenses_by_category(df)
        bot_reply = None  # already printed
    elif intent == "max_category":
        last_month = df["month"].max()
        top = (
            df[df["month"] == last_month]
            .groupby("category")["amount"]
            .sum()
            .idxmax()
        )
        bot_reply = f"📊 You spent the most on **{top}** last month."
    elif intent == "total_spent":
        total = df.groupby("month")["amount"].sum().iloc[-1]
        bot_reply = f"💰 You spent **₹{total:.2f}** last month."
    elif intent == "bye":
        bot_reply = "👋 Goodbye! Hope to see you again soon! Feel free to ask anything!"
    elif intent == "unknown":
        bot_reply = "🤖 Let me think…"
        # stream a thinking bubble first
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        bot_reply = get_gemini_response(user_query)
    else:
        bot_reply = "🤖 Sorry, I didn't understand that. Could you rephrase?"

    # ────────── Add assistant response to history ─────────
    if bot_reply:
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
