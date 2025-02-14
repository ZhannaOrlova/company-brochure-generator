import os
import requests

class GoogleSearch:
    def __init__(self, api_key, cse_id, query):
        self.api_key = api_key
        self.cse_id = cse_id
        self.query = query

class GoogleSearch:
    def __init__(self, api_key, cse_id, query):
        self.api_key = api_key
        self.cse_id = cse_id
        self.query = query

    def search(self):
        url = f"https://www.googleapis.com/customsearch/v1?q={self.query}&key={self.api_key}&cx={self.cse_id}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            results = response.json()
            return [item['link'] for item in results.get('items', [])]
        else:
            raise Exception(f"Error fetching search results: {response.status_code}")
