import requests
import spacy

api_key = ""
headers = {"Authorization": f"Bearer {api_key}"}

headers = {
    'Accept': 'application/json'
}
response = requests.get('https://www.ncbi.nlm.nih.gov/', headers=headers)


try:
    response = requests.get('https://www.ncbi.nlm.nih.gov/')
    response.raise_for_status()  # Raises a HTTPError if the response status isn't 200
    if response.text:  # Check if response is not empty
        try:
            data = response.json()  # Try to parse response as JSON
            print(data)
        except ValueError:  # Catch JSONDecodeError
            print("Response content is not in JSON format.")
    else:
        print("Empty response.")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")
print(response.text)
