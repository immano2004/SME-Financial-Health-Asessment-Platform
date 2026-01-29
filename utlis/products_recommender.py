"""
Financial Products Recommender Module
Suggests suitable financial products based on business profile
"""

def recommend_financial_products(score, revenue, industry, metrics, working_capital):
    """
    Recommends suitable financial products from banks and NBFCs
    """
    
    recommendations = {
        "immediate_products": [],
        "growth_products": [],
        "investment_products": [],
        "insurance_products": [],
        "advisory_products": []
    }
    
    # Based on creditworthiness score
    if score > 75:
        recommendations["immediate_products"].extend([
            {
                "product": "Premium Working Capital Loan",
                "provider": "HDFC Bank / ICICI Bank / Axis Bank",
                "features": ["Competitive rates (Current Market Rate - 1-2%)", "Quick approval", "Upto ₹1 Crore"],
                "eligibility": "Score > 75, Revenue > ₹50L",
                "expected_limit": f"₹{revenue * 0.50:.0f}"
            },
            {
                "product": "Business Term Loan",
                "provider": "SBI / HDFC Bank / ICICI Bank",
                "features": ["Fixed EMI", "Long tenor (36-60 months)", "Low interest rate"],
                "eligibility": "Score > 75, Revenue > ₹50L",
                "expected_limit": f"₹{revenue * 1.0:.0f}"
            }
        ])
    
    elif score > 60:
        recommendations["immediate_products"].extend([
            {
                "product": "Standard Working Capital Loan",
                "provider": "Yes Bank / HDFC Bank / Axis Bank",
                "features": ["Moderate rates", "Upto 12 months", "Quick disbursal"],
                "eligibility": "Score > 60, Revenue > ₹30L",
                "expected_limit": f"₹{revenue * 0.40:.0f}"
            },
            {
                "product": "Business Overdraft",
                "provider": "SBI / HDFC Bank / ICICI Bank",
                "features": ["Flexible", "No pre-payment charges", "Interest on daily balance"],
                "eligibility": "Score > 60, Revenue > ₹25L",
                "expected_limit": f"₹{revenue * 0.25:.0f}"
            }
        ])
    
    else:
        recommendations["immediate_products"].extend([
            {
                "product": "Micro Business Loan",
                "provider": "MUDRA / Fintech Companies",
                "features": ["Quick approval", "Flexible repayment", "Lower eligibility"],
                "eligibility": "Score > 40",
                "expected_limit": f"₹{revenue * 0.25:.0f}"
            }
        ])
    
    # Growth products
    if revenue > 5000000:
        recommendations["growth_products"].extend([
            {
                "product": "Asset Financing",
                "provider": "HDFC Bank / Axis Bank / ICICI Bank",
                "features": ["For machinery/equipment", "Long tenor", "Competitive rates"],
                "use_case": "Capex investments",
                "expected_limit": f"₹{revenue * 0.60:.0f}"
            },
            {
                "product": "Venture Debt",
                "provider": "Venture Debt Funds",
                "features": ["For scaling businesses", "Equity-like returns", "Growth focus"],
                "use_case": "Rapid expansion",
                "expected_limit": f"₹{revenue * 0.50:.0f}"
            }
        ])
    
    # Based on working capital analysis
    if working_capital < 0 or (metrics.get("Working Capital", 0) < revenue * 0.10):
        recommendations["immediate_products"].append({
            "product": "Invoice Discounting / Bill Discounting",
            "provider": "TradeFin Platforms / NBFC",
            "features": ["Convert receivables to cash", "Fast approval", "Flexible tenure"],
            "use_case": "Improve cash flow",
            "expected_limit": f"₹{revenue * 0.50:.0f}"
        })
    
    # Investment products
    if score > 50 and revenue > 2500000:
        recommendations["investment_products"].extend([
            {
                "product": "Sweep Account",
                "provider": "HDFC Bank / ICICI Bank / Axis Bank",
                "features": ["Earn interest on surplus funds", "Auto sweep", "High liquidity"],
                "benefit": "Optimize idle cash"
            },
            {
                "product": "Merchant Discount Rate Optimization",
                "provider": "Payment Gateway Providers",
                "features": ["Negotiate lower MDR", "Volume-based discounts", "Custom solutions"],
                "benefit": f"Save ₹{revenue * 0.02:.0f} annually (est.)"
            }
        ])
    
    # Insurance products
    recommendations["insurance_products"].extend([
        {
            "product": "Business Interruption Insurance",
            "provider": "HDFC General / ICICI Lombard",
            "coverage": "Loss due to operational disruptions",
            "premium_range": f"₹{revenue * 0.002:.0f} - ₹{revenue * 0.005:.0f} annually"
        },
        {
            "product": "Key Person Insurance",
            "provider": "LIC / HDFC Life / Max Life",
            "coverage": "Financial protection if key business person is incapacitated",
            "premium_range": f"₹{revenue * 0.001:.0f} - ₹{revenue * 0.003:.0f} annually"
        },
        {
            "product": "Cyber Insurance",
            "provider": "HDFC Ergo / Bajaj Allianz",
            "coverage": "Protection against cyber threats and data breaches",
            "premium_range": f"₹{revenue * 0.001:.0f} - ₹{revenue * 0.002:.0f} annually"
        }
    ])
    
    # Advisory products
    recommendations["advisory_products"].extend([
        {
            "service": "Financial Planning & Advisory",
            "provider": "Bank / NBFC / Advisory Firms",
            "benefits": ["Customized financial strategies", "Tax optimization", "Growth planning"]
        },
        {
            "service": "GST & Compliance Advisory",
            "provider": "CA Firms / Compliance Platforms",
            "benefits": ["Ensure regulatory compliance", "Optimize tax filing", "Audit support"]
        },
        {
            "service": "Working Capital Optimization",
            "provider": "Supply Chain Finance Companies",
            "benefits": ["Improve cash conversion cycle", "Better supplier terms", "Buyer financing"]
        }
    ])
    
    return recommendations


