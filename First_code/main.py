import requests
import sys
from bs4 import BeautifulSoup
import openai

#set PYTHONUTF8=1
#set PYTHONIOENCODING=utf-8

final_text:str = ""

def main():
    #openaikey = input("Enter your OPENAI key: ")
    #openai.api_key = openaikey
    query = input("Enter your search query: ")
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={query}"

    # Send the HTTP request
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'xml')
    full_text:list = soup.find_all('fullTextId')
    
    full_text_id:list = []
    print(f'All full text number find: {len(full_text)}')
    if len(full_text) > 0:
        for fl_text in full_text:
            full_text_id.append(fl_text.get_text())
    else:
        print("No found search result by your query. Try again with another query.")
        exit()
        
    global final_text
    for fl_text_id in full_text_id:
        print(f"Full text id: {fl_text_id}")
        full_text_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{fl_text_id}/fullTextXML"
        response = requests.get(full_text_url)
        soup = BeautifulSoup(response.text, 'xml')
        respone_beutify = soup.prettify()
        file_to_write = open(f"temp{fl_text_id}.xml", "w", encoding="utf-8")
        file_to_write.write(respone_beutify)

        #final_text += str(soup)
        #final_text += "☺☺"

    #final_text = final_text.rstrip("☺")
    #temp_file = open("temp.txt", "w", encoding="utf-8")
    #temp_file.write(final_text)
    #temp_file.close()
        
#    query = "Tell me a joke about the weather."

    # Make an API request
#    response = openai.Completion.create(
#        engine="text-embedding-3-small",  # Use the Davinci model
#        prompt=query,
#        max_tokens=100
#    )

    # Extract and print the response
#    chatgpt_response = response.choices[0].text
#    print("ChatGPT Response:", chatgpt_response)

if __name__ == "__main__":
    main()