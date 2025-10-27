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
