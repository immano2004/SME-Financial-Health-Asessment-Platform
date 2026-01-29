import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go


from utlis.metrics import calculate_metrics
from utlis.scoring import health_score
from utlis.ai_advisor import get_advice
from utlis.report import generate_pdf
from utlis.tax_compliance import check_tax_compliance, get_tax_deductions, compliance_recommendations_by_language
from utlis.working_capital import analyze_working_capital, suggest_working_capital_products
from utlis.cost_optimization import analyze_cost_structure, get_cost_reduction_strategies
from utlis.creditworthiness import detailed_creditworthiness_assessment
from utlis.forecasting import forecast_financial_metrics, analyze_trends, project_scenarios
from utlis.products_recommender import recommend_financial_products
from utlis.data_validation import validate_financial_data, sanitize_financial_data
from utlis.security_compliance import ComplianceChecker, get_security_recommendations

# -------------------------------------------------
# LANGUAGE TRANSLATIONS
# -------------------------------------------------
translations = {
    "English": {
        "language": "Language",
        "title": "📊 SME Financial Health Assessment Tool",
        "upload_file": "Upload CSV or Excel",
        "select_industry": "Select Industry",
        "use_demo_data": "Use Demo Data",
        "demo_loaded": "Demo data loaded successfully",
        "data_loaded": "Data loaded successfully",
        "raw_data": "Raw Data",
        "metrics": "Metrics",
        "industry_benchmark": "Industry Benchmark",
        "industry_avg": "Industry Avg Margin",
        "your_margin": "Your Margin",
        "below_avg": "Below industry average",
        "above_avg": "Above industry average",
        "creditworthiness": "Creditworthiness",
        "eligible_loan": "Eligible: Working Capital Loan, MSME Term Loan",
        "eligible_credit": "Eligible: Small Credit Line",
        "high_risk_loan": "High Risk: Loan not recommended",
        "working_capital": "Working Capital Status",
        "healthy_wc": "Healthy working capital",
        "negative_wc": "Negative working capital — improve collections",
        "financial_health": "Financial Health Score",
        "business_health": "Business Health",
        "key_metrics": "Key Metrics",
        "revenue": "Revenue",
        "profit_margin": "Profit Margin %",
        "expense_ratio": "Expense Ratio %",
        "gst_estimate": "GST & Tax Estimate",
        "gst_liability": "Estimated GST Liability",
        "expense_breakdown": "Expense Breakdown",
        "profit": "Profit",
        "expenses": "Expenses",
        "revenue_vs_expense": "Revenue vs Expense Trend",
        "revenue_forecast": "Revenue Forecast (Simple Prediction)",
        "ai_advisor": "AI Financial Advisor",
        "generate_insights": "Generate Insights",
        "download_report": "Download Report",
        "download_pdf": "Download PDF Report",
        "pdf_generated": "PDF report generated and ready for download",
        "integrations": "Integrations",
        "connect_bank": "Connect Bank (Demo)",
        "bank_connected": "Bank connected successfully (Demo)",
        "transactions_synced": "Transactions synced",
        "import_gst": "Import GST Data (Demo)",
        "gst_imported": "GST data imported (Demo)",
        "gst_summary": "GST Summary",
        "investor_report": "Investor Financial Health Report",
        "secure": "Data processed locally • Secure • For demo purposes only",
        "healthy": "Business is financially healthy",
        "moderate_risk": "Moderate financial risk detected",
        "high_risk": "High financial risk detected",
        "required_columns": "Required columns (Date, Revenue, Expense) not found for chart"
    },
    "Hindi": {
        "language": "भाषा",
        "title": "📊 एसएमई वित्तीय स्वास्थ्य मूल्यांकन उपकरण",
        "upload_file": "CSV या Excel अपलोड करें",
        "select_industry": "उद्योग चुनें",
        "use_demo_data": "डेमो डेटा का उपयोग करें",
        "demo_loaded": "डेमो डेटा सफलतापूर्वक लोड हुआ",
        "data_loaded": "डेटा सफलतापूर्वक लोड हुआ",
        "raw_data": "कच्चा डेटा",
        "metrics": "मेट्रिक्स",
        "industry_benchmark": "उद्योग बेंचमार्क",
        "industry_avg": "उद्योग औसत मार्जिन",
        "your_margin": "आपका मार्जिन",
        "below_avg": "उद्योग औसत से नीचे",
        "above_avg": "उद्योग औसत से ऊपर",
        "creditworthiness": "साख",
        "eligible_loan": "पात्र: कार्यशील पूंजी ऋण, एमएसएमई टर्म ऋण",
        "eligible_credit": "पात्र: छोटा क्रेडिट लाइन",
        "high_risk_loan": "उच्च जोखिम: ऋण की सिफारिश नहीं की जाती",
        "working_capital": "कार्यशील पूंजी स्थिति",
        "healthy_wc": "स्वस्थ कार्यशील पूंजी",
        "negative_wc": "नकारात्मक कार्यशील पूंजी — संग्रह में सुधार करें",
        "financial_health": "वित्तीय स्वास्थ्य स्कोर",
        "business_health": "व्यावसायिक स्वास्थ्य",
        "key_metrics": "मुख्य मेट्रिक्स",
        "revenue": "राजस्व",
        "profit_margin": "लाभ मार्जिन %",
        "expense_ratio": "व्यय अनुपात %",
        "gst_estimate": "जीएसटी और कर अनुमान",
        "gst_liability": "अनुमानित जीएसटी देयता",
        "expense_breakdown": "व्यय का विभाजन",
        "profit": "लाभ",
        "expenses": "व्यय",
        "revenue_vs_expense": "राजस्व बनाम व्यय प्रवृत्ति",
        "revenue_forecast": "राजस्व पूर्वानुमान (सरल भविष्यवाणी)",
        "ai_advisor": "एआई वित्तीय सलाहकार",
        "generate_insights": "अंतर्दृष्टि उत्पन्न करें",
        "download_report": "रिपोर्ट डाउनलोड करें",
        "download_pdf": "पीडीएफ रिपोर्ट डाउनलोड करें",
        "pdf_generated": "पीडीएफ रिपोर्ट उत्पन्न और डाउनलोड के लिए तैयार",
        "integrations": "एकीकरण",
        "connect_bank": "बैंक कनेक्ट करें (डेमो)",
        "bank_connected": "बैंक सफलतापूर्वक कनेक्ट हो गया (डेमो)",
        "transactions_synced": "लेनदेन सिंक हो गया",
        "import_gst": "जीएसटी डेटा आयात करें (डेमो)",
        "gst_imported": "जीएसटी डेटा आयात किया गया (डेमो)",
        "gst_summary": "जीएसटी सारांश",
        "investor_report": "निवेशक वित्तीय स्वास्थ्य रिपोर्ट",
        "secure": "डेटा स्थानीय रूप से संसाधित • सुरक्षित • डेमो उद्देश्यों के लिए",
        "healthy": "व्यवसाय वित्तीय रूप से स्वस्थ है",
        "moderate_risk": "मध्यम वित्तीय जोखिम का पता चला",
        "high_risk": "उच्च वित्तीय जोखिम का पता चला",
        "required_columns": "आवश्यक स्तंभ (तारीख, राजस्व, व्यय) चार्ट के लिए नहीं मिले"
    },
    "Tamil": {
        "language": "மொழி",
        "title": "📊 எஸ்எমிஇ நிதி ஆரோக்கியம் மதிப்பீட்டு கருவி",
        "upload_file": "CSV அல்லது Excel பதிவேற்றவும்",
        "select_industry": "தொழிலைத் தேர்ந்தெடுக்கவும்",
        "use_demo_data": "டெமோ தரவைப் பயன்படுத்தவும்",
        "demo_loaded": "டெமோ தரவு வெற்றிகரமாக ஏற்றப்பட்டது",
        "data_loaded": "தரவு வெற்றிகரமாக ஏற்றப்பட்டது",
        "raw_data": "மூல தரவு",
        "metrics": "அளவீடுகள்",
        "industry_benchmark": "தொழில் சாராংசம்",
        "industry_avg": "தொழில் சராசரி விளிம்பு",
        "your_margin": "உங்கள் விளிம்பு",
        "below_avg": "தொழில் சராசரிக்கு கீழே",
        "above_avg": "தொழில் சராசரிக்கு மேல்",
        "creditworthiness": "கடன் மூল்যம்",
        "eligible_loan": "தகுதி: பணிநிலை பூंजி கடன், எம்எসএমஇ கால கடன்",
        "eligible_credit": "தகுதி: சிறிய கடன் வரிசை",
        "high_risk_loan": "உচ்च ஆபத்து: கடன் பரிந்துரைக்கப்படவில்லை",
        "working_capital": "பணிநிலை மூலதன நிலை",
        "healthy_wc": "ஆரோக்கியமான பணிநிலை மூலதனம்",
        "negative_wc": "எதிர்மறை பணிநிலை மூலதனம் — சேகரணை மேம்படுத்தவும்",
        "financial_health": "நிதி ஆரோக்கியம் மதிப்பீடு",
        "business_health": "ব্যবসায়িক ஆরோக்கியம்",
        "key_metrics": "முக்கிய அளவீடுகள்",
        "revenue": "வருவாய்",
        "profit_margin": "லாभ விளிம்பு %",
        "expense_ratio": "செலவு விகிதம் %",
        "gst_estimate": "GST மற்றும் வரி மதிப்பீடு",
        "gst_liability": "மதிப்பிடப்பட்ட GST பொறுப்பு",
        "expense_breakdown": "செலவு பிரிப்பு",
        "profit": "லாभ",
        "expenses": "செலவுகள்",
        "revenue_vs_expense": "வருவாய் மற்றும் செலவு போக்கு",
        "revenue_forecast": "வருவாய் முன்னறிவிப்பு (எளிய கணிப்பு)",
        "ai_advisor": "AI நிதி ஆலோசகர்",
        "generate_insights": "நுண்ணறிவு உருவாக்கவும்",
        "download_report": "அறிக்கை பதிவிறக்கவும்",
        "download_pdf": "PDF அறிக்கை பதிவிறக்கவும்",
        "pdf_generated": "PDF அறிக்கை உருவாக்கப்பட்டு பதிவிறக்கத்திற்குத் தயாரிக்கப்பட்டுள்ளது",
        "integrations": "ஒருங்கிணைப்புகள்",
        "connect_bank": "வங்கி இணைக்கவும் (டெமோ)",
        "bank_connected": "வங்கி வெற்றிகரமாக இணைக்கப்பட்டது (டெமோ)",
        "transactions_synced": "பரிவர்த்தனைகள் ஒத்திசைக்கப்பட்டுள்ளன",
        "import_gst": "GST தரவை இறக்குமதி செய்யவும் (டெமோ)",
        "gst_imported": "GST தரவு இறக்குமதி செய்யப்பட்டது (டெமோ)",
        "gst_summary": "GST சுருக்கம்",
        "investor_report": "முதலீட்டாளர் நிதி ஆரோக்கியம் அறிக்கை",
        "secure": "தரவு உள்நாட்டில் செயல்படுத்தப்பட்டது • பாதுகாப்பு • டெமோ நோக்கங்களுக்காக",
        "healthy": "ব්যবসায় আর্থিকভাবে সুস্থ",
        "moderate_risk": "মধ্যম আর্থিক ঝুঁকি সনাক্ত হয়েছে",
        "high_risk": "উচ্চ আর্থিক ঝুঁকি সনাক্ত হয়েছে",
        "required_columns": "প্রয়োজনীয় কলাম (তারিখ, রাজস্ব, ব্যয়) চার্টের জন্য পাওয়া যায়নি"
    }
}

# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------
st.set_page_config(page_title="SME Financial Health Tool", layout="wide")

# Language Selection at the top
col_lang1, col_lang2 = st.columns([1, 10])
with col_lang1:
    lang = st.selectbox("🌐", ["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)"])

# Map language code for translations
lang_code = "English" if lang == "English" else "Hindi" if "Hindi" in lang else "Tamil"
t = translations[lang_code]

st.title(t["title"])


# -------------------------------------------------
# SESSION STATE (CRITICAL FOR STREAMLIT)
# -------------------------------------------------
if "advice" not in st.session_state:
    st.session_state.advice = None

if "df" not in st.session_state:
    st.session_state.df = None


# -------------------------------------------------
# FILE INPUT
# -------------------------------------------------
file = st.file_uploader(t["upload_file"], type=["csv", "xlsx"])

# Industry selection
industries = {
    "English": ["Retail", "Manufacturing", "Services", "Agriculture", "E-commerce"],
    "Hindi": ["खुदरा", "विनिर्माण", "सेवाएं", "कृषि", "ई-कॉमर्स"],
    "Tamil": ["சில்பக", "உற்பादனம்", "சேவைகள்", "விவசாயம்", "ই-வணிகம்"]
}

industry = st.selectbox(t["select_industry"], industries[lang_code])

