"""
Advanced Financial Forecasting Module
Provides detailed financial projections and trend analysis
"""

import pandas as pd
import numpy as np

def forecast_financial_metrics(df, periods=12, method="linear"):
    """
    Forecasts future financial metrics
    """
    
    forecasts = {}
    
    # Extract numeric columns for forecasting
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        if col in ["Revenue", "Expense", "Profit"]:
            forecasts[col] = forecast_series(df[col].values, periods, method)
    
    return forecasts


def forecast_series(values, periods=12, method="linear"):
    """
    Forecasts a time series using specified method
    """
    
    if method == "linear":
        return linear_forecast(values, periods)
    elif method == "exponential":
        return exponential_forecast(values, periods)
    else:
        return moving_average_forecast(values, periods)


def linear_forecast(values, periods):
    """
    Linear trend forecasting using least squares
    """
    x = np.arange(len(values))
    y = values
    
    # Calculate trend line
    coefficients = np.polyfit(x, y, 1)
    trend = np.poly1d(coefficients)
    
    # Forecast future values
    future_x = np.arange(len(values), len(values) + periods)
    forecast_values = trend(future_x)
    
    return {
        "forecast": list(forecast_values),
        "trend_slope": coefficients[0],
        "growth_rate": (coefficients[0] / np.mean(values) * 100) if np.mean(values) != 0 else 0
    }


def exponential_forecast(values, periods):
    """
    Exponential growth forecasting
    """
    # Calculate growth rates
    growth_rates = []
    for i in range(1, len(values)):
        if values[i-1] != 0:
            growth_rates.append((values[i] - values[i-1]) / values[i-1])
    
    avg_growth_rate = np.mean(growth_rates) if growth_rates else 0.05
    
    # Forecast using exponential growth
    last_value = values[-1]
    forecast_values = [last_value * (1 + avg_growth_rate) ** i for i in range(1, periods + 1)]
    
    return {
        "forecast": forecast_values,
        "avg_growth_rate": avg_growth_rate * 100,
        "confidence": "Medium"
    }


def moving_average_forecast(values, periods):
    """
    Moving average forecasting
    """
    window = min(3, len(values) // 2)
    ma = np.mean(values[-window:]) if window > 0 else np.mean(values)
    
    # Forecast using average
    forecast_values = [ma] * periods
    
    return {
        "forecast": forecast_values,
        "average_value": ma,
        "confidence": "Low"
    }


def analyze_trends(df):
    """
    Analyzes financial trends over time
    """
    
    trends = {
        "revenue_trend": None,
        "expense_trend": None,
        "profit_trend": None,
        "trend_analysis": []
    }
    
    if "Revenue" in df.columns:
        revenue_values = df["Revenue"].values
        if len(revenue_values) > 1:
            growth_rate = ((revenue_values[-1] - revenue_values[0]) / revenue_values[0] * 100) if revenue_values[0] != 0 else 0
            trends["revenue_trend"] = {
                "growth_rate": growth_rate,
                "trend": "Increasing" if growth_rate > 5 else "Stable" if growth_rate > -5 else "Decreasing",
                "momentum": calculate_momentum(revenue_values)
            }
            
            if growth_rate > 0:
                trends["trend_analysis"].append(f"✅ Revenue growing at {growth_rate:.1f}% - positive momentum")
            else:
                trends["trend_analysis"].append(f"⚠ Revenue declining by {abs(growth_rate):.1f}% - needs attention")
    
    if "Expense" in df.columns:
        expense_values = df["Expense"].values
        if len(expense_values) > 1:
            growth_rate = ((expense_values[-1] - expense_values[0]) / expense_values[0] * 100) if expense_values[0] != 0 else 0
            trends["expense_trend"] = {
                "growth_rate": growth_rate,
                "trend": "Increasing" if growth_rate > 5 else "Stable" if growth_rate > -5 else "Decreasing",
                "momentum": calculate_momentum(expense_values)
            }
            
            if growth_rate > 0:
                trends["trend_analysis"].append(f"⚠ Expenses growing at {growth_rate:.1f}% - cost control needed")
            else:
                trends["trend_analysis"].append(f"✅ Expenses declining by {abs(growth_rate):.1f}% - good cost management")
    
    return trends


def calculate_momentum(values):
    """
    Calculates momentum of a series
    """
    if len(values) < 2:
        return "Insufficient data"
    
    recent_avg = np.mean(values[-3:]) if len(values) >= 3 else values[-1]
    earlier_avg = np.mean(values[:-3]) if len(values) > 3 else values[0]
    
    if earlier_avg != 0:
        momentum = ((recent_avg - earlier_avg) / earlier_avg * 100)
        return "Strong Positive" if momentum > 10 else "Positive" if momentum > 0 else "Stable" if momentum > -5 else "Negative"
    
    return "Cannot calculate"


def project_scenarios(revenue, growth_rate, expense_ratio, periods=12):
    """
    Projects best, base, and worst case scenarios
    """
    
    scenarios = {
        "base_case": [],
        "optimistic_case": [],
        "pessimistic_case": []
    }
    
    for i in range(1, periods + 1):
        # Base case: expected growth
        base_revenue = revenue * (1 + growth_rate / 100) ** i
        base_profit = base_revenue * (1 - expense_ratio / 100)
        scenarios["base_case"].append({
            "month": i,
            "revenue": base_revenue,
            "profit": base_profit,
            "margin": (base_profit / base_revenue * 100) if base_revenue > 0 else 0
        })
        
        # Optimistic: 1.5x growth
        optimistic_revenue = revenue * (1 + growth_rate * 1.5 / 100) ** i
        optimistic_profit = optimistic_revenue * (1 - expense_ratio / 100 * 0.9)
        scenarios["optimistic_case"].append({
            "month": i,
            "revenue": optimistic_revenue,
            "profit": optimistic_profit,
            "margin": (optimistic_profit / optimistic_revenue * 100) if optimistic_revenue > 0 else 0
        })
        
        # Pessimistic: 0.5x growth
        pessimistic_revenue = revenue * (1 + growth_rate * 0.5 / 100) ** i
        pessimistic_profit = pessimistic_revenue * (1 - expense_ratio / 100 * 1.1)
        scenarios["pessimistic_case"].append({
            "month": i,
            "revenue": pessimistic_revenue,
            "profit": pessimistic_profit,
            "margin": (pessimistic_profit / pessimistic_revenue * 100) if pessimistic_revenue > 0 else 0
        })
    
    return scenarios


def calculate_breakeven_point(fixed_costs, variable_cost_ratio):
    """
    Calculates breakeven revenue
    """
    
    contribution_margin = 1 - variable_cost_ratio
    
    if contribution_margin > 0:
        breakeven_revenue = fixed_costs / contribution_margin
        return {
            "breakeven_revenue": breakeven_revenue,
            "breakeven_units": "Not calculated without unit price",
            "safety_margin": "Safety margin not calculated without current revenue",
            "interpretation": f"You need to generate ₹{breakeven_revenue:.0f} revenue to break even"
        }
    else:
        return {
            "breakeven_revenue": "Cannot calculate - variable costs exceed 100%",
            "error": "Invalid cost structure"
        }
