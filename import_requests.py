import requests
import spacy

api_key = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {api_key}"}

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

'''
try:
    response = requests.get(f"https://www.ncbi.nlm.nih.gov/", headers=headers)
    print(response.json())  # This should print a JSON response if successful
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    '''

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Function to search for articles
def search_articles(query):
    try:
        response = requests.get(f"https://www.ncbi.nlm.nih.gov/={query}")
        if response.status_code == 200:
            return response.json()  # Assuming the API returns JSON with a list of articles
        else:
            return []
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return []

# Function to summarize an article
def summarize_article(article_text):
    doc = nlp(article_text)
    sentences = list(doc.sents)
    return ' '.join(str(sentence) for sentence in sentences[:3])  # Return the first three sentences as a summary

# Function to extract key terms from an article
def extract_key_terms(article_text):
    doc = nlp(article_text)
    key_terms = set([chunk.text for chunk in doc.noun_chunks if chunk.root.pos_ in ['NOUN', 'PROPN']])
    return key_terms

# Main function to demonstrate the assistant's functionality
def main():
    query = "Machine Learning"  # Example search query
    articles = search_articles(query)
    
    for article in articles[:5]:  # Assuming each article has 'title' and 'content'
        print(f"Title: {article['title']}")
        summary = summarize_article(article['content'])
        print(f"Summary: {summary}")
        key_terms = extract_key_terms(article['content'])
        print(f"Key Terms: {', '.join(key_terms)}\n")

# Run the main function
if __name__ == "__main__":
    main()