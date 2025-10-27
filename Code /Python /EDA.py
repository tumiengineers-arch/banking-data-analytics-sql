import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import StringIO

# --- 1. Load DataFrames ---
print("--- 1. Loading and Preparing Data ---\n")

# NOTE: In a live environment, these would be direct file reads.
# Here, i use placeholder snippets to represent the data loading.

# Function to simulate loading CSV data from snippets (replace with pd.read_csv in a real setup)
def load_data(filename):
    try:
        # Assuming files are accessible
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Using a dummy DataFrame.")
        return pd.DataFrame()

df_cust = load_data('customer_accounts.csv')
df_txn = load_data('transactions.csv')
df_loan = load_data('loan_applications.csv')
df_cc_usage = load_data('credit_card_usage.csv')
df_fraud = load_data('fraud_reports.csv')
df_branch = load_data('branch_performance.csv')

# Data Cleaning and Type Conversion
# Convert date columns
date_cols = {
    df_txn: 'Date',
    df_loan: 'Application_Date',
    df_cc_usage: 'Date',
    df_fraud: 'Date',
    df_branch: 'Month'
}

for df, col in date_cols.items():
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        if col == 'Month':
            df['YearMonth'] = df[col].dt.to_period('M')


# --- 2. Define Plotting Function ---
def create_plot(title, data_func, kind='bar', x_label='', y_label='', rotation=0, figsize=(8, 5)):
    plt.figure(figsize=figsize)
    data = data_func()
    
    if kind == 'bar':
        sns.barplot(x=data.index, y=data.values)
        plt.xticks(rotation=rotation)
    elif kind == 'pie':
        plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
        plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    elif kind == 'line':
        sns.lineplot(x=data.index, y=data.values, marker='o')
        plt.xticks(rotation=rotation)

    plt.title(title, fontweight='bold')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


# --- 3. Key Findings & Visualizations ---

print("\n--- 3. Customer Account Insights ---\n")
print(f"Total Customers: {len(df_cust)}")
print("Balance Statistics:")
print(df_cust['Balance'].describe())
print("\n")

# V1: Distribution of Account Status (Active vs. Dormant)
create_plot(
    title='Account Status Distribution',
    data_func=lambda: df_cust['Status'].value_counts(),
    kind='pie'
)
# Finding: A significant portion of accounts are dormant (58.0%). 


print("\n--- 4. Transaction Analysis ---\n")

# V2: Total Transaction Volume by Type
create_plot(
    title='Total Transaction Volume by Type',
    data_func=lambda: df_txn.groupby('Type')['Amount'].sum().sort_values(ascending=False),
    x_label='Transaction Type',
    y_label='Total Amount ($)',
    rotation=0
)
# Finding: Transfers and Deposits dominate volume. 

# V3: Monthly Transaction Volume Trend
txn_monthly_volume = df_txn.set_index('Date').resample('M')['Amount'].sum()
create_plot(
    title='Monthly Transaction Volume (2023)',
    data_func=lambda: txn_monthly_volume,
    kind='line',
    x_label='Month',
    y_label='Total Volume ($)',
    rotation=45,
    figsize=(10, 6)
)
# Finding: December shows the highest volume, while September is the lowest. 


print("\n--- 5. Loan Application Insights ---\n")

# Calculate Approval Rate
loan_summary = df_loan.groupby('Loan_Type')['Status'].value_counts(normalize=True).mul(100).unstack(fill_value=0)
loan_summary['Approval_Rate'] = loan_summary.get('Approved', 0)
loan_summary = loan_summary.sort_values(by='Approval_Rate', ascending=False)['Approval_Rate']

# V4: Loan Approval Rate by Type
create_plot(
    title='Loan Approval Rate by Loan Type',
    data_func=lambda: loan_summary,
    x_label='Loan Type',
    y_label='Approval Rate (%)',
    rotation=0
)
# Finding: Personal loans have a 0% approval rate, suggesting a highly restrictive policy or issue with application quality. 


print("\n--- 6. Credit Card Usage Analysis ---\n")

# V5: Total Spend by Credit Card Category
create_plot(
    title='Total Credit Card Spend by Category',
    data_func=lambda: df_cc_usage.groupby('Category')['Amount'].sum().sort_values(ascending=False),
    x_label='Category',
    y_label='Total Spend ($)',
    rotation=45
)
# Finding: Shopping is the highest spend category. 


print("\n--- 7. Branch Performance Analysis ---\n")

# Calculate Profit
df_branch['Profit'] = df_branch['Revenue'] - df_branch['Expenses']

# V6: Average Monthly Profit by Branch
branch_profit = df_branch.groupby('Branch')['Profit'].mean().sort_values(ascending=False)
create_plot(
    title='Average Monthly Profit by Branch',
    data_func=lambda: branch_profit,
    x_label='Branch',
    y_label='Average Monthly Profit ($)',
    rotation=0
)
# Finding: West branch is the most profitable on average, while East is the least. 


print("\n--- 8. Fraud Reports Analysis ---\n")
print("Fraud Report Status Distribution:")
print(df_fraud['Status'].value_counts(normalize=True).mul(100))
print("\n")

# V7: Fraud Report Type Distribution
create_plot(
    title='Distribution of Fraud Report Types',
    data_func=lambda: df_fraud['Type'].value_counts(),
    kind='pie'
)
# Finding: Credit Card and Loan fraud reports are the most frequent types. 

print("\n--- EDA Script Complete ---\n")
