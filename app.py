import streamlit as st
# import pandas as pd
import functions as fn
import ratios as rt

def main():
    
    # Function to reset the session state for financial statements and buttons
    def reset_financial_statements():
        st.session_state["financial_statements"] = {"income_statement": None, "balance_sheet": None}
        st.session_state["fist_button_enabled"] = False
        st.session_state["current_ratio"] = False  # Reset the checkbox state
        st.session_state["quick_ratio"] = False  # Reset the checkbox state
        st.session_state["cash_ratio"] = False  # Reset the checkbox state
        st.session_state["gross_profit_margin"] = False  # Reset the checkbox state
        st.session_state["operating_margin"] = False  # Reset the checkbox state
        st.session_state["net_profit_margin"] = False  # Reset the checkbox state
        st.session_state["return_on_assets"] = False  # Reset the checkbox state
        st.session_state["return_on_equity"] = False  # Reset the checkbox state
        st.session_state["return_on_investment"] = False # Reset the checkbox state
        st.session_state["total_debt_ratio"] = False  # Reset the checkbox state
        st.session_state["debt_to_equity_ratio"] = False  # Reset the checkbox state
        st.session_state["equity_multiplier"] = False  # Reset the checkbox state

    def reset_ratios():
        st.session_state["current_ratio"] = False
        st.session_state["quick_ratio"] = False
        st.session_state["cash_ratio"] = False
        st.session_state["gross_profit_margin"] = False
        st.session_state["operating_margin"] = False
        st.session_state["net_profit_margin"] = False
        st.session_state["return_on_assets"] = False
        st.session_state["return_on_equity"] = False
        st.session_state["return_on_investment"] = False
        st.session_state["total_debt_ratio"] = False
        st.session_state["debt_to_equity_ratio"] = False
        st.session_state["equity_multiplier"] = False


    with st.container(border=False):   
        st.set_page_config(page_title="Financial Ratio Dashboard", layout="wide")
        # Center align the title and description using HTML and st.markdown
        st.markdown(
            """
            <div style="text-align: center;">
                <h1>Financial Ratio Dashboard</h1>
                <p>This app allows you to view financial statements for different companies and years.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Select a company and year to get the financial data.")
        company_names = fn.get_company_name()
        selected_company_name = st.selectbox("Select a company:", company_names, on_change=reset_financial_statements)  # Reset session state when company is changed
        selected_company_ticker = fn.get_company_ticker(selected_company_name)
        year = st.selectbox("Select a year:", fn.get_year_list(), index=4, on_change=reset_financial_statements) # Default to the last year in the list
        # st.write("you selected:", year)

        # col1, col2, col3 = st.columns([1, 1, 1])

        # if "first_button_enabled" not in st.session_state:
        #     st.session_state["first_button_enabled"] = False
        if "financial_statements" not in st.session_state and "fist_button_enabled" not in st.session_state:
            st.session_state["financial_statements"] = {"income_statement": None, "balance_sheet": None}
            st.session_state["fist_button_enabled"] = False

    # if "fist_button_enabled" not in st.session_state:
    #     st.session_state["fist_button_enabled"] = False
        if st.button("Get Financial statements", key="first"):  # Only enable if no other button is pressed
            try:
                filtered_income_statement = fn.filtered_income_statement(selected_company_ticker, year)
                filtered_balance_sheet = fn.filtered_balance_sheet(selected_company_ticker, year)
                # st.write(f"**Income Statement for {selected_company_name} ({year})**")
                # st.dataframe(filtered_income_statement)
                # st.write(f"**Balance Sheet for {selected_company_name} ({year})**")
                # st.dataframe(filtered_balance_sheet)
                st.session_state["financial_statements"]["income_statement"] = filtered_income_statement
                st.session_state["financial_statements"]["balance_sheet"] = filtered_balance_sheet
                st.session_state["fist_button_enabled"] = True
            except ValueError as e:
                st.error(str(e))
        
        if st.session_state["financial_statements"]["income_statement"] is not None:
            st.write(f"**Income Statement for {selected_company_name} ({year})**")
            st.dataframe(st.session_state["financial_statements"]["income_statement"])

        if st.session_state["financial_statements"]["balance_sheet"] is not None:
            st.write(f"**Balance Sheet for {selected_company_name} ({year})**")
            st.dataframe(st.session_state["financial_statements"]["balance_sheet"])

        temp_df_1 = st.session_state["financial_statements"]["balance_sheet"] # This is the balance sheet
        temp_df_2 = st.session_state["financial_statements"]["income_statement"] # This is the income statement
    
    # with col3:
    #     st.button("Dummy Button", key="third")
    
    # if st.session_state["financial_statements"]["income_statement"] is not None:
    #     st.write(f"**Income Statement for {selected_company_name} ({year})**")
    #     st.dataframe(st.session_state["financial_statements"]["income_statement"])

    # if st.session_state["financial_statements"]["balance_sheet"] is not None:
    #     st.write(f"**Balance Sheet for {selected_company_name} ({year})**")
    #     st.dataframe(st.session_state["financial_statements"]["balance_sheet"])

    # temp_df_1 = st.session_state["financial_statements"]["balance_sheet"] # This is the balance sheet
    # temp_df_2 = st.session_state["financial_statements"]["income_statement"] # This is the income statement
        st.markdown(
            """
            <div style="text-align: center;">
            <h3>Financial Ratios</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Reset Ratios", key="reset_ratios", type="primary"):
            reset_ratios()

        subcol1, subcol2, subcol3 = st.columns([1, 1, 1])
        with subcol1:
            st.write("Profitability Ratios")
            #
            st.checkbox("Show Gross Profit Margin", value=False, key="gross_profit_margin", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("gross_profit_margin", True):
                try:
                    gross_profit_margin = rt.FinancialRatios.calculate_gross_profit_margin(temp_df_2)
                    if gross_profit_margin is not None:
                        st.write(f"Gross Profit Margin for {selected_company_name} ({year}): **{gross_profit_margin:.2f}**")
                    else:
                        st.write("Gross Profit Margin cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Gross Profit Margin: {str(e)}")
            st.checkbox("Show Operating Margin", value=False, key="operating_margin", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("operating_margin", True):
                try:
                    operating_margin = rt.FinancialRatios.calculate_operating_margin(temp_df_2)
                    if operating_margin is not None:
                        st.write(f"Operating Margin for {selected_company_name} ({year}): **{operating_margin:.2f}**")
                    else:
                        st.write("Operating Margin cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Operating Margin: {str(e)}")
            st.checkbox("Show Net Profit Margin", value=False, key="net_profit_margin", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("net_profit_margin", True):
                try:
                    net_profit_margin = rt.FinancialRatios.calculate_net_profit_margin(temp_df_2)
                    if net_profit_margin is not None:
                        st.write(f"Net Profit Margin for {selected_company_name} ({year}): **{net_profit_margin:.2f}**")
                    else:
                        st.write("Net Profit Margin cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Net Profit Margin: {str(e)}")
            st.checkbox("Show Return on Assets", value=False, key="return_on_assets", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("return_on_assets", True):
                try:
                    return_on_assets = rt.FinancialRatios.calculate_return_on_assets(temp_df_2, temp_df_1)
                    if return_on_assets is not None:
                        st.write(f"Return on Assets for {selected_company_name} ({year}): **{return_on_assets:.2f}**")
                    else:
                        st.write("Return on Assets cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Return on Assets: {str(e)}")
            st.checkbox("Show Return on Equity", value=False, key="return_on_equity", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("return_on_equity", True):
                try:
                    return_on_equity = rt.FinancialRatios.calculate_return_on_equity(temp_df_2, temp_df_1)
                    if return_on_equity is not None:
                        st.write(f"Return on Equity for {selected_company_name} ({year}): **{return_on_equity:.2f}**")
                    else:
                        st.write("Return on Equity cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Return on Equity: {str(e)}")
            st.checkbox("Show Return on Investment", value=False, key="return_on_investment", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("return_on_investment", True):
                try:
                    return_on_investment = rt.FinancialRatios.calculate_return_on_investment(temp_df_2, temp_df_1)
                    if return_on_investment is not None:
                        st.write(f"Return on Investment for {selected_company_name} ({year}): **{return_on_investment:.2f}**")
                    else:
                        st.write("Return on Investment cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Return on Investment: {str(e)}")
            
        with subcol2:
            st.write("Liquidity Ratios")
            st.checkbox("Show Current Ratio", value=False, key="current_ratio", disabled=not st.session_state["fist_button_enabled"])    
            if st.session_state.get("current_ratio", True):
                try:
                    current_ratio = rt.FinancialRatios.calculate_current_ratio(temp_df_1)
                    if current_ratio is not None:
                        st.write(f"**Current Ratio for {selected_company_name} ({year})**: {current_ratio:.2f}")
                    else:
                        st.write("Current Liabilities are zero, cannot calculate Current Ratio.")
                except Exception as e:
                    st.error(f"Error calculating Current Ratio: {str(e)}")
            st.checkbox("Show Quick Ratio", value=False, key="quick_ratio", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("quick_ratio", True):
                try:
                    quick_ratio = rt.FinancialRatios.calculate_quick_ratio(temp_df_1)
                    if quick_ratio is not None:
                        st.write(f"**Quick Ratio for {selected_company_name} ({year})**: {quick_ratio:.2f}")
                    else:
                        st.write("Quick Ratio cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Quick Ratio: {str(e)}")
            st.checkbox("Show Cash Ratio", value=False, key="cash_ratio", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("cash_ratio", True):
                try:
                    cash_ratio = rt.FinancialRatios.calculate_cash_ratio(temp_df_1)
                    if cash_ratio is not None:
                        st.write(f"**Cash Ratio for {selected_company_name} ({year})**: {cash_ratio:.2f}")
                    else:
                        st.write("Cash Ratio cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Cash Ratio: {str(e)}")
        with subcol3:
            st.write("Solvency Ratios")
            st.checkbox("Show Total Debt Ratio", value=False, key="total_debt_ratio", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("total_debt_ratio", True):
                try:
                    total_debt_ratio = rt.FinancialRatios.calculate_total_debt_ratio(temp_df_1)
                    if total_debt_ratio is not None:
                        st.write(f"**Total Debt Ratio for {selected_company_name} ({year})**: {total_debt_ratio:.2f}")
                    else:
                        st.write("Total Debt Ratio cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Total Debt Ratio: {str(e)}")

            st.checkbox("Show Debt to Equity Ratio", value=False, key="debt_to_equity_ratio", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("debt_to_equity_ratio", True):
                try:
                    debt_to_equity_ratio = rt.FinancialRatios.calculate_debt_to_equity_ratio(temp_df_1)
                    if debt_to_equity_ratio is not None:
                        st.write(f"**Debt to Equity Ratio for {selected_company_name} ({year})**: {debt_to_equity_ratio:.2f}")
                    else:
                        st.write("Debt to Equity Ratio cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Debt to Equity Ratio: {str(e)}")
            
            st.checkbox("Show Equity Multiplier", value=False, key="equity_multiplier", disabled=not st.session_state["fist_button_enabled"])
            if st.session_state.get("equity_multiplier", True): 
                try:
                    equity_multiplier = rt.FinancialRatios.calculate_equity_multiplier(temp_df_1)
                    if equity_multiplier is not None:
                        st.write(f"**Equity Multiplier for {selected_company_name} ({year})**: {equity_multiplier:.2f}")
                    else:
                        st.write("Equity Multiplier cannot be calculated due to missing data.")
                except Exception as e:
                    st.error(f"Error calculating Equity Multiplier: {str(e)}")
            



    with col2:
        st.warning("AI analysis features will be available soon!")
        st.button("Dummy Button", key="second")

    # if st.button("Get Income Statement"):
    #     try:
    #         #income_statement = fn.get_income_statement(selected_company_ticker, year)
    #         filtered_income_statement = fn.filtered_income_statement(selected_company_ticker, year)
    #         st.write(f"**Income Statement for {selected_company_name} ({year})**")
    #         st.dataframe(filtered_income_statement)
    #     except ValueError as e:
    #         st.error(str(e))
    
    # if st.button("Get Balance Sheet"):
    #     try:
    #         # balance_sheet = fn.get_balance_sheet(selected_company_ticker, year)
    #         filtered_balance_sheet = fn.filtered_balance_sheet(selected_company_ticker, year)
    #         st.write(f"**Balance Sheet for {selected_company_name} ({year})**")
    #         # st.dataframe(balance_sheet)
    #         st.dataframe(filtered_balance_sheet)
    #     except ValueError as e:
    #         st.error(str(e))

    



    # st.write(f"Ticker for {selected_company_name}: {selected_company_ticker}")



if __name__ == "__main__":
    main()
# To run this app, save it as app.py and run the command:
# streamlit run app.py
# Make sure you have Streamlit installed in your Python environment.