import requests
from urllib.parse import quote

def main():
    query = input("Enter your search query: ")
    encoded_query = quote(query)
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={encoded_query}&format=xml"

    print(f"Request URL: {url}")  # Debugging step to check the formed URL
    
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")  # Debugging step to check the response status
    
    if response.status_code != 200:
        print("Failed to retrieve data, check the URL and your network connection.")
        return
    
    if 'No results found' in response.text:
        print("No found search result by your query. Try again with another query.")
        return
    else:
        print(response.text[:500])  # Debugging step to check part of the response

if __name__ == "__main__":
    main()
