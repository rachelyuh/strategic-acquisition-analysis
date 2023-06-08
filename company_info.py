import requests


def get_company_info(company):
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/profile/{company}?apikey=8d8d7b6df8c7889b80fee22328d2c0dd")
    data = response.json()
    company_info = {}
    company_info["companyName"] = data[0]["companyName"]
    company_info["description"] = data[0]["description"]
    company_info["image"] = data[0]["image"]
    company_info["sector"] = data[0]["sector"]
    return company_info


