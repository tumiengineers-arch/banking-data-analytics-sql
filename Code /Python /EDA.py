#import os
#for file in os.listdir():
#    if file.endswith('.csv'):
#        os.remove(file)
#print("All CSV files deleted.")


#from google.colab import files
#uploaded = files.upload()  # Select ALL your CSV files at once


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
df_cust = pd.read_csv('customer_accounts.csv')
df_txn = pd.read_csv('transactions.csv')
df_loan = pd.read_csv('loan_applications.csv')
df_cc_usage = pd.read_csv('credit_card_usage.csv')
df_fraud = pd.read_csv('fraud_reports.csv')
df_branch = pd.read_csv('branch_performance.csv')

# Convert date columns
df_txn['Date'] = pd.to_datetime(df_txn['Date'], errors='coerce')
df_loan['Application_Date'] = pd.to_datetime(df_loan['Application_Date'], errors='coerce')
df_cc_usage['Date'] = pd.to_datetime(df_cc_usage['Date'], errors='coerce')
df_fraud['Date'] = pd.to_datetime(df_fraud['Date'], errors='coerce')
df_branch['Month'] = pd.to_datetime(df_branch['Month'], errors='coerce')
df_branch['YearMonth'] = df_branch['Month'].dt.to_period('M')

# Plotting function
def create_plot(title, data_func, kind='bar', x_label='', y_label='', rotation=0, figsize=(8, 5)):
    data = data_func()
    if data.empty:
        print(f"Skipping plot: {title} (no data)")
        return
    plt.figure(figsize=figsize)
    if kind == 'bar':
        sns.barplot(x=data.index, y=data.values)
        plt.xticks(rotation=rotation)
    elif kind == 'pie':
        plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
        plt.axis('equal')
    elif kind == 'line':
        sns.lineplot(x=data.index, y=data.values, marker='o')
        plt.xticks(rotation=rotation)
    plt.title(title, fontweight='bold')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # --- Customer Account Insights ---
print("\n--- Customer Account Insights ---\n")
print(f"Total Customers: {len(df_cust)}")
print("Balance Statistics:")
print(df_cust['Balance'].describe())
create_plot('Account Status Distribution', lambda: df_cust['Status'].value_counts(), kind='pie')
sns.boxplot(x='Account_Type', y='Balance', data=df_cust)
plt.title('Account Balance Distribution by Type')
plt.show()

# --- Transaction Analysis ---
create_plot('Total Transaction Volume by Type', lambda: df_txn.groupby('Type')['Amount'].sum().sort_values(ascending=False))
txn_monthly_volume = df_txn.set_index('Date').resample('M')['Amount'].sum()
create_plot('Monthly Transaction Volume (2023)', lambda: txn_monthly_volume, kind='line', rotation=45, figsize=(10, 6))

# --- Loan Application Insights ---
loan_summary = df_loan.groupby('Loan_Type')['Status'].value_counts(normalize=True).mul(100).unstack(fill_value=0)
loan_summary['Approval_Rate'] = loan_summary.get('Approved', 0)
loan_summary = loan_summary.sort_values(by='Approval_Rate', ascending=False)['Approval_Rate']
create_plot('Loan Approval Rate by Loan Type', lambda: loan_summary)

# --- Credit Card Usage ---
create_plot('Total Credit Card Spend by Category', lambda: df_cc_usage.groupby('Category')['Amount'].sum().sort_values(ascending=False), rotation=45)
monthly_spend = df_cc_usage.set_index('Date').resample('M')['Amount'].sum()
create_plot('Monthly Credit Card Spend (2023)', lambda: monthly_spend, kind='line', rotation=45, figsize=(10, 6))

# --- Branch Performance ---
df_branch['Profit'] = df_branch['Revenue'] - df_branch['Expenses']
branch_profit = df_branch.groupby('Branch')['Profit'].mean().sort_values(ascending=False)
create_plot('Average Monthly Profit by Branch', lambda: branch_profit)

df_branch['YearMonth'] = df_branch['YearMonth'].astype(str)
sns.lineplot(x='YearMonth', y='Profit', hue='Branch', data=df_branch, marker='o')
plt.title('Monthly Profit Trend by Branch (2023)')
plt.xticks(rotation=45)
plt.show()


# --- Fraud Reports ---
print("\nFraud Report Status Distribution:")
print(df_fraud['Status'].value_counts(normalize=True).mul(100))
create_plot('Distribution of Fraud Report Types', lambda: df_fraud['Type'].value_counts(), kind='pie')
fraud_monthly_count = df_fraud.set_index('Date').resample('M')['Report_ID'].count()
create_plot('Monthly Fraud Report Count (2023)', lambda: fraud_monthly_count, kind='line', rotation=45, figsize=(10, 6))

print("\n--- EDA Complete ---\n")
