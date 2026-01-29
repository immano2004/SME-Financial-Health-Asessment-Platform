"""
Tax Compliance Checker Module
Validates financial data against tax regulations and compliance requirements
"""

def check_tax_compliance(metrics, revenue, expenses, industry):
    """
    Checks tax compliance based on financial metrics
    Returns compliance status and recommendations
    """
    compliance_report = {
        "status": "compliant",
        "issues": [],
        "recommendations": [],
        "gst_eligible": False,
        "income_tax_slab": "Not Calculated",
        "compliance_score": 100
    }
    
    # GST Eligibility Check (India)
    if revenue > 4000000:  # 40 lakhs threshold for services
        compliance_report["gst_eligible"] = True
    elif revenue > 2000000 and industry in ["Manufacturing", "Services", "E-commerce"]:
        compliance_report["gst_eligible"] = True
    
    # Income Tax Calculation (India - simplified)
    if revenue > 5000000:
        compliance_report["income_tax_slab"] = "30%"
    elif revenue > 2500000:
        compliance_report["income_tax_slab"] = "25%"
    elif revenue > 1000000:
        compliance_report["income_tax_slab"] = "20%"
    else:
        compliance_report["income_tax_slab"] = "No tax (Below threshold)"
    
    # Expense Validation
    if expenses > revenue:
        compliance_report["issues"].append("Expenses exceed revenue - review accounting")
        compliance_report["status"] = "warning"
        compliance_report["compliance_score"] -= 20
    
    # Profit Margin Check
    profit_margin = ((revenue - expenses) / revenue * 100) if revenue > 0 else 0
    if profit_margin < 0:
        compliance_report["issues"].append("Negative profit margin - potential loss carryforward needed")
        compliance_report["recommendations"].append("File ITR with loss carryforward provisions")
        compliance_report["compliance_score"] -= 15
    
    # TDS Compliance
    if revenue > 3000000:
        compliance_report["recommendations"].append("Ensure TDS deduction and remittance on due date")
    
    # Audit Eligibility
    if revenue > 10000000:
        compliance_report["recommendations"].append("Statutory audit required as per Companies Act")
    
    # MSME Classification
    if revenue <= 5000000 and "Manufacturing" in industry:
        compliance_report["recommendations"].append("You qualify for MSME benefits - register on MSME portal")
    elif revenue <= 2500000 and industry not in ["Manufacturing"]:
        compliance_report["recommendations"].append("You qualify for MSME benefits - register on MSME portal")
    
    # Book Keeping Records
    compliance_report["recommendations"].append("Maintain proper books of accounts for minimum 6 years")
    compliance_report["recommendations"].append("File GSTR returns on time (monthly/quarterly)")
    
    return compliance_report


def get_tax_deductions(industry, revenue, expenses):
    """
    Identifies available tax deductions based on industry and business structure
    """
    deductions = {
        "operating_expenses": expenses,
        "depreciation": revenue * 0.05,  # Simplified: 5% of revenue
        "professional_fees": revenue * 0.02,
        "travel_expenses": revenue * 0.01,
        "utilities": revenue * 0.015,
        "business_promotion": revenue * 0.02,
        "insurance_premiums": revenue * 0.01,
        "bank_charges": 500,
        "interest_on_loans": 0,
    }
    
    if industry == "Manufacturing":
        deductions["raw_materials"] = expenses * 0.6
        deductions["power_fuel"] = expenses * 0.1
    elif industry == "Retail":
        deductions["rent"] = expenses * 0.15
        deductions["inventory_write_off"] = expenses * 0.05
    elif industry == "Agriculture":
        deductions["farm_inputs"] = expenses * 0.4
        deductions["agricultural_subsidies"] = 0
    elif industry == "E-commerce":
        deductions["platform_commissions"] = expenses * 0.1
        deductions["logistics"] = expenses * 0.15
        deductions["digital_marketing"] = expenses * 0.1
    
    total_deductions = sum(deductions.values())
    return {
        "deductions": deductions,
        "total_deductions": total_deductions,
        "estimated_taxable_income": max(0, revenue - total_deductions)
    }


def compliance_recommendations_by_language(lang="English"):
    """
    Returns compliance recommendations in specified language
    """
    recommendations = {
        "English": {
            "maintain_records": "Maintain proper financial records and GST invoices for 6 years",
            "file_returns": "File income tax returns and GST returns on time",
            "audit": "Conduct statutory audit if required by law",
            "bank_reconciliation": "Perform monthly bank reconciliation",
            "invoice_audit": "Keep duplicate copies of all invoices issued",
            "payroll": "Maintain accurate payroll records and file employee tax returns"
        },
        "Hindi": {
            "maintain_records": "6 साल के लिए उचित वित्तीय रिकॉर्ड और GST इनवॉइस रखें",
            "file_returns": "समय पर आयकर रिटर्न और GST रिटर्न दाखिल करें",
            "audit": "कानून द्वारा आवश्यक होने पर वैधानिक लेखा परीक्षा करें",
            "bank_reconciliation": "मासिक बैंक समन्वय करें",
            "invoice_audit": "जारी किए गए सभी इनवॉइस की डुप्लिकेट प्रतियां रखें",
            "payroll": "सटीक पेरोल रिकॉर्ड रखें और कर्मचारी कर रिटर्न दाखिल करें"
        },
        "Tamil": {
            "maintain_records": "6 ஆண்டுகளுக்கு சரியான நிதிய பதிவுகள் மற்றும் GST இன்வॉய்சுகளை வைத்திருங்கள்",
            "file_returns": "சரியான நேரத்தில் வருமான வரி வருமானம் மற்றும் GST வருமானம் தாக்கல் செய்யவும்",
            "audit": "சட்டத்தால் தேவைப்பட்டால் சட்டசபை தணிக்கை நடத்தவும்",
            "bank_reconciliation": "மாதாந்திர வங்கி சமநிலை செய்யவும்",
            "invoice_audit": "வெளியிடப்பட்ட அனைத்து ஏலாய்டுகளின் நகல் நகלைக் வைத்திருங்கள்",
            "payroll": "துல்லிய ஊதிய பதிவுகளைப் பராமரிக்கவும் மற்றும் ஊழியர் வரி வருமானம் தாக்கல் செய்யவும்"
        }
    }
    
    return recommendations.get(lang, recommendations["English"])
