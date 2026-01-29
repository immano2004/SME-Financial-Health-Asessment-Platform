"""
Security & Data Protection Module
Handles encryption and secure data management
"""

import hashlib
import json
from datetime import datetime

class DataSecurityManager:
    """
    Manages encryption and secure data handling
    """
    
    @staticmethod
    def encrypt_sensitive_data(data, key="financial_health_platform"):
        """
        Simple encryption for sensitive data
        In production, use proper encryption libraries like cryptography
        """
        # Placeholder for actual encryption implementation
        # In production use AES-256 or similar
        return hashlib.sha256((str(data) + key).encode()).hexdigest()
    
    @staticmethod
    def hash_user_data(email, phone):
        """
        Create secure hash of user identification data
        """
        combined = f"{email}{phone}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    @staticmethod
    def create_audit_log(action, user_id, data_accessed, status="success"):
        """
        Creates audit log for compliance and security
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_id": user_id,
            "data_accessed": data_accessed,
            "status": status,
            "ip_address": "Tracked in production"
        }


class ComplianceChecker:
    """
    Ensures compliance with financial regulations
    """
    
    @staticmethod
    def check_rbi_compliance(entity_type, revenue):
        """
        Checks RBI compliance requirements for different entity types
        """
        compliance = {
            "entity_type": entity_type,
            "requirements": [],
            "compliant": True
        }
        
        if entity_type in ["Private Limited", "Public Limited", "Partnership"]:
            compliance["requirements"].extend([
                "RBI Registration (if applicable)",
                "Licensed Dealer in Foreign Exchange",
                "Know Your Customer (KYC) compliance",
                "Anti-Money Laundering (AML) compliance"
            ])
        
        if revenue > 10000000:
            compliance["requirements"].extend([
                "Independent audit required",
                "ROC filing mandatory",
                "Financial disclosure requirements"
            ])
        
        return compliance
    
    @staticmethod
    def check_ifc_compliance(entity_type):
        """
        Checks Income Financial Compliance
        """
        return {
            "entity_type": entity_type,
            "requirements": [
                "Maintain books of accounts",
                "File returns within due date",
                "Keep records for 6 years",
                "Section 44AB: Audit if turnover > 50L"
            ]
        }
    
    @staticmethod
    def check_gst_compliance(revenue, industry):
        """
        Checks GST compliance requirements
        """
        compliance = {
            "gst_required": revenue > 4000000 or (revenue > 2000000 and industry != "Services"),
            "requirements": [
                "GST Registration",
                "Monthly GSTR-1 filing",
                "Monthly GSTR-3B filing",
                "Quarterly GSTR-1 for composition scheme",
                "Maintain GST invoices for 6 years"
            ],
            "penalties_for_non_compliance": [
                "Late fee for non-filing: ₹100-500 per day",
                "Interest at 18% p.a. on tax due",
                "Prosecution under Section 122"
            ]
        }
        
        return compliance
    
    @staticmethod
    def check_data_protection(storage_location, encryption_level):
        """
        Verifies data protection compliance
        """
        return {
            "data_protection": {
                "gdpr_compliant": storage_location == "EU" or encryption_level == "AES-256",
                "india_data_protection": encryption_level in ["AES-256", "RSA-2048"],
                "pii_protection": True if encryption_level == "AES-256" else False,
                "backup_frequency": "Daily",
                "disaster_recovery": "Enabled"
            },
            "requirements": [
                "Personal data encrypted at rest and in transit",
                "Regular security audits",
                "Data retention policy implementation",
                "User consent for data usage",
                "Data breach notification procedure"
            ]
        }


def get_security_recommendations(lang="English"):
    """
    Provides security best practices by language
    """
    recommendations = {
        "English": {
            "password": "Use strong passwords (minimum 12 characters with special characters)",
            "two_factor": "Enable two-factor authentication for all accounts",
            "data_backup": "Regular backups of financial data (daily/weekly)",
            "access_control": "Restrict access to sensitive financial data",
            "updates": "Keep software and security patches updated",
            "antivirus": "Maintain active antivirus and malware protection",
            "audit_trail": "Enable and review audit logs regularly"
        },
        "Hindi": {
            "password": "मजबूत पासवर्ड का उपयोग करें (कम से कम 12 वर्ण विशेष वर्णों के साथ)",
            "two_factor": "सभी खातों के लिए दो-कारक प्रमाणीकरण सक्षम करें",
            "data_backup": "वित्तीय डेटा का नियमित बैकअप (दैनिक/साप्ताहिक)",
            "access_control": "संवेदनशील वित्तीय डेटा तक पहुंच प्रतिबंधित करें",
            "updates": "सॉफ्टवेयर और सुरक्षा पैच को अपडेट रखें",
            "antivirus": "सक्रिय एंटीवायरस और मैलवेयर सुरक्षा बनाए रखें",
            "audit_trail": "ऑडिट लॉग नियमित रूप से सक्षम और समीक्षा करें"
        },
        "Tamil": {
            "password": "வலுவான கடவுச்சொற்களைப் பயன்படுத்தவும் (குறைந்தபட்சம் 12 எழுத்துக்கள் சிறப்பு எழுத்துக்களுடன்)",
            "two_factor": "அனைத்து கணக்குகளுக்கும் இரண்டு-காரணி அங்கீகாரத்தை இயக்கவும்",
            "data_backup": "நிதிய தரவுவின் வழக்கமான காப்பு (தினசரி/வாராந்திரம்)",
            "access_control": "உணர்திறன்மிக்க நிதிய தரவுக்கான அணுகலை கட்டுப்படுத்தவும்",
            "updates": "மென்பொருள் மற்றும் பாதுகாப்பு திருத்தங்களை புதுப்பிக்கவும்",
            "antivirus": "செயல்பட்ட ஆண்டிவைரஸ் மற்றும் தீங்கு விளைவிக்கும் மென்பொருள் பாதுகாப்பு பராமரிக்கவும்",
            "audit_trail": "ऑडिट लॉगை வழக்கமாக இயக்கி மதிப்பாய்வு செய்யவும்"
        }
    }
    
    return recommendations.get(lang, recommendations["English"])


def generate_compliance_certificate(business_name, assessment_date, compliance_status):
    """
    Generates compliance certificate
    """
    return {
        "certificate_type": "Financial Health Assessment Certificate",
        "business_name": business_name,
        "assessment_date": assessment_date,
        "compliance_status": compliance_status,
        "valid_until": "Assessment valid for 12 months",
        "disclaimer": "This is an automated assessment and does not replace professional audit/compliance review",
        "issued_by": "Financial Health Assessment Platform"
    }
