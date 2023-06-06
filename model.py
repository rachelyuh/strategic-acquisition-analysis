import requests
import yfinance as yf

def get_free_cash_flow(company):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit=120&apikey=4975d0effdd49277f9f496ce27032830")
    data = response.json()
    free_cash_flow = []
    free_cash_flow.append(data[0]["freeCashFlow"])
    free_cash_flow.append(data[1]["freeCashFlow"])
    free_cash_flow.append(data[2]["freeCashFlow"])
    free_cash_flow.append(data[3]["freeCashFlow"])
    return free_cash_flow

def get_interest_expense(company):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit=120&apikey=4975d0effdd49277f9f496ce27032830")
    data = response.json()
    interest_expense = data[0]["interestExpense"]
    return interest_expense

def get_total_debt(company):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit=120&apikey=4975d0effdd49277f9f496ce27032830")
    data = response.json()
    total_debt = data[0]["totalDebt"]
    return total_debt

def cost_of_debt(company):
    return get_interest_expense(company)/get_total_debt(company)

def get_target_debt(company):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{company}?apikey=4975d0effdd49277f9f496ce27032830")
    data = response.json()
    target_debt = data[0]["debtRatioTTM"]
    return target_debt

def get_DCF(company):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{company}?apikey=4975d0effdd49277f9f496ce27032830")
    data = response.json()
    DCF = data[0]["dcf"]
    return DCF

def get_shared_outstanding(company):
    try:  
        response = yf.Ticker(company)
        shares = response.info["sharesOutstanding"]
        return shares
    except:
        print("Not the response")
        
def enterprise_value(company):
    return (get_shared_outstanding(company)*get_DCF(company) + get_total_debt(company))

def purchase_price(company):
    ma_premium = 1.25
    return ma_premium * enterprise_value(company)



