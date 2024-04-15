import requests

url = 'https://www.ncbi.nlm.nih.gov/'
headers = {'Accept': 'application/json'}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises a HTTPError if the response status isn't 200
    print(response.text)  # Print the response content
    data = response.json()  # Try to parse response as JSON
    print(data)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")
except ValueError:  # Includes simplejson.errors.JSONDecodeError
    print("Response content is not in JSON format.")