def recommend_by_industry(industry, score, revenue):
    """
    Provides industry-specific financial product recommendations
    """
    
    recommendations = {
        "Manufacturing": [
            "Asset Financing for machinery and equipment",
            "Supply Chain Financing from component suppliers",
            "Inventory Financing",
            "Trade Credit Lines",
            "Working Capital Loan (Higher limits available)"
        ],
        "Retail": [
            "Working Capital Loan",
            "Bill Discounting",
            "Inventory Financing",
            "Retail Finance Solutions",
            "Business Overdraft"
        ],
        "E-commerce": [
            "Marketplace Finance",
            "Seller Cash Advance",
            "Inventory Financing",
            "Logistics Finance",
            "Working Capital Loan"
        ],
        "Agriculture": [
            "Kisan Credit Card (KCC)",
            "Agricultural Term Loan",
            "Crop Insurance",
            "Warehouse Receipts Finance",
            "Commodity Financing"
        ],
        "Services": [
            "Professional Loan",
            "Project-based Financing",
            "Working Capital Loan",
            "Business Overdraft",
            "Invoice Discounting"
        ],
        "Logistics": [
            "Vehicle Finance",
            "Working Capital Loan",
            "Fuel Advance",
            "Trade Credit Line",
            "Equipment Finance"
        ]
    }
    
    return recommendations.get(industry, [])


def calculate_affordability(loan_amount, interest_rate, tenor_months):
    """
    Calculates EMI and affordability metrics
    """
    
    monthly_rate = interest_rate / 100 / 12
    
    if monthly_rate == 0:
        emi = loan_amount / tenor_months
    else:
        emi = loan_amount * (monthly_rate * (1 + monthly_rate) ** tenor_months) / ((1 + monthly_rate) ** tenor_months - 1)
    
    total_interest = (emi * tenor_months) - loan_amount
    total_amount = loan_amount + total_interest
    
    return {
        "monthly_emi": emi,
        "total_interest": total_interest,
        "total_amount_payable": total_amount,
        "interest_percentage": (total_interest / loan_amount * 100) if loan_amount > 0 else 0,
        "tenor_months": tenor_months,
        "tenor_years": tenor_months / 12
    }


def evaluate_loan_offers(offers):
    """
    Compares multiple loan offers and recommends the best
    """
    
    comparison = []
    
    for offer in offers:
        affordability = calculate_affordability(
            offer.get("loan_amount", 0),
            offer.get("interest_rate", 0),
            offer.get("tenor_months", 12)
        )
        
        comparison.append({
            "lender": offer.get("lender", "Unknown"),
            "loan_amount": offer.get("loan_amount", 0),
            "interest_rate": offer.get("interest_rate", 0),
            "monthly_emi": affordability["monthly_emi"],
            "total_interest": affordability["total_interest"],
            "total_cost": affordability["total_amount_payable"],
            "score": calculate_offer_score(affordability)
        })
    
    # Sort by score (lower is better if measured by cost)
    comparison_sorted = sorted(comparison, key=lambda x: x["total_cost"])
    
    return {
        "comparison": comparison_sorted,
        "best_offer": comparison_sorted[0] if comparison_sorted else None,
        "recommendation": f"Best offer from {comparison_sorted[0]['lender']}" if comparison_sorted else "No offers available"
    }


def calculate_offer_score(affordability):
    """
    Calculates a score for comparing offers (lower is better)
    """
    return affordability["total_cost"]
