import streamlit as st
from search import GoogleSearch
from web_scrapper import Website
from link_selection import LinkSelection
from brochure import BrochureCreation
from dotenv import load_dotenv
import os
import streamlit as st

if not os.path.exists("/root/.cache/ms-playwright"):
    st.write("Installing Playwright browsers... Please wait.")
    os.system("playwright install chromium")

load_dotenv()

google_search_api = os.getenv("GOOGLE_SEARCH_API")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not google_search_api or not search_engine_id or not openai_api_key:
    st.error("One or more environment variables are missing. Please check your .env file.")
    st.stop()

class CompanyBrochure:
    def __init__(self, google_api_key, cse_id, openai_api_key, model):
        self.google_api_key = google_api_key 
        self.cse_id = cse_id  
        self.openai_api_key = openai_api_key  
        self.model = model

    def create_company_brochure(self, company_name):
        search_query = f"{company_name} company"
        
        google_search = GoogleSearch(self.google_api_key, self.cse_id, search_query)
        search_results = google_search.search()

        website = Website(search_results[0]) 
        link_selection = LinkSelection(self.model, self.openai_api_key)
        relevant_links = link_selection.select_relevant_links(website)

        brochure_creation = BrochureCreation(self.model, self.openai_api_key)
        brochure = brochure_creation.create_brochure(company_name, relevant_links)

        return brochure

def main():
    st.title("Company Brochure Generator")

    st.header("Step 1: Enter the Company Name")
    company_name = st.text_input("Type the company name and press Enter:")

    if company_name:
        st.header("Step 2: Generated Brochure")
        
        with st.spinner("Generating the brochure... Please wait."):
            company_brochure = CompanyBrochure(google_search_api, search_engine_id, openai_api_key, 'gpt-4o-mini')
            brochure = company_brochure.create_company_brochure(company_name)
        
        st.subheader(f"Brochure for {company_name}")
        st.write(brochure)

if __name__ == "__main__":
    main()