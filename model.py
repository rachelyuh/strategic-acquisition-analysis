import requests

def get_free_cash_flow(company):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit=120&apikey=4975d0effdd49277f9f496ce27032830")
    data = response.json()
    free_cash_flow = []
    free_cash_flow.append(data[0]["freeCashFlow"])
    free_cash_flow.append(data[1]["freeCashFlow"])
    free_cash_flow.append(data[2]["freeCashFlow"])
    free_cash_flow.append(data[3]["freeCashFlow"])
    return free_cash_flow