industry_avg = {
    "Retail": 12, "खुदरा": 12, "சில்பக": 12,
    "Manufacturing": 18, "विनिर्माण": 18, "உற்பादனம்": 18,
    "Services": 25, "सेवाएं": 25, "சேவைகள்": 25,
    "Agriculture": 10, "कृषि": 10, "விவசாயம்": 10,
    "E-commerce": 15, "ई-कॉमर्स": 15, "ई-வணிகம்": 15
}

col1, col2 = st.columns([1, 5])

with col1:
    if st.button(t["use_demo_data"]):
        demo_path = os.path.join(os.path.dirname(__file__), "demo.csv")
        st.session_state.df = pd.read_csv(demo_path)
        st.success(t["demo_loaded"])
        st.write(st.session_state.df.head())


# Load uploaded file
if file:
    if file.name.endswith(".csv"):
        st.session_state.df = pd.read_csv(file)
    else:
        st.session_state.df = pd.read_excel(file)


df = st.session_state.df

# (GST estimate and expense breakdown will be shown after metrics are calculated)
# -------------------------------------------------
# MAIN APP
# -------------------------------------------------
if df is not None:

    st.success(t["data_loaded"])

    # -----------------------
    # RAW DATA
    # -----------------------
    st.subheader(t["raw_data"])
    st.dataframe(df, use_container_width=True)


    # -----------------------
    # METRICS
    # -----------------------
    metrics = calculate_metrics(df)
    score = health_score(metrics)

    # -----------------------
    # INDUSTRY BENCHMARK & CREDITWORTHINESS
    # -----------------------
    avg = industry_avg.get(industry, None)
    if avg is not None:
        st.subheader(t["industry_benchmark"])
        st.write(f"{t['industry_avg']}: {avg}%")
        st.write(f"{t['your_margin']}: {metrics.get('Profit Margin', 0):.1f}%")

        if metrics.get("Profit Margin", 0) < avg:
            st.warning(t["below_avg"])
        else:
            st.success(t["above_avg"])

    st.subheader(t["creditworthiness"])
    if score > 75:
        st.success(t["eligible_loan"])
    elif score > 50:
        st.warning(t["eligible_credit"])
    else:
        st.error(t["high_risk_loan"])

    wc = metrics.get("Working Capital", 0)
    st.subheader(t["working_capital"])
    if wc > 0:
        st.success(f"{t['healthy_wc']}: {wc}")
    else:
        st.error(t["negative_wc"])


    # -----------------------
    # HEALTH SCORE + UI
    # -----------------------
    st.subheader(t["financial_health"])

    # Gauge chart
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': t["business_health"]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"}
            ]
        }
    ))

    st.plotly_chart(gauge_fig, use_container_width=True)

    color = "green" if score > 70 else "orange" if score > 40 else "red"
    st.markdown(f"# :{color}[{score}/100]")

    if score > 70:
        st.success(t["healthy"])
    elif score > 40:
        st.warning(t["moderate_risk"])
    else:
        st.error(t["high_risk"])

    # -----------------------
    # METRICS CARDS
    # -----------------------
    st.subheader(t["key_metrics"])

    c1, c2, c3 = st.columns(3)

    c1.metric(t["revenue"], f"{metrics['Revenue']:.0f}")
    c2.metric(t["profit_margin"], f"{metrics['Profit Margin']:.1f}")
    c3.metric(t["expense_ratio"], f"{metrics['Expense Ratio']:.1f}")

    # -----------------------
    # GST Estimate & Expense Breakdown
    # -----------------------
    try:
        gst = metrics.get("Revenue", 0) * 0.18
        st.subheader(t["gst_estimate"])
        st.write(f"{t['gst_liability']}: ₹{gst:.0f}")

        st.subheader(t["expense_breakdown"])
        if metrics.get("Revenue") is not None and metrics.get("Expense Ratio") is not None:
            fig = px.pie(
                values=[metrics["Revenue"] - metrics["Revenue"] * metrics["Expense Ratio"] / 100,
                        metrics["Revenue"] * metrics["Expense Ratio"] / 100],
                names=[t["profit"], t["expenses"]]
            )
            st.plotly_chart(fig)
        else:
            st.warning(t["required_columns"])
    except Exception:
        st.warning(t["required_columns"])

    # -----------------------
    # CHART
    # -----------------------
    st.subheader(t["revenue_vs_expense"])

    fig = px.line(df, x="Date", y=["Revenue", "Expense"]) if "Revenue" in df.columns and "Expense" in df.columns else None
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(t["required_columns"])

    # -----------------------
    # FORECAST CHART
    # -----------------------
    st.subheader(t["revenue_forecast"])
    try:
        if "Revenue" in df.columns:
            df["Forecast"] = df["Revenue"].rolling(2).mean()
            fig_forecast = px.line(df, x="Date", y=["Revenue", "Forecast"]) if "Date" in df.columns else None
            if fig_forecast is not None:
                st.plotly_chart(fig_forecast, use_container_width=True)
        else:
            st.warning(t["required_columns"])
    except Exception:
        st.warning(t["required_columns"])

    # =================================================
    # AI ADVISOR (session state)
    # =================================================
    st.subheader(t["ai_advisor"])

    if st.button(t["generate_insights"]):
        st.session_state.advice = get_advice(metrics)

    if st.session_state.advice:
        st.info(st.session_state.advice)

    # =================================================
    # PDF DOWNLOAD
    # =================================================
    st.subheader(t["download_report"])

    if st.button(t["download_pdf"]):
        filepath = generate_pdf(metrics, score)

        with open(filepath, "rb") as f:
            st.download_button(
                label=t["download_pdf"],
                data=f,
                file_name="financial_report.pdf",
                mime="application/pdf"
            )
        st.success(t["pdf_generated"])
    
    # Create tabs for advanced features
    st.markdown("---")
    st.subheader("🚀 Advanced Analytics & Features")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Tax Compliance",
        "Working Capital",
        "Cost Optimization",
        "Credit Risk",
        "Forecasting",
        "Products & Loans"
    ])
    
    with tab1:
        st.header("💰 Tax Compliance & Regulations")
        
        # Tax compliance check
        tax_compliance = check_tax_compliance(metrics, revenue=metrics.get("Revenue", 0), 
                                             expenses=metrics.get("Expense Ratio", 0) * metrics.get("Revenue", 0) / 100,
                                             industry=industry)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tax Compliance Status", tax_compliance["status"].upper())
            st.metric("Compliance Score", f"{tax_compliance['compliance_score']}/100")
        
        with col2:
            st.metric("GST Eligible", "Yes" if tax_compliance["gst_eligible"] else "No")
            st.metric("Income Tax Slab", tax_compliance["income_tax_slab"])
        
        if tax_compliance["issues"]:
            st.warning("⚠️ Compliance Issues Detected:")
            for issue in tax_compliance["issues"]:
                st.write(f"• {issue}")
        
        st.info("📋 Recommendations:")
        for rec in tax_compliance["recommendations"]:
            st.write(f"✓ {rec}")
        
        # Tax deductions
        st.subheader("Available Tax Deductions")
        deductions = get_tax_deductions(industry, metrics.get("Revenue", 0), metrics.get("Expense Ratio", 0) * metrics.get("Revenue", 0) / 100)
        
        deduction_df = pd.DataFrame([
            {"Category": k, "Amount": f"₹{v:.0f}"} 
            for k, v in deductions["deductions"].items()
        ])
        st.dataframe(deduction_df, use_container_width=True)
        
        st.metric("Total Available Deductions", f"₹{deductions['total_deductions']:.0f}")
        st.metric("Estimated Taxable Income", f"₹{deductions['estimated_taxable_income']:.0f}")
    
    with tab2:
        st.header("💧 Working Capital Optimization")
        
        # Working capital analysis
        wc_analysis = analyze_working_capital(df, metrics.get("Revenue", 0), 
                                            metrics.get("Expense Ratio", 0) * metrics.get("Revenue", 0) / 100)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Receivables Days", f"{wc_analysis['receivables_days']:.0f}")
        col2.metric("Inventory Days", f"{wc_analysis['inventory_days']:.0f}")
        col3.metric("Payables Days", f"{wc_analysis['payables_days']:.0f}")
        col4.metric("Cash Cycle", f"{wc_analysis['cash_conversion_cycle']:.0f} days")
        
        st.metric("WC Efficiency", wc_analysis["working_capital_efficiency"])
        
        if wc_analysis["recommendations"]:
            st.info("💡 Optimization Recommendations:")
            for rec in wc_analysis["recommendations"]:
                st.write(rec)
        
        # Suggested products
        st.subheader("💳 Recommended Financing Products")
        wc_products = suggest_working_capital_products(wc_analysis, metrics.get("Revenue", 0))
        
        for product in wc_products:
            with st.expander(f"📦 {product['name']}"):
                st.write(f"**Purpose:** {product['purpose']}")
                st.write(f"**Loan Amount:** {product['amount_range']}")
                st.write(f"**Tenor:** {product['tenor']}")
                st.write(f"**Ideal For:** {product['ideal_for']}")
    
    with tab3:
        st.header("📊 Cost Structure & Optimization")
        
        # Cost analysis
        cost_analysis = analyze_cost_structure(df, metrics.get("Revenue", 0), 
                                              metrics.get("Expense Ratio", 0) * metrics.get("Revenue", 0) / 100,
                                              industry)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Expense Ratio", f"{cost_analysis['current_expense_ratio']:.1f}%")
        col2.metric("Industry Benchmark", f"{cost_analysis['industry_benchmark']}%")
        col3.metric("Optimization Potential", f"{cost_analysis['optimization_potential']:.1f}%")
        
        st.metric("💰 Potential Annual Savings", f"₹{cost_analysis['potential_savings']:.0f}")
        
        # Cost categories breakdown
        st.subheader("💼 Expense Breakdown")
        cost_categories = cost_analysis["cost_categories"]
        
        fig_pie = px.pie(
            values=[v["amount"] for v in cost_categories.values()],
            names=list(cost_categories.keys()),
            title="Expense Distribution by Category"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Optimization opportunities
        if cost_analysis["optimization_opportunities"]:
            st.subheader("🎯 Optimization Opportunities")
            for opp in cost_analysis["optimization_opportunities"]:
                with st.expander(f"{opp['area']} - {opp['potential_reduction']} reduction"):
                    st.write(f"**Potential Savings:** {opp['savings']}")
                    st.write(f"**Action:** {opp['action']}")
        
        # Industry-specific strategies
        st.subheader("🔧 Cost Reduction Strategies")
        strategies = get_cost_reduction_strategies(industry, cost_categories)
        
        for category, strat_list in strategies.items():
            if category != "Industry Specific":
                with st.expander(f"**{category}** - {len(strat_list)} strategies"):
                    for i, strategy in enumerate(strat_list, 1):
                        st.write(f"{i}. {strategy}")
    
    with tab4:
        st.header("🎖️ Creditworthiness & Risk Assessment")
        
        # Detailed creditworthiness assessment
        credit_assessment = detailed_creditworthiness_assessment(metrics, score, industry, metrics.get("Revenue", 0))
        
        col1, col2 = st.columns(2)
        
        with col1:
            rating = credit_assessment["credit_rating"]
            st.metric("Credit Rating", rating["rating"])
            st.write(f"**{rating['description']}**")
            st.write(f"Approval Probability: {rating['loan_approval_probability']}")
        
        with col2:
            default_risk = credit_assessment["default_risk"]
            st.metric("Default Risk", default_risk["risk_level"])
            st.write(f"Default Probability: {default_risk['default_probability']}")
            st.write(f"{default_risk['interpretation']}")
        
        # Loan eligibility
        st.subheader("📋 Loan Eligibility Matrix")
        eligibility = credit_assessment["loan_eligibility"]
        
        eligibility_data = []
        for loan_type, details in eligibility.items():
            eligibility_data.append({
                "Loan Type": loan_type.replace("_", " ").title(),
                "Eligible": "✅ Yes" if details["eligible"] else "❌ No",
                "Amount": details["loan_amount"],
                "Tenure": details["tenor"]
            })
        
        st.dataframe(pd.DataFrame(eligibility_data), use_container_width=True)
        
        # Risk factors
        st.subheader("⚠️ Risk Factors")
        if credit_assessment["risk_factors"]:
            for risk in credit_assessment["risk_factors"]:
                severity_color = "🔴" if risk["severity"] == "High" else "🟡" if risk["severity"] == "Medium" else "🟢"
                with st.expander(f"{severity_color} {risk['factor']} ({risk['severity']})"):
                    st.write(f"**Impact:** {risk['impact']}")
                    st.write(f"**Mitigation:** {risk['mitigation']}")
        
        # Strengths
        st.subheader("✅ Financial Strengths")
        for strength in credit_assessment["strengths"]:
            st.write(f"✓ {strength}")
    
    with tab5:
        st.header("📈 Financial Forecasting & Trends")
        
        # Analyze trends
        trends = analyze_trends(df)
        
        st.subheader("📊 Historical Trends")
        col1, col2 = st.columns(2)
        
        if trends["revenue_trend"]:
            with col1:
                st.metric("Revenue Trend", trends["revenue_trend"]["trend"])
                st.write(f"Growth Rate: {trends['revenue_trend']['growth_rate']:.1f}%")
                st.write(f"Momentum: {trends['revenue_trend']['momentum']}")
        
        if trends["expense_trend"]:
            with col2:
                st.metric("Expense Trend", trends["expense_trend"]["trend"])
                st.write(f"Growth Rate: {trends['expense_trend']['growth_rate']:.1f}%")
                st.write(f"Momentum: {trends['expense_trend']['momentum']}")
        
        if trends["trend_analysis"]:
            st.info("📌 Trend Analysis:")
            for analysis in trends["trend_analysis"]:
                st.write(analysis)
        
        # Forecast scenarios
        st.subheader("🔮 12-Month Revenue Forecast")
        
        growth_rate = trends["revenue_trend"]["growth_rate"] if trends["revenue_trend"] else 10
        scenarios = project_scenarios(metrics.get("Revenue", 0), growth_rate, 
                                     metrics.get("Expense Ratio", 0), periods=12)
        
        # Create forecast chart
        months = [f"M{i}" for i in range(1, 13)]
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            y=[s["revenue"] for s in scenarios["base_case"]],
            name="Base Case",
            mode="lines+markers"
        ))
        fig_forecast.add_trace(go.Scatter(
            y=[s["revenue"] for s in scenarios["optimistic_case"]],
            name="Optimistic",
            mode="lines",
            line=dict(dash="dash")
        ))
        fig_forecast.add_trace(go.Scatter(
            y=[s["revenue"] for s in scenarios["pessimistic_case"]],
            name="Pessimistic",
            mode="lines",
            line=dict(dash="dash")
        ))
        
        fig_forecast.update_layout(title="Revenue Forecast Scenarios", hovermode="x unified")
        st.plotly_chart(fig_forecast, use_container_width=True)
    
    with tab6:
        st.header("💳 Recommended Financial Products")
        
        # Get product recommendations
        wc = metrics.get("Working Capital", 0)
        products = recommend_financial_products(score, metrics.get("Revenue", 0), industry, metrics, wc)
        
        # Immediate products
        if products["immediate_products"]:
            st.subheader("🎯 Immediate Financing Options")
            for product in products["immediate_products"]:
                with st.expander(f"📦 {product['product']} - {product['provider']}"):
                    st.write(f"**Loan Amount:** {product['expected_limit']}")
                    st.write("**Features:**")
                    for feature in product['features']:
                        st.write(f"• {feature}")
                    st.write(f"**Eligibility:** {product.get('eligibility', 'Not specified')}")
        
        # Growth products
        if products["growth_products"]:
            st.subheader("🚀 Growth & Expansion Products")
            for product in products["growth_products"]:
                with st.expander(f"📦 {product['product']}"):
                    st.write(f"**Provider:** {product['provider']}")
                    st.write(f"**Use Case:** {product['use_case']}")
                    st.write(f"**Amount:** {product['expected_limit']}")
                    st.write("**Features:**")
                    for feature in product['features']:
                        st.write(f"• {feature}")
        
        # Insurance products
        if products["insurance_products"]:
            st.subheader("🛡️ Insurance & Risk Management")
            for product in products["insurance_products"]:
                with st.expander(f"🛡️ {product['product']}"):
                    st.write(f"**Provider:** {product['provider']}")
                    st.write(f"**Coverage:** {product['coverage']}")
                    st.write(f"**Premium Range:** {product['premium_range']}")

st.subheader(t["integrations"])

# Bank button
if st.button(t["connect_bank"]):
    st.success(t["bank_connected"])
    st.info(t["transactions_synced"])

# GST button
if st.button(t["import_gst"]):
    st.success(t["gst_imported"])

    gst_df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar"],
        "GST Paid": [1800, 2100, 2400]
    })

    st.subheader(t["gst_summary"])
    st.dataframe(gst_df)

st.header(t["investor_report"])
st.markdown("---")
st.caption(t["secure"])
