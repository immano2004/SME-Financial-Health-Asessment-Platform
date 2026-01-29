def calculate_metrics(df):

    revenue = df["Revenue"].sum()
    expense = df["Expense"].sum()
    loan = df["Loan"].mean()

    profit = revenue - expense
    profit_margin = (profit / revenue) * 100

    expense_ratio = (expense / revenue) * 100

    growth = ((df["Revenue"].iloc[-1] - df["Revenue"].iloc[0]) /
              df["Revenue"].iloc[0]) * 100

    working_capital = df["Receivable"].sum() - df["Payable"].sum()

    return {
        "Revenue": revenue,
        "Profit Margin": profit_margin,
        "Expense Ratio": expense_ratio,
        "Growth %": growth,
        "Avg Loan": loan,
        "Working Capital": working_capital
    }

