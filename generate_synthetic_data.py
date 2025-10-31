import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_synthetic_financial_data():
    """Generate realistic synthetic financial data for 12 months with positive net income"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Base income (monthly) - increased to ensure positive net income
    base_income = 85000
    
    # Generate 12 months of data
    months = []
    for i in range(12):
        date = datetime(2024, 1, 1) + timedelta(days=30*i)
        months.append(date.strftime('%Y-%m'))
    
    data = []
    
    for month in months:
        # Income with some variation (always positive)
        income = max(80000, base_income + np.random.normal(0, 3000))
        
        # Fixed expenses (rent, utilities, etc.) - controlled to ensure positive net income
        rent = 25000
        utilities = max(4000, 5000 + np.random.normal(0, 300))
        insurance = 3000
        loan_payments = 8000
        
        # Variable expenses - controlled amounts
        groceries = max(10000, 12000 + np.random.normal(0, 1000))
        transportation = max(3000, 4000 + np.random.normal(0, 300))
        entertainment = max(5000, 6000 + np.random.normal(0, 800))
        healthcare = max(1500, 2000 + np.random.normal(0, 300))
        shopping = max(4000, 5000 + np.random.normal(0, 600))
        dining_out = max(3000, 4000 + np.random.normal(0, 500))
        subscriptions = 2000
        
        # Calculate total expenses
        total_expenses = (rent + utilities + insurance + loan_payments + 
                         groceries + transportation + entertainment + 
                         healthcare + shopping + dining_out + subscriptions)
        
        # Ensure expenses are always less than income (with buffer)
        max_allowed_expenses = income * 0.75  # Max 75% of income
        if total_expenses > max_allowed_expenses:
            # Scale down expenses proportionally
            scale_factor = max_allowed_expenses / total_expenses
            rent *= scale_factor
            utilities *= scale_factor
            groceries *= scale_factor
            transportation *= scale_factor
            entertainment *= scale_factor
            healthcare *= scale_factor
            shopping *= scale_factor
            dining_out *= scale_factor
            total_expenses = (rent + utilities + insurance + loan_payments + 
                             groceries + transportation + entertainment + 
                             healthcare + shopping + dining_out + subscriptions)
        
        # Calculate net income (guaranteed positive)
        net_income = income - total_expenses
        
        # Calculate savings (based on net income)
        savings = max(5000, net_income * 0.3 + np.random.normal(0, 1000))
        
        # Add some investment data
        investments = max(2000, savings * 0.6 + np.random.normal(0, 500))
        
        data.append({
            'Month': month,
            'Income': round(income, 2),
            'Rent': round(rent, 2),
            'Utilities': round(utilities, 2),
            'Insurance': round(insurance, 2),
            'Loan_Payments': round(loan_payments, 2),
            'Groceries': round(groceries, 2),
            'Transportation': round(transportation, 2),
            'Entertainment': round(entertainment, 2),
            'Healthcare': round(healthcare, 2),
            'Shopping': round(shopping, 2),
            'Dining_Out': round(dining_out, 2),
            'Subscriptions': round(subscriptions, 2),
            'Savings': round(savings, 2),
            'Investments': round(investments, 2),
            'Total_Expenses': round(total_expenses, 2),
            'Net_Income': round(net_income, 2)
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate the data
    df = generate_synthetic_financial_data()
    
    # Save to CSV
    df.to_csv('financial_data.csv', index=False)
    print("Synthetic financial data generated and saved to 'financial_data.csv'")
    print(f"Data shape: {df.shape}")
    print("\nFirst few rows:")
    print(df.head())
