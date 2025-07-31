import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define companies to compare
companies = [
    {"ticker": "INTC", "name": "Intel Corporation"},
    {"ticker": "AMD", "name": "Advanced Micro Devices, Inc."}
]

# Function to fetch financial data from Yahoo Finance
def get_financials(ticker):
    stock = yf.Ticker(ticker)
    income_stmt = stock.financials.transpose()
    balance_sheet = stock.balance_sheet.transpose()
    return income_stmt, balance_sheet

# Function to calculate financial ratios
def get_ratios(df_income_filtered, df_balance_filtered, df_financial_ratios):
    # Calculate Profitablilty ratios
    df_financial_ratios["Gross Profit Margin"] = (df_income_filtered["Revenue"] - df_income_filtered["COGS"]) / df_income_filtered["Revenue"]
    df_financial_ratios["Operating Margin"] = df_income_filtered["Operating Income"] / df_income_filtered["Revenue"]
    df_financial_ratios["Net Profit Margin"] = df_income_filtered["Net Income"] / df_income_filtered["Revenue"]
    df_financial_ratios["Return on Assets"] = df_income_filtered["Net Income"] / df_balance_filtered["Total Assets"]
    df_financial_ratios["Return on Equity"] = df_income_filtered["Net Income"] / df_balance_filtered["Stockholders Equity"]
    df_financial_ratios["Return on Investment"] = df_income_filtered["Net Income"] / (df_balance_filtered["Total Assets"] - df_balance_filtered["Current Liabilities"])
    # Calculate Liquidity ratios
    df_financial_ratios["Current Ratio"] = df_balance_filtered["Current Assets"] / df_balance_filtered["Current Liabilities"]
    df_financial_ratios["Quick Ratio"] = (df_balance_filtered["Current Assets"] - df_balance_filtered["Inventory"]) / df_balance_filtered["Current Liabilities"]
    df_financial_ratios["Cash Ratio"] = df_balance_filtered["Cash & Cash Equivalents"] / df_balance_filtered["Current Liabilities"]
    # Calculate Solvency ratios
    df_financial_ratios["Debt to Assets/Debt Ratio"] = df_balance_filtered["Total Debt"] / df_balance_filtered["Total Assets"]
    df_financial_ratios["Debt to Equity"] = df_balance_filtered["Total Debt"] / df_balance_filtered["Stockholders Equity"]
    df_financial_ratios["Interest Coverage Ratio"] = df_income_filtered["EBIT"] / df_income_filtered["Interest Expense"]
    df_financial_ratios["Equity Ratio"] = df_balance_filtered["Stockholders Equity"] / df_balance_filtered["Total Assets"]

    return df_financial_ratios

# Fetch financial data for both companies
financial_data = {company["ticker"]: get_financials(company["ticker"]) for company in companies}

# Filter data for the year 2024
filtered_income_data = {}
filtered_balance_data = {}
for ticker, (income_stmt, balance_sheet) in financial_data.items():
    if '2024-12-31' in income_stmt.index:
        filtered_income_data[ticker] = income_stmt.loc['2024-12-31', ['Total Revenue', 'Cost Of Revenue', 'Operating Income', 'Net Income', 'EBIT', 'EBITDA', 'Gross Profit', 'Interest Expense']]
    if '2024-12-31' in balance_sheet.index:
        filtered_balance_data[ticker] = balance_sheet.loc['2024-12-31', ['Total Assets', 'Total Non Current Assets', 'Total Debt', 'Total Capitalization', 'Stockholders Equity', 'Accounts Payable','Accounts Receivable', 'Inventory', 'Cash And Cash Equivalents', 'Current Assets', 'Current Liabilities', 'Invested Capital', 'Long Term Debt', 'Working Capital']]

# Rename columns for clarity
df_income_filtered = pd.DataFrame(filtered_income_data).transpose()
df_income_filtered.columns = ['Revenue', 'COGS', 'Operating Income', 'Net Income', 'EBIT', 'EBITDA', 'Gross Profit', 'Interest Expense']

df_balance_filtered = pd.DataFrame(filtered_balance_data).transpose()
df_balance_filtered.columns = ['Total Assets', 'Total Non Current Assets', 'Total Debt', 'Total Captialization', 'Stockholders Equity', 'Accounts Payable','Accounts Receivable',	'Inventory', 'Cash & Cash Equivalents', 'Current Assets', 'Current Liabilities', 'Invested Capital', 'Long Term Debt', 'Working Capital']

df_financial_ratios = pd.DataFrame()

# Calculate financial ratios
df_financial_ratios = get_ratios(df_income_filtered, df_balance_filtered, df_financial_ratios)

# Export financial data to Excel
excel_path = "financial_data_2024.xlsx"
with pd.ExcelWriter(excel_path) as writer:
    df_income_filtered.to_excel(writer, sheet_name="Income Statement", index=True)
    df_balance_filtered.to_excel(writer, sheet_name="Balance Sheet", index=True)
    df_financial_ratios.to_excel(writer, sheet_name="Financial Ratios", index=True)

print(f"Income statements and balance sheets for 2024 saved to {excel_path}")

# Plot financial ratios
profitability_ratios = ["Gross Profit Margin", "Operating Margin", "Net Profit Margin", "Return on Assets", "Return on Equity", "Return on Investment"]
liquidity_ratios = ["Current Ratio", "Quick Ratio", "Cash Ratio"]
solvency_ratios = ["Debt to Assets/Debt Ratio", "Debt to Equity", "Interest Coverage Ratio", "Equity Ratio"]

# Create a figure with 3 subplots
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

# Bar Plot of Profitability Ratios
df_financial_ratios[profitability_ratios].plot(kind='bar', ax=axes[0])
axes[0].set_title('Profitability Ratios for 2024')
axes[0].set_xlabel('Company')
axes[0].set_ylabel('Ratio')
axes[0].legend(loc='best')

# Bar Plot of Liquidity Ratios
df_financial_ratios[liquidity_ratios].plot(kind='bar', ax=axes[1])
axes[1].set_title('Liquidity Ratios for 2024')
axes[1].set_xlabel('Company')
axes[1].set_ylabel('Ratio')
axes[1].legend(loc='best')

# Bar Plot of Solvency Ratios
df_financial_ratios[solvency_ratios].plot(kind='bar', ax=axes[2])
axes[2].set_title('Solvency Ratios for 2024')
axes[2].set_xlabel('Company')
axes[2].set_ylabel('Ratio')
axes[2].legend(loc='best')

plt.tight_layout()
plt.savefig("financial_ratios_2024.png")
plt.show()