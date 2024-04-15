"""TODO: Add a module description here"""

import os
import re
import datetime
import requests
import spacy
import xmltodict


api_key = ""
headers = {"Authorization": f"Bearer {api_key}"}
#response = requests.get("https://api.example.com/articles?query=Machine+Learning", headers=headers)

#data_dict = xmltodict.parse(xml_data)

try:
    response = requests.get('https://www.ncbi.nlm.nih.gov/')
    if response.headers.get('Content-Type') == 'application/json':
        data = response.json()  # Parse JSON data
        print(data)  # This should print a JSON response if successful
    else:
        print('Response content is not in JSON format.')
        print(response.text)  # Print HTML or other response text
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Function to search for articles (replace 'your_api_endpoint' with the actual API endpoint)
def search_articles(query):
    # This is a placeholder for how you might interact with an academic API.
    # You'll need to replace this with actual code to interact with a real API.
    response = requests.get(f"https://www.ncbi.nlm.nih.gov/={query}")
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON with a list of articles
    else:
        return []

# Function to summarize an article
def summarize_article(article_text):
    doc = nlp(article_text)
    # Extracting sentences; this is a naive approach for demonstration.
    # More sophisticated summarization techniques can be applied.
    sentences = list(doc.sents)
    return ' '.join(sentences[:3])  # Return the first three sentences as a summary

# Function to extract key terms from an article
def extract_key_terms(article_text):
    doc = nlp(article_text)
    # Extracting Nouns and Proper Nouns as key terms; this is a simplification.
    key_terms = set([chunk.text for chunk in doc.noun_chunks if chunk.root.pos_ in ['NOUN', 'PROPN']])
    return key_terms

# Main function to demonstrate the assistant's functionality
def main():
    query = "Machine Learning"  # Example search query
    articles = search_articles(query)
    
    # for article in articles[:5]:  # Assuming each article has 'title' and 'content'
    #     print(f"Title: {article['title']}")
    #     summary = summarize_article(article['content'])
    #     print(f"Summary: {summary}")
    #     key_terms = extract_key_terms(article['content'])
    #     print(f"Key Terms: {', '.join(key_terms)}\n")


    # # Verify if the directory exists, create if it does not exist
    # if not os.path.exists('article_search_results'):
    #     os.makedirs('article_search_results')

    # for i, article in enumerate(articles[:5], start=1):  # Assuming each article has 'title' and 'content'
    #     print(f"Result Number: {i}")
    #     print(f"Title: {article['title']}")
    #     summary = summarize_article(article['content'])
    #     print(f"Summary: {summary}")
    #     key_terms = extract_key_terms(article['content'])
    #     print(f"Key Terms: {', '.join(key_terms)}\n")

    #     # Create a time-stamped file name
    #     timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    #     filename = f"{article['title'][:24]}_{timestamp}.xhtml"

    #     # Write the output to the file
    #     with open(os.path.join('article_search_results', filename), 'w') as f:
    #         f.write(f"Result Number: {i}\n")
    #         f.write(f"Title: {article['title']}\n")
    #         f.write(f"Summary: {summary}\n")
    #         f.write(f"Key Terms: {', '.join(key_terms)}\n")


# ...

for i, article in enumerate(articles[:5], start=1):  # Assuming each article has 'title' and 'content'
    print(f"Result Number: {i}")
    print(f"Title: {article['title']}")
    summary = summarize_article(article['content'])
    print(f"Summary: {summary}")
    key_terms = extract_key_terms(article['content'])
    print(f"Key Terms: {', '.join(key_terms)}\n")

    # Create a time-stamped file name
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    safe_title = re.sub(r'[\\/*?:"<>|]', "", article['title'][:24])  # Remove invalid characters
    filename = f"{safe_title}_{timestamp}.xhtml"

    # Write the output to the file
    with open(os.path.join('article_search_results', filename), 'w') as f:
        f.write(f"Result Number: {i}\n")
        f.write(f"Title: {article['title']}\n")
        f.write(f"Summary: {summary}\n")
        f.write(f"Key Terms: {', '.join(key_terms)}\n")

# Run the main function
if __name__ == "__main__":
    main()
