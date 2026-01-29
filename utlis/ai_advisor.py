def get_advice(metrics):

    advice = []

    profit = metrics["Profit Margin"]
    expense = metrics["Expense Ratio"]
    revenue = metrics["Revenue"]

    # Profit analysis
    if profit < 10:
        advice.append("⚠ Low profit margin. Reduce costs or increase pricing.")
    elif profit > 25:
        advice.append("✅ Strong profit margin. Business is healthy.")

    # Expense analysis
    if expense > 70:
        advice.append("⚠ Expenses too high. Optimize operational spending.")

    # Revenue analysis
    if revenue < 10000:
        advice.append("⚠ Revenue is low. Focus on customer growth and sales.")
    else:
        advice.append("📈 Revenue trend looks stable.")

    advice.append("💡 Maintain working capital and monitor cash flow regularly.")

    return "\n\n".join(advice)


