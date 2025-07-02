from .gemini_chat import get_gemini_response


def classify_query(query):
    query = query.lower()
    if "predict" in query or "next month" in query:
        return "predict"
    elif "most" in query or "where" in query:
        return "max_category"
    elif "chart" in query or "graph" in query:
        return "chart"
    elif "most" in query or "where" in query:
        return "max_category"
    elif "total" in query:
        return "total_spent"
    elif "bye" in query or "exit" in query:
        return "bye"
    elif "hi" in query or "hello" in query:
        return "greet"
    else:
        # Fallback to Gemini
        gemini_response = get_gemini_response(
            f"""
            A user asked: "{query}"

            Classify this question into one of these intents:
            - predict
            - chart
            - max_category
            - total_spent
            - bye
            - unknown  ← (use this if it's a general finance question, not data)

            Only reply with one intent keyword.
            """,
            mode="classify"
        )

        return gemini_response.strip().lower()
