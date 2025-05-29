import streamlit as st


def app_header():
    st.markdown("""
        <h1 style='text-align: center; color: #4B8BBE;'>
            💸 Money Expenditure Assistant
        </h1>
        <hr style="border: 1px solid #ccc;">
    """, unsafe_allow_html=True)


# def chatbot_message(text, sender="bot"):
#     if sender == "bot":
#         bubble_color = "#f1f0f0"
#         align = "left"
#     else:
#         bubble_color = "#dcf8c6"
#         align = "right"

#     st.markdown(f"""
#         <div style='background-color: {bubble_color};
#                     color: black;
#                     padding: 10px 15px;
#                     border-radius: 10px;
#                     margin: 8px;
#                     max-width: 70%;
#                     text-align: {align};
#                     float: {align};
#                     clear: both;'>
#             {text}
#         </div>
#     """, unsafe_allow_html=True)


# def section_title(title):
#     st.markdown(f"""
#         <h3 style='color: #333;'>{title}</h3>
#     """, unsafe_allow_html=True)
