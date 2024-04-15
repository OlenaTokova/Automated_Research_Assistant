import requests
import xml.etree.ElementTree as ET
import streamlit as st
import os
import csv
import re


def is_article_processed(title, filepath='processed_articles.txt'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            processed_titles = file.read().splitlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            processed_titles = file.read().splitlines()
    except FileNotFoundError:
        return False
    return title in processed_titles


def record_processed_article(title, filepath='processed_articles.txt'):
    try:
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write(title + '\n')
    except UnicodeEncodeError:
        print(f"Error encoding title: {title}")
        

# Global results directory
results_dir = 'search_results'

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

def sanitize_filename(filename):
    """
    Sanitize the query to be used as a valid filename.
    """
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

def save_search_results(results, query):
    # Sanitize the query to create a valid directory name
    safe_query = sanitize_filename(query)
    specific_results_dir = os.path.join(results_dir, f"search_results_{safe_query}")
    if not os.path.exists(specific_results_dir):
        os.makedirs(specific_results_dir)

    # Define the CSV file path
    csv_filename = os.path.join(specific_results_dir, f"search_results_{safe_query}.csv")
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Index', 'Title', 'URL', 'Summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index, result in enumerate(results, start=1):
            writer.writerow({'Index': index, 'Title': result['title'], 'URL': result['url'], 'Summary': result['summary']})

# The rest of the functions remain unchanged



# Initial directory creation removed since we now create a new directory for each query

# Modified part of the Streamlit UI elements
st.title('arXiv Article Search')

query = st.text_input('Enter keywords to search for articles (title, author):', '', on_change=None, key="query")

if st.button('Search Articles') or st.session_state.query:
    results_dir = 'search_results'  # Ensure results_dir is defined for use in save_search_results
    results = search_arxiv(query)
    if results:
        st.write(f"Returned: {len(results)} results.")
        for index, result in enumerate(results, start=1):
            st.markdown('---')
            st.markdown(f"{index}. [{result['title']}]({result['url']})")
            st.write(result['summary'])
        save_search_results(results, query)
    else:
        st.write('No results found. Please try different keywords.')
