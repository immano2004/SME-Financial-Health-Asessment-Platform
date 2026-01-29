"""
Working Capital Optimizer Module
Analyzes and optimizes working capital management
"""

def analyze_working_capital(df, revenue, expenses):
    """
    Analyzes working capital efficiency and provides optimization strategies
    """
    
    # Calculate average receivables days (simplified)
    avg_receivables_days = 30  # Default assumption
    if "Receivables" in df.columns:
        avg_receivables = df["Receivables"].mean() if len(df) > 0 else 0
        avg_receivables_days = (avg_receivables / (revenue / 365)) if revenue > 0 else 30
    
    # Calculate average payables days
    avg_payables_days = 45  # Default assumption
    if "Payables" in df.columns:
        avg_payables = df["Payables"].mean() if len(df) > 0 else 0
        avg_payables_days = (avg_payables / (expenses / 365)) if expenses > 0 else 45
    
    # Calculate inventory days
    inventory_days = 60  # Default assumption
    if "Inventory" in df.columns:
        avg_inventory = df["Inventory"].mean() if len(df) > 0 else 0
        cogs = expenses * 0.6
        inventory_days = (avg_inventory / (cogs / 365)) if cogs > 0 else 60
    
    # Calculate Cash Conversion Cycle
    cash_conversion_cycle = avg_receivables_days + inventory_days - avg_payables_days
    
    analysis = {
        "receivables_days": round(avg_receivables_days, 2),
        "payables_days": round(avg_payables_days, 2),
        "inventory_days": round(inventory_days, 2),
        "cash_conversion_cycle": round(cash_conversion_cycle, 2),
        "working_capital_efficiency": "Good" if cash_conversion_cycle < 30 else "Moderate" if cash_conversion_cycle < 60 else "Poor",
        "optimization_potential": max(0, cash_conversion_cycle - 30),
        "recommendations": []
    }
    
    # Generate recommendations based on analysis
    if avg_receivables_days > 45:
        analysis["recommendations"].append(
            f"⚠ High receivables days ({avg_receivables_days:.0f}). "
            "Implement stricter credit policy and improve collection process."
        )
    
    if inventory_days > 60:
        analysis["recommendations"].append(
            f"⚠ High inventory days ({inventory_days:.0f}). "
            "Optimize inventory levels and reduce dead stock."
        )
    
    if avg_payables_days < 30:
        analysis["recommendations"].append(
            f"💡 Negotiate extended payment terms with suppliers "
            f"(currently {avg_payables_days:.0f} days)."
        )
    
    if cash_conversion_cycle > 60:
        analysis["recommendations"].append(
            "🔴 Poor cash conversion cycle. This ties up significant working capital. "
            "Consider working capital loans or supply chain financing."
        )
    else:
        analysis["recommendations"].append(
            "✅ Good working capital management maintaining healthy cash flow."
        )
    
    return analysis


def suggest_working_capital_products(analysis, revenue):
    """
    Recommends suitable working capital financing products
    """
    products = []
    
    if analysis["cash_conversion_cycle"] > 45:
        products.append({
            "name": "Working Capital Loan",
            "purpose": "Bridge cash gap between expenses and collections",
            "amount_range": f"₹{revenue * 0.25:.0f} - ₹{revenue * 0.50:.0f}",
            "tenor": "12-36 months",
            "ideal_for": "Businesses with high receivables days"
        })
    
    if analysis["receivables_days"] > 45:
        products.append({
            "name": "Invoice Discounting / Bill Discounting",
            "purpose": "Get immediate cash against outstanding invoices",
            "amount_range": f"₹{revenue * 0.30:.0f} - ₹{revenue * 0.70:.0f}",
            "tenor": "90-180 days",
            "ideal_for": "B2B businesses with long credit terms"
        })
    
    if analysis["inventory_days"] > 60:
        products.append({
            "name": "Inventory Financing",
            "purpose": "Optimize inventory holding and reduce carrying costs",
            "amount_range": f"₹{revenue * 0.15:.0f} - ₹{revenue * 0.40:.0f}",
            "tenor": "6-12 months",
            "ideal_for": "Retail and manufacturing businesses"
        })
    
    products.append({
        "name": "Trade Credit Line",
        "purpose": "Flexible revolving credit for operational needs",
        "amount_range": f"₹{revenue * 0.20:.0f} - ₹{revenue * 0.60:.0f}",
        "tenor": "12-24 months",
        "ideal_for": "All businesses needing flexible credit"
    })
    
    return products


def calculate_wc_optimization_impact(analysis):
    """
    Calculates potential impact of working capital optimization
    """
    improvement_potential = {
        "reduce_receivables_days": {
            "target": max(20, analysis["receivables_days"] - 15),
            "impact": "Accelerates cash inflow",
            "effort": "Medium"
        },
        "optimize_inventory": {
            "target": max(40, analysis["inventory_days"] - 20),
            "impact": "Reduces carrying costs and frees up cash",
            "effort": "High"
        },
        "extend_payables": {
            "target": analysis["payables_days"] + 15,
            "impact": "Improves cash outflow timing",
            "effort": "Low"
        }
    }
    
    return improvement_potential
