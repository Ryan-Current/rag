import json 
import os
import requests 
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama

class InternetSearcher():
    CONFIG_FILE_NAME = 'config.json'
    
    def __init__(self, model: str = 'llama3'):
        with open(self.CONFIG_FILE_NAME, 'r') as file:
            config = json.load(file)

        self.SERPER_API_KEY = config['SERPER_API_KEY']
        self.INTERNET_SEARCH_LOCATION = config['INTERNET_SEARCH_LOCATION']
        self.model = Ollama(model=model)

    def scrape_and_summarize_website(self, url):
        response = requests.get(url)

        if response.status_code == 200: 
            soup = BeautifulSoup(response.content, "html.parser")
            content = soup.get_text(strip=True)
            content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        else:
            content = []

        summaries = []
        for chunk in content:
            summary = self.model.invoke(f'Summarize this text in a consise but thorough way: \n\n CONTENT \n {chunk}')
            summaries.append(summary)
        return "\n\n".join(summaries)


    def search_internet(self, query):
        top_result_to_return = 2
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query,
            "location": self.INTERNET_SEARCH_LOCATION
        })
        headers = {
            'X-API-KEY': self.SERPER_API_KEY,
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # check if there is an organic key
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
        else:
            results = response.json()['organic']
            summaries = []
            for result in results[:top_result_to_return]:
                try:
                    summaries.append('\n'.join([
                        self.scrape_and_summarize_website(result['link'])
                        # result['link']
                        # f"Title: {result['title']}", f"Link: {result['link']}",
                        # f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    next
        return '\n'.join(summaries)