import os
import requests
from dotenv import load_dotenv

load_dotenv()

google_search_api = os.getenv("GOOGLE_SEARCH_API") or input("Enter your Google Search API key: ")
search_engine_id = os.getenv("SEARCH_ENGINE_ID") or input("Enter your Custom Search Engine ID: ")
openai_api_key = os.getenv("OPENAI_API_KEY") or input("Enter your OpenAI API key: ")

if not google_search_api or not search_engine_id or not openai_api_key:
    print("One or more environment variables are missing.")
    exit()

query = "Python web scraping"

url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_search_api}&cx={search_engine_id}"

response = requests.get(url)

if response.status_code == 200:
    results = response.json()
    print("Search results:")
    for item in results.get('items', []):
        print(f"- {item['link']}")
else:
    print(f"Error fetching search results: {response.status_code}")
    print(f"Response: {response.text}")
