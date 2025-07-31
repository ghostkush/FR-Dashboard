import yfinance as yf
import pandas as pd
import json

# loading the list of companies from https://www.sec.gov/file/company-tickers
def read_company_list():
    with open('company_tickers.json', 'r') as file:
        company_data = json.load(file)
    return company_data

def get_company_name():
    company_data = read_company_list()
    company_names = [company['title'] for company in company_data.values()]
    return company_names

def get_company_ticker(name):
    company_data = read_company_list()
    ticker = [company['ticker'] for company in company_data.values() if company['title'] == name][0]
    return ticker

def get_year_list():
    years = list(range(2020, 2025))
    return years

def get_income_statement(ticker, year):
    income_statement = yf.Ticker(ticker).financials.filter(like=str(year)).transpose()
    if income_statement.empty:
        raise ValueError(f"No financial data found for {ticker} in {year}.")
    return income_statement

def get_balance_sheet(ticker, year):
    balance_sheet = yf.Ticker(ticker).balance_sheet.filter(like=str(year)).transpose()
    if balance_sheet.empty:
        raise ValueError(f"No balance sheet data found for {ticker} in {year}.")
    return balance_sheet

def filtered_income_statement(ticker, year):
    income_statement = get_income_statement(ticker, year)
    # Filter the income statement to include only relevant columns
    relevant_columns = [
        'Total Revenue',
        'Operating Revenue',
        'Cost Of Revenue',
        'Gross Profit',
        'Operating Expense',
        'Total Expenses',
        'Operating Income',
        'EBIT',
        'EBITDA',
        'Net Income',
        'Basic EPS'
    ]
    missing_columns = [col for col in relevant_columns if col not in income_statement.columns]
    filtered_statement = income_statement.reindex(columns=relevant_columns)
    for col in missing_columns:
        filtered_statement[col] = None
    return filtered_statement

def filtered_balance_sheet(ticker, year):
    balance_sheet = get_balance_sheet(ticker, year)
    # Filter the balance sheet to include only relevant columns
    relevant_columns = [
        'Total Assets',
        'Total Debt',
        'Current Assets',
        'Current Liabilities',
        'Cash And Cash Equivalents',
        # 'Short Term Investments',
        'Inventory',
        'Accounts Receivable',
        'Accounts Payable',
        'Retained Earnings',
        'Stockholders Equity',
        # 'Total Equity',
        # 'Total Liabilities',
        'Long Term Debt'
    ]
    missing_columns = [col for col in relevant_columns if col not in balance_sheet.columns]
    filtered_statement = balance_sheet.reindex(columns=relevant_columns)
    for col in missing_columns:
        filtered_statement[col] = None
    return filtered_statement