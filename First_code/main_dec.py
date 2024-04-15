import requests
from bs4 import BeautifulSoup

def extract_url(article):
    """Attempt to construct an article URL from available identifiers."""
    doi = article.find('doi')
    pmid = article.find('pmid')
    europe_pmc_id = article.find('id')  # Assuming 'id' could be a Europe PMC ID
    
    if doi:
        return f"https://doi.org/{doi.text.strip()}"
    elif pmid:
        return f"https://pubmed.ncbi.nlm.nih.gov/{pmid.text.strip()}/"
    elif europe_pmc_id:
        # This is a fallback and might not always lead to a direct article link
        return f"https://europepmc.org/article/MED/{europe_pmc_id.text.strip()}"
    else:
        return None

def main():
    query = "big data"
    encoded_query = requests.utils.quote(query)
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={encoded_query}&format=xml"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'xml')
        articles = soup.find_all('result', limit=3)  # Adjust as needed
        
        with open("search_results.txt", "w", encoding="utf-8") as file:
            if articles:
                file.write(f"Found articles related to '{query}':\n\n")
                for article in articles:
                    title = article.find('title').text.strip() if article.find('title') else 'No Title'
                    link = extract_url(article)
                    
                    if link:
                        file.write(f"Title: {title}\nLink: {link}\n\n")
                    else:
                        file.write(f"Title: {title}\nLink: No direct link available\n\n")
            else:
                file.write("No articles found for your query. Please try a different query.")
            print("Results have been saved to 'search_results.txt'")
    else:
        print("Failed to retrieve data. Status Code:", response.status_code)

if __name__ == "__main__":
    main()
