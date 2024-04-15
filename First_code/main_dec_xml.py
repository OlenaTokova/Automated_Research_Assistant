import requests
from bs4 import BeautifulSoup

def main():
    query = input("Enter your search query: ")
    # Encoding the query for safe URL inclusion
    encoded_query = requests.utils.quote(query)
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={encoded_query}&format=xml"

    # Send the HTTP request
    response = requests.get(url)
    # Parse the XML content
    soup = BeautifulSoup(response.text, 'xml')
    
    # Extract the first few search result details
    articles = soup.find_all('result', limit=3)  # Adjust the limit as needed
    
    if not articles:
        print("No results found for your query. Try again with another query.")
        return
    
    for article in articles:
        title = article.find('title').text if article.find('title') else 'No Title'
        abstract = article.find('abstract').text if article.find('abstract') else 'No Abstract'
        print(f"Title: {title}\nAbstract: {abstract}\n---")
        
    # Here, you might save or further process the extracted information as needed.

if __name__ == "__main__":
    main()
