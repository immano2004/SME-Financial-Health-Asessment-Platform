"""
Data Validation Module
Validates input data and ensures data quality
"""

def validate_financial_data(df):
    """
    Validates uploaded financial data for completeness and accuracy
    """
    validation_report = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "data_quality_score": 100
    }
    
    # Check for empty dataframe
    if df is None or df.empty:
        validation_report["is_valid"] = False
        validation_report["errors"].append("Uploaded file is empty")
        return validation_report
    
    # Required columns
    required_columns = ["Date", "Revenue", "Expense"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        validation_report["errors"].append(f"Missing required columns: {', '.join(missing_columns)}")
        validation_report["is_valid"] = False
    
    # Data type validation
    for col in ["Revenue", "Expense"]:
        if col in df.columns:
            try:
                pd.to_numeric(df[col], errors='coerce')
                non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna() & df[col].notna()]
                if len(non_numeric) > 0:
                    validation_report["warnings"].append(f"{col} column contains non-numeric values: {len(non_numeric)} rows")
                    validation_report["data_quality_score"] -= 10
            except:
                validation_report["errors"].append(f"{col} column validation failed")
    
    # Check for negative values
    for col in ["Revenue", "Expense"]:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation_report["warnings"].append(f"{col} has {negative_count} negative values - please verify")
                validation_report["data_quality_score"] -= 5
    
    # Check for revenue > expense (basic sanity check)
    if "Revenue" in df.columns and "Expense" in df.columns:
        loss_months = (df["Revenue"] < df["Expense"]).sum()
        if loss_months > len(df) * 0.5:
            validation_report["warnings"].append(f"Business shows loss in {loss_months} out of {len(df)} months")
    
    # Check date format
    if "Date" in df.columns:
        try:
            pd.to_datetime(df["Date"])
        except:
            validation_report["warnings"].append("Date column format may be incorrect")
            validation_report["data_quality_score"] -= 5
    
    # Check minimum data points
    if len(df) < 3:
        validation_report["warnings"].append("Minimum 3 months of data recommended for accurate analysis")
        validation_report["data_quality_score"] -= 20
    
    return validation_report


def validate_user_input(business_name, industry, revenue, pan):
    """
    Validates user input data
    """
    validation = {
        "is_valid": True,
        "errors": []
    }
    
    # Business name validation
    if not business_name or len(business_name) < 2:
        validation["errors"].append("Business name must be at least 2 characters")
        validation["is_valid"] = False
    
    # Industry validation
    valid_industries = ["Retail", "Manufacturing", "Services", "Agriculture", "E-commerce", "Logistics"]
    if industry not in valid_industries:
        validation["errors"].append(f"Industry must be one of: {', '.join(valid_industries)}")
        validation["is_valid"] = False
    
    # Revenue validation
    if revenue <= 0:
        validation["errors"].append("Revenue must be greater than 0")
        validation["is_valid"] = False
    
    # PAN validation (simplified)
    if pan and not validate_pan(pan):
        validation["errors"].append("Invalid PAN format")
        validation["is_valid"] = False
    
    return validation


def validate_pan(pan):
    """
    Validates PAN format (simplified)
    PAN format: AAAPL1234C
    """
    if not isinstance(pan, str) or len(pan) != 10:
        return False
    
    # First 5 characters should be letters
    if not pan[:5].isalpha():
        return False
    
    # 6th character is typically a digit (year)
    # 7-9 characters should be digits
    # 10th character should be a letter
    
    if not pan[5].isdigit() or not pan[6:9].isdigit() or not pan[9].isalpha():
        return False
    
    return True


def validate_gst_number(gst):
    """
    Validates GST number format
    GST format: 27AABCT1234C1Z0 (15 digits)
    """
    if not isinstance(gst, str) or len(gst) != 15:
        return False
    
    # First 2 characters are state code (numeric)
    if not gst[:2].isdigit():
        return False
    
    # Next 10 characters are PAN
    if not validate_pan(gst[2:12]):
        return False
    
    return True


def sanitize_financial_data(df):
    """
    Cleans and sanitizes financial data
    """
    df_clean = df.copy()
    
    # Remove rows with missing critical values
    df_clean = df_clean.dropna(subset=["Revenue", "Expense"])
    
    # Convert to numeric
    for col in ["Revenue", "Expense"]:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Replace negative values with absolute values (with warning)
    for col in ["Revenue", "Expense"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].abs()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Sort by date if available
    if "Date" in df_clean.columns:
        try:
            df_clean["Date"] = pd.to_datetime(df_clean["Date"])
            df_clean = df_clean.sort_values("Date")
        except:
            pass
    
    return df_clean


def check_outliers(df):
    """
    Identifies outliers in financial data
    """
    outliers = {
        "detected": False,
        "outlier_rows": [],
        "recommendations": []
    }
    
    for col in ["Revenue", "Expense"]:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_rows = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
            
            if outlier_rows:
                outliers["detected"] = True
                outliers["outlier_rows"].append({
                    "column": col,
                    "rows": outlier_rows,
                    "values": df.loc[outlier_rows, col].tolist()
                })
                outliers["recommendations"].append(f"Found {len(outlier_rows)} outliers in {col} column - verify these entries")
    
    return outliers


def get_data_quality_report(df):
    """
    Generates comprehensive data quality report
    """
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": len(df[df.duplicated()]),
        "date_range": f"{df['Date'].min()} to {df['Date'].max()}" if 'Date' in df.columns else "N/A",
        "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
        "quality_score": 100
    }
    
    # Reduce score for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        report["quality_score"] -= min(20, missing_count * 5)
    
    # Reduce score for duplicates
    if report["duplicate_rows"] > 0:
        report["quality_score"] -= min(10, report["duplicate_rows"] * 2)
    
    return report


import pandas as pd
