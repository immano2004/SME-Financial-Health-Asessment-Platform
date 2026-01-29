"""
Creditworthiness Analyzer Module
Detailed credit risk assessment and loan eligibility analysis
"""

def detailed_creditworthiness_assessment(metrics, score, industry, revenue):
    """
    Provides comprehensive creditworthiness assessment
    """
    
    assessment = {
        "overall_score": score,
        "credit_rating": assign_credit_rating(score),
        "default_risk": calculate_default_risk(metrics, score),
        "loan_eligibility": assess_loan_eligibility(score, metrics, revenue),
        "risk_factors": identify_risk_factors(metrics, industry),
        "strengths": identify_strengths(metrics),
        "areas_of_concern": identify_concerns(metrics)
    }
    
    return assessment


def assign_credit_rating(score):
    """
    Assigns credit rating based on health score
    Similar to CIBIL/credit rating scales
    """
    if score >= 85:
        return {
            "rating": "AAA",
            "description": "Excellent - Minimal Risk",
            "loan_approval_probability": "95%+",
            "recommended_interest_rate": "Current Market Rate - 2%"
        }
    elif score >= 75:
        return {
            "rating": "AA",
            "description": "Very Good - Low Risk",
            "loan_approval_probability": "85-95%",
            "recommended_interest_rate": "Current Market Rate - 1%"
        }
    elif score >= 65:
        return {
            "rating": "A",
            "description": "Good - Moderate Risk",
            "loan_approval_probability": "70-85%",
            "recommended_interest_rate": "Current Market Rate"
        }
    elif score >= 50:
        return {
            "rating": "BBB",
            "description": "Fair - Acceptable Risk",
            "loan_approval_probability": "50-70%",
            "recommended_interest_rate": "Current Market Rate + 1-2%"
        }
    else:
        return {
            "rating": "B",
            "description": "Poor - High Risk",
            "loan_approval_probability": "<50%",
            "recommended_interest_rate": "Current Market Rate + 3-5%"
        }


def calculate_default_risk(metrics, score):
    """
    Calculates probability of default based on metrics
    """
    default_probability = max(0, 100 - score * 1.2)  # Simplified calculation
    
    risk_level = "Low" if default_probability < 15 else "Medium" if default_probability < 35 else "High"
    
    return {
        "default_probability": f"{default_probability:.1f}%",
        "risk_level": risk_level,
        "interpretation": get_default_risk_interpretation(default_probability)
    }


def get_default_risk_interpretation(probability):
    """
    Provides interpretation of default risk probability
    """
    if probability < 5:
        return "Very low likelihood of default"
    elif probability < 15:
        return "Low likelihood of default - good credit profile"
    elif probability < 35:
        return "Moderate likelihood of default - monitor performance"
    elif probability < 60:
        return "High likelihood of default - significant risk"
    else:
        return "Critical risk - not recommended for lending"


def assess_loan_eligibility(score, metrics, revenue):
    """
    Assesses eligibility for different types of loans
    """
    
    eligibility = {
        "working_capital_loan": {
            "eligible": score > 40,
            "loan_amount": f"₹{revenue * 0.25:.0f} - ₹{revenue * 0.50:.0f}",
            "tenor": "12-36 months",
            "required_collateral": "None" if score > 60 else "50% of loan amount",
            "approval_probability": min(95, max(40, score * 1.1)) if score > 40 else "Not Eligible"
        },
        "term_loan": {
            "eligible": score > 50,
            "loan_amount": f"₹{revenue * 0.50:.0f} - ₹{revenue * 1.0:.0f}",
            "tenor": "36-60 months",
            "required_collateral": "100% of loan amount" if score < 65 else "50% of loan amount",
            "approval_probability": min(90, max(45, score * 1.0)) if score > 50 else "Not Eligible"
        },
        "overdraft_facility": {
            "eligible": score > 50,
            "loan_amount": f"₹{revenue * 0.10:.0f} - ₹{revenue * 0.25:.0f}",
            "tenor": "12 months (renewable)",
            "required_collateral": "None" if score > 70 else "25% of facility",
            "approval_probability": min(95, max(50, score * 1.05)) if score > 50 else "Not Eligible"
        },
        "equipment_finance": {
            "eligible": score > 45,
            "loan_amount": f"₹{revenue * 0.20:.0f} - ₹{revenue * 0.60:.0f}",
            "tenor": "24-60 months",
            "required_collateral": "Equipment as mortgage",
            "approval_probability": min(85, max(40, score * 0.95)) if score > 45 else "Not Eligible"
        },
        "invoice_discounting": {
            "eligible": score > 30,
            "loan_amount": f"₹{revenue * 0.20:.0f} - ₹{revenue * 0.70:.0f}",
            "tenor": "90-180 days",
            "required_collateral": "Invoices/Bills",
            "approval_probability": min(90, max(60, score * 0.9)) if score > 30 else "Not Eligible"
        }
    }
    
    return eligibility


