#contains the functions that calculate different financial ratios
import pandas as pd

class FinancialRatios:
    @staticmethod
    def calculate_current_ratio(balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Current Ratio"""
        # print(balance_sheet["Current Assets"].values)
        # print(balance_sheet["Current Liabilities"].values)
        if balance_sheet["Current Assets"].values == None or balance_sheet["Current Liabilities"].values == None:
            return None
        r = balance_sheet["Current Assets"].values / balance_sheet["Current Liabilities"].values
        # print(float(r))
        return float(r)
    
    @staticmethod
    def calculate_quick_ratio(balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Quick Ratio"""

        if balance_sheet["Current Assets"].values == None or balance_sheet["Current Liabilities"].values == None:
            return None
        elif balance_sheet["Inventory"].values == None:
            r = (balance_sheet["Current Assets"].values - 0)/ balance_sheet["Current Liabilities"].values
            return float(r)    
        # print(float(r))
        r = (balance_sheet["Current Assets"].values - balance_sheet["Inventory"].values) / balance_sheet["Current Liabilities"].values
        return float(r)
    
    @staticmethod
    def calculate_cash_ratio(balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Cash Ratio"""
        if balance_sheet["Cash And Cash Equivalents"].values == None or balance_sheet["Current Liabilities"].values == None:
            return None
        r = balance_sheet["Cash And Cash Equivalents"].values / balance_sheet["Current Liabilities"].values
        return float(r)
    
    @staticmethod
    def calculate_gross_profit_margin(income_statement: pd.DataFrame) -> pd.DataFrame:
        """Calculate Gross Profit Margin"""
        if income_statement["Total Revenue"].values == None:
            return None
        elif income_statement["Cost Of Revenue"].values == None:
            r = (income_statement["Total Revenue"].values - 0) / income_statement["Total Revenue"].values
            return float(r)
        r = (income_statement["Total Revenue"].values - income_statement["Cost Of Revenue"].values) / income_statement["Total Revenue"].values
        return float(r)
    
    @staticmethod
    def calculate_operating_margin(income_statement: pd.DataFrame) -> pd.DataFrame:
        """Calculate Operating Margin"""
        if income_statement["Total Revenue"].values == None:
            return None
        r = income_statement["Operating Income"].values / income_statement["Total Revenue"].values
        return float(r)
    
    @staticmethod
    def calculate_net_profit_margin(income_statement: pd.DataFrame) -> pd.DataFrame:
        """Calculate Net Profit Margin"""
        if income_statement["Total Revenue"].values == None:
            return None
        r = income_statement["Net Income"].values / income_statement["Total Revenue"].values
        return float(r)
    
    @staticmethod
    def calculate_return_on_assets(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Return on Assets"""
        if income_statement["Net Income"].values == None or balance_sheet["Total Assets"].values == None:
            return None
        r = income_statement["Net Income"].values / balance_sheet["Total Assets"].values
        return float(r)
    
    @staticmethod
    def calculate_return_on_equity(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Return on Equity"""
        if income_statement["Net Income"].values == None or balance_sheet["Stockholders Equity"].values == None:
            return None
        r = income_statement["Net Income"].values / balance_sheet["Stockholders Equity"].values
        return float(r)
    
    @staticmethod
    def calculate_return_on_investment(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Return on Investment"""
        if income_statement["Net Income"].values == None or balance_sheet["Total Assets"].values == None:
            return None
        r = income_statement["Net Income"].values / (balance_sheet["Total Assets"].values - balance_sheet["Current Liabilities"].values)
        return float(r)
    
    # check these functions for correctness
    @staticmethod
    def calculate_total_debt_ratio(balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Total Debt Ratio"""
        if balance_sheet["Total Assets"].values == None:
            return None
        r = (balance_sheet["Total Assets"].values - balance_sheet["Stockholders Equity"].values) / balance_sheet["Total Assets"].values
        return float(r)
    
    @staticmethod
    def calculate_debt_to_equity_ratio(balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Debt to Equity Ratio"""
        if balance_sheet["Stockholders Equity"].values == None:
            return None
        r = balance_sheet["Total Debt"].values / balance_sheet["Stockholders Equity"].values
        return float(r)
    
    @staticmethod
    def calculate_equity_multiplier(balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """Calculate Equity Multiplier"""
        if balance_sheet["Stockholders Equity"].values == None:
            return None
        r = balance_sheet["Total Assets"].values / balance_sheet["Stockholders Equity"].values
        return float(r)