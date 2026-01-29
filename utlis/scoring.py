def health_score(m):

    score = 0

    score += min(max(m["Profit Margin"], 0), 30)
    score += max(0, 30 - m["Expense Ratio"])
    score += min(max(m["Growth %"], 0), 20)
    score += 20 if m["Working Capital"] > 0 else 5

    return int(min(score, 100))