def identify_risk_factors(metrics, industry):
    """
    Identifies key risk factors affecting creditworthiness
    """
    
    risk_factors = []
    
    # Profitability Risk
    profit_margin = metrics.get("Profit Margin", 0)
    if profit_margin < 5:
        risk_factors.append({
            "factor": "Low Profitability",
            "severity": "High",
            "impact": "Reduces debt servicing capacity",
            "mitigation": "Focus on cost control and revenue growth"
        })
    elif profit_margin < 10:
        risk_factors.append({
            "factor": "Below Average Profitability",
            "severity": "Medium",
            "impact": "Limited buffer for loan repayment",
            "mitigation": "Improve operational efficiency"
        })
    
    # Liquidity Risk
    working_capital = metrics.get("Working Capital", 0)
    if working_capital < 0:
        risk_factors.append({
            "factor": "Negative Working Capital",
            "severity": "High",
            "impact": "Potential liquidity crisis",
            "mitigation": "Improve collections and payment terms"
        })
    
    # Business Cycle Risk
    industry_risk = {
        "Agriculture": "High",
        "E-commerce": "Medium",
        "Manufacturing": "Medium",
        "Retail": "High",
        "Services": "Low",
        "Logistics": "Medium"
    }
    
    if industry in industry_risk:
        risk_factors.append({
            "factor": f"Industry Cyclicality ({industry})",
            "severity": industry_risk[industry],
            "impact": "Seasonal or economic cycle impacts",
            "mitigation": "Diversify revenue streams, maintain reserves"
        })
    
    return risk_factors


def identify_strengths(metrics):
    """
    Identifies financial strengths
    """
    
    strengths = []
    
    revenue = metrics.get("Revenue", 0)
    if revenue > 5000000:
        strengths.append("Large revenue base indicates scale and market presence")
    
    profit_margin = metrics.get("Profit Margin", 0)
    if profit_margin > 20:
        strengths.append("Strong profitability demonstrates operational efficiency")
    
    working_capital = metrics.get("Working Capital", 0)
    if working_capital > 0:
        strengths.append("Healthy working capital indicates good liquidity management")
    
    expense_ratio = metrics.get("Expense Ratio", 100)
    if expense_ratio < 60:
        strengths.append("Low expense ratio shows cost discipline")
    
    return strengths


def identify_concerns(metrics):
    """
    Identifies areas of concern in financial metrics
    """
    
    concerns = []
    
    profit_margin = metrics.get("Profit Margin", 0)
    if profit_margin < 10:
        concerns.append("Low profit margin limits debt servicing capacity")
    
    working_capital = metrics.get("Working Capital", 0)
    if working_capital < 0:
        concerns.append("Negative working capital poses liquidity risk")
    
    expense_ratio = metrics.get("Expense Ratio", 0)
    if expense_ratio > 80:
        concerns.append("High expense ratio leaves little margin for error")
    
    return concerns
