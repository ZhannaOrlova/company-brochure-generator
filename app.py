from search import GoogleSearch
from web_scrapper import Website
from link_selection import LinkSelection
from brochure import BrochureCreation

from dotenv import load_dotenv
import os

load_dotenv()

google_search_api = os.getenv("GOOGLE_SEARCH_API") or input("Enter your Google Search API key: ")
search_engine_id = os.getenv("SEARCH_ENGINE_ID") or input("Enter your Custom Search Engine ID: ")
openai_api_key = os.getenv("OPENAI_API_KEY") or input("Enter your OpenAI API key: ")

if not google_search_api or not search_engine_id or not openai_api_key:
    print("One or more environment variables are missing.")
    exit()

class CompanyBrochure:
    def __init__(self, google_api_key, cse_id, openai_api_key, model):
        self.google_api_key = google_api_key  
        self.cse_id = cse_id  
        self.openai_api_key = openai_api_key  
        self.model = model

    def create_company_brochure(self, company_name):
        google_search = GoogleSearch(self.google_api_key, self.cse_id, company_name)
        search_results = google_search.search()

        website = Website(search_results[0])  
        link_selection = LinkSelection(self.model, self.openai_api_key)
        relevant_links = link_selection.select_relevant_links(website)

        brochure_creation = BrochureCreation(self.model, self.openai_api_key)
        brochure = brochure_creation.create_brochure(company_name, relevant_links)

        return brochure

if __name__ == "__main__":
    company_name = input("Enter the company name to create a brochure: ")
    
    company_brochure = CompanyBrochure(google_search_api, search_engine_id, openai_api_key, 'gpt-4o-mini')
    
    brochure = company_brochure.create_company_brochure(company_name)

    print("\nGenerated Brochure:\n")
    print(brochure)
