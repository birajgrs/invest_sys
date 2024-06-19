# forex_api/api.py
import requests

def get_forex_rates(date):
    base_url = "https://www.nrb.org.np/api/forex/v1/"
    endpoint = "rates"
    url = f"{base_url}{endpoint}"

    # Prepare parameters
    params = {
        "page": 1,
        "per_page": 1,
        "from": date,
        "to": date
    }

    try:
        # Make request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    return None
