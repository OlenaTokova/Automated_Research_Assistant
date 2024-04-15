import requests
import xml.etree.ElementTree as ET
import streamlit as st
import os

# Create a directory for search results if it doesn't exist
results_dir = 'search_results'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

def save_search_result(index, result):
    # Construct a filename for each result
    filename = os.path.join(results_dir, f"Result_{index}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Title: {result['title']}\n")
        file.write(f"URL: {result['url']}\n")
        file.write(f"Summary: {result['summary']}\n")
        
        
# The part of code responsible for registering the names of articles that 
# have already been displayed and ensuring they are not displayed again involves 
# a combination of the is_article_processed and record_processed_article functions.


def is_article_processed(title, filepath='processed_articles.txt'):
    try:
        with open(filepath, 'r') as file:
            processed_titles = file.read().splitlines()
        return title in processed_titles
    except FileNotFoundError:
        return False

def record_processed_article(title, filepath='processed_articles.txt'):
    with open(filepath, 'a') as file:
        file.write(title + '\n')

def search_arxiv(query):
    base_url = "http://export.arxiv.org/api/query?"
    search_params = f"search_query=all:{query}&start=0&max_results=100"
    response = requests.get(base_url + search_params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        results = []
        for entry in entries:
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            if not is_article_processed(title):
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
                results.append({"title": title, "summary": summary, "url": url})
                # Record the article as processed
                record_processed_article(title)
        return results
    else:
        return []

# Streamlit UI elements
st.title('arXiv Article Search')

query = st.text_input('Enter keywords to search for articles (title, author):', '')

if st.button('Search Articles', key='search_articles_button'):
    results = search_arxiv(query)
    if results:
        st.write(f"Returned: {len(results)} results.")
        for index, result in enumerate(results, start=1):
            st.markdown('---')  # Horizontal line
            st.markdown(f"{index}. [{result['title']}]({result['url']})")  # Title as a clickable link with numbering
            st.write(result['summary'])  # Summary
            save_search_result(index, result)  # Save each result
    else:
        st.write('No results found. Please try different keywords.')
