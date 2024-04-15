from utils import sanitize_filename
import requests
import xml.etree.ElementTree as ET
import streamlit as st
import os
import csv
import re
import openai


# Define functions for working with arXiv API, OpenAI API, and utilities

def fetch_articles_from_arxiv(query):
    arxiv_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=10"
    response = requests.get(arxiv_url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        articles = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            # Extract URL
            link = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
            articles.append({"title": title, "summary": summary, "url": link})
        return articles
    else:
        print(f"Failed to fetch articles: HTTP {response.status_code}")
        return []

def compute_similarity_gpt3(title1, title2):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Rate the similarity between these two titles on a scale from 0 to 1: Title 1: {title1} Title 2: {title2}"},
            ]
        )
        similarity_text = response.choices[0].message["content"].strip()
        similarity_score = extract_similarity_score(similarity_text)
        return similarity_score
    except Exception as e:
        print(f"Error computing similarity with OpenAI API: {e}")
        return 0

def extract_similarity_score(text):
    matches = re.findall(r"\d+\.\d+|\d+", text)
    if matches:
        return float(matches[0])
    return 0  # Default to 0 if no numerical score is found

def normalize_title(title):
    title = title.lower()
    title = re.sub(r'\s+', '_', title)
    title = re.sub(r'[^\w\s]', '', title)
    return title

def is_article_processed(title, filepath='processed_articles.txt'):
    normalized_title = normalize_title(title)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for processed_title in file:
                processed_title_normalized = normalize_title(processed_title.strip())
                similarity = compute_similarity_gpt3(normalized_title, processed_title_normalized)
                if similarity > 0.9:  
                    return True
    except (UnicodeDecodeError, FileNotFoundError):
        pass
    return False

def record_processed_article(title, filepath='processed_articles.txt'):
    try:
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write(title + '\n')
    except UnicodeEncodeError:
        print(f"Error encoding title: {title}")

def save_search_results(results, query):
    safe_query = sanitize_filename(query)
    specific_results_dir = os.path.join('search_results', f"search_results_{safe_query}")
    if not os.path.exists(specific_results_dir):
        os.makedirs(specific_results_dir)
    csv_filename = os.path.join(specific_results_dir, f"search_results_{safe_query}.csv")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Index', 'Title', 'URL', 'Summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index, result in enumerate(results, start=1):
            writer.writerow({'Index': index, 'Title': result['title'], 'URL': result['url'], 'Summary': result['summary']})

# Streamlit UI
st.title('arXiv Article Search')
query = st.text_input('Enter keywords to search for articles (title, author):', '', key="query")
if st.button('Search Articles') or ('query' in st.session_state and st.session_state.query):
    results_dir = 'search_results'  # Ensure results_dir is defined for use in save_search_results
    results = fetch_articles_from_arxiv(query)
    if results:
        st.write(f"Returned: {len(results)} results.")
        for index, result in enumerate(results, start=1):
            st.markdown('---')
            st.markdown(f"{index}. [{result['title']}]({result['url']})")
            st.write(result['summary'])
        save_search_results(results, query)
    else:
        st.write('No results found. Please try different keywords.')
        
