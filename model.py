import requests
import yfinance as yf
import asyncio

def get_interest_expense(company):
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit=120&apikey=8d8d7b6df8c7889b80fee22328d2c0dd")
    data = response.json()
    interest_expense = data[0]["interestExpense"]
    return interest_expense


def get_total_debt(company):
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit=120&apikey=8d8d7b6df8c7889b80fee22328d2c0dd")
    data = response.json()
    total_debt = data[0]["totalDebt"]
    return total_debt


def get_target_debt(company):
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/ratios-ttm/{company}?apikey=8d8d7b6df8c7889b80fee22328d2c0dd")
    data = response.json()
    target_debt = data[0]["debtRatioTTM"]
    return target_debt


def get_DCF(company):
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{company}?apikey=8d8d7b6df8c7889b80fee22328d2c0dd")
    data = response.json()
    DCF = data[0]["dcf"]
    return DCF


def get_shares_outstanding(company):
    try:
        response = yf.Ticker(company)
        shares = response.info["sharesOutstanding"]
        return shares
    except:
        print("Not the response")


def enterprise_value(company):
    return (get_shares_outstanding(company)*get_DCF(company) + get_total_debt(company))


def purchase_price(company):
    ma_premium = 1.25
    return ma_premium * enterprise_value(company)


def financing_debt(percent_debt, company):
    return purchase_price(company) * percent_debt/100


def financing_cash(percent_cash, company):
    return purchase_price(company) * percent_cash/100


def forgone_interest(cash):
    risk_free_rate = 0.04
    return cash * risk_free_rate


def additional_interest_on_debt(debt):
    interest_rate = 0.05
    return debt * interest_rate


def get_income_growth_rate(company):
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/income-statement-growth/{company}?limit=40&apikey=8d8d7b6df8c7889b80fee22328d2c0dd")
    data = response.json()
    net_income_growth_rate = data[0]["growthNetIncome"]
    return net_income_growth_rate


def project_net_income(company):
    projected_net_income = {}
    net_income_growth_rate = get_income_growth_rate(company)
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit=120&apikey=8d8d7b6df8c7889b80fee22328d2c0dd")
    data = response.json()
    recent_net_income = data[0]["netIncome"]
    projected_net_income['2022'] = recent_net_income
    year = 2023
    for i in range(6):
        next_yr_income = projected_net_income[str(
            year - 1)] * (1 + net_income_growth_rate)
        projected_net_income[f'{year}'] = next_yr_income
        year += 1
    return projected_net_income


def combine_net_income(buyer_net_income, seller_net_income):
    combined_net_income = {x: buyer_net_income.get(
        x, 0) + seller_net_income.get(x, 0) for x in set(buyer_net_income).union(seller_net_income)}
    myKeys = list(combined_net_income.keys())
    myKeys.sort()
    final_combined_net_income = {i: combined_net_income[i] for i in myKeys}
    return final_combined_net_income


def pre_tax_minus_interest(combined_net_income, company):
    for i in combined_net_income:
        combined_net_income[i] -= additional_interest_on_debt(
            financing_debt(30, company))
        combined_net_income[i] -= forgone_interest(financing_cash(70, company))
    return combined_net_income


def post_tax_net_income(pre_tax_net_income):
    tax_rate = 0.25
    for i in pre_tax_net_income:
        pre_tax_net_income[i] *= (1 - tax_rate)
    return pre_tax_net_income


def price_per_share(company):
    return purchase_price(company) / get_shares_outstanding(company)


def additional_shares(percent_cash, company):
    # cash portion from financing_cash function, p_per_share from price_per_share function
    return financing_cash(percent_cash, company) / price_per_share(company)


def final_shares_outstanding(buyer, percent_cash, seller):
    return get_shares_outstanding(buyer) + additional_shares(percent_cash, seller)


def yearly_eps(buyer, seller, percent_cash):
    post_tax_earnings = post_tax_net_income(pre_tax_minus_interest(combine_net_income(
        project_net_income(buyer), project_net_income(seller)), seller))
    for i in post_tax_earnings:
        post_tax_earnings[i] /= final_shares_outstanding(
            buyer, percent_cash, seller)
    final_yearly_eps = post_tax_earnings
    # print(final_yearly_eps)
    return final_yearly_eps


def change_in_yearly_eps(yearly_eps):
    dict = {}
    for i in range(2023, 2029):
        value = (yearly_eps[str(i)] - yearly_eps[str(i-1)]) / \
            yearly_eps[str(i-1)]
        dict[f'{i}'] = round((value * 100), 1)
    print(dict)
    return dict


change_in_yearly_eps(yearly_eps('AAPL', 'MSFT', 70))
