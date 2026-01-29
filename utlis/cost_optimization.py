"""
Cost Optimization Module
Identifies cost reduction opportunities and suggests optimization strategies
"""

import pandas as pd


# =====================================================
# MAIN ANALYSIS
# =====================================================
def analyze_cost_structure(df, revenue, expenses, industry):
    """
    Analyze cost structure and suggest optimization opportunities
    """

    expense_ratio = (expenses / revenue * 100) if revenue > 0 else 0

    # Industry benchmarks
    industry_benchmarks = {
        "Retail": 70,
        "Manufacturing": 75,
        "Services": 65,
        "E-commerce": 80,
        "Agriculture": 60,
        "Logistics": 75
    }

    benchmark = industry_benchmarks.get(industry, 70)

    analysis = {
        "current_expense_ratio": round(expense_ratio, 2),
        "industry_benchmark": benchmark,
        "optimization_potential": max(0, expense_ratio - benchmark),
        "potential_savings": max(0, (expense_ratio - benchmark) / 100 * revenue),
        "cost_categories": categorize_expenses(df, expenses),
        "optimization_opportunities": []
    }

    # =====================================================
    # OVERALL COST CHECK
    # =====================================================
    if expense_ratio > benchmark:
        surplus = expense_ratio - benchmark

        analysis["optimization_opportunities"].append({
            "area": "Overall Costs",
            "potential_reduction": f"{surplus:.1f}%",
            "savings": f"₹{analysis['potential_savings']:.0f}",
            "action": "Review all expense categories for optimization"
        })

    # =====================================================
    # PERSONNEL COST CHECK (FIXED BUG HERE)
    # =====================================================
    personnel_cost = 0

    if "Salaries" in df.columns:
        personnel_cost = df["Salaries"].mean()

    elif "Personnel" in df.columns:
        personnel_cost = df["Personnel"].mean()

    if personnel_cost > revenue * 0.30:
        analysis["optimization_opportunities"].append({
            "area": "Personnel Costs",
            "potential_reduction": "10-15%",
            "savings": f"₹{personnel_cost * 0.15:.0f}",
            "action": "Review staffing levels, automation, outsourcing"
        })

    return analysis


# =====================================================
# CATEGORIZE EXPENSES
# =====================================================
def categorize_expenses(df, total_expenses):

    categories = {
        "Personnel & Salaries": {"percentage": 30, "amount": total_expenses * 0.30},
        "Raw Materials/Inventory": {"percentage": 25, "amount": total_expenses * 0.25},
        "Rent & Utilities": {"percentage": 10, "amount": total_expenses * 0.10},
        "Logistics & Transportation": {"percentage": 10, "amount": total_expenses * 0.10},
        "Marketing & Advertising": {"percentage": 8, "amount": total_expenses * 0.08},
        "Maintenance & Repairs": {"percentage": 7, "amount": total_expenses * 0.07},
        "Miscellaneous": {"percentage": 10, "amount": total_expenses * 0.10}
    }

    return categories


# =====================================================
# COST REDUCTION STRATEGIES
# =====================================================
def get_cost_reduction_strategies(industry, expense_categories):

    strategies = {
        "Personnel & Salaries": [
            "Automate repetitive tasks",
            "Outsource non-core work",
            "Use freelancers",
            "Performance incentives"
        ],
        "Raw Materials/Inventory": [
            "Bulk purchase discounts",
            "Just-in-time inventory",
            "Remove slow-moving stock"
        ],
        "Marketing & Advertising": [
            "Focus on digital marketing",
            "Reduce traditional ads",
            "Track ROI strictly"
        ]
    }

    industry_specific = {
        "Manufacturing": ["Lean production", "Reduce scrap"],
        "Retail": ["Optimize inventory turnover"],
        "E-commerce": ["Reduce returns"],
        "Services": ["Increase billable utilization"]
    }

    combined = dict(strategies)

    if industry in industry_specific:
        combined["Industry Specific"] = industry_specific[industry]

    return combined


# =====================================================
# SAVINGS IMPACT
# =====================================================
def calculate_cost_savings_impact(savings_amount, revenue, industry):

    industry_margins = {
        "Retail": 12,
        "Manufacturing": 15,
        "Services": 25,
        "E-commerce": 8,
        "Agriculture": 18,
        "Logistics": 10
    }

    current_margin = industry_margins.get(industry, 15)

    profit_before = revenue * (current_margin / 100)
    profit_after = profit_before + savings_amount
    new_margin = (profit_after / revenue * 100)

    return {
        "savings_amount": savings_amount,
        "profit_improvement": f"₹{savings_amount:.0f}",
        "margin_improvement": f"{new_margin - current_margin:.2f}%",
        "new_profit_margin": f"{new_margin:.2f}%",
        "roi_percentage": f"{(savings_amount / revenue * 100):.2f}%"
    }
