def classify_query(query):
    query = query.lower()
    if "predict" in query or "next month" in query:
        return "predict"
    elif "chart" in query or "graph" in query:
        return "chart"
    elif "most" in query or "where" in query:
        return "max_category"
    elif "total" in query:
        return "total_spent"
    return "unknown"
