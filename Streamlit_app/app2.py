import requests
import xml.etree.ElementTree as ET
import streamlit as st
import os
import csv

# Create a directory for search results if it doesn't exist
results_dir = 'search_results'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

def save_search_results(results):
    # Define the CSV file path
    csv_filename = os.path.join(results_dir, "search_results.csv")
    
    # Open the CSV file for writing
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Define the column names
        fieldnames = ['Index', 'Title', 'URL', 'Summary']
        
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write each search result as a row in the CSV file
        for index, result in enumerate(results, start=1):
            writer.writerow({'Index': index, 'Title': result['title'], 'URL': result['url'], 'Summary': result['summary']})

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
        # Save all search results to a CSV file
        save_search_results(results)
    else:
        st.write('No results found. Please try different keywords.')
