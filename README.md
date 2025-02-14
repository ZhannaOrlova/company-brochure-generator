*Get the Google Search API and CSE ID. 
You can follow the instructions of this particular YouTube video that explain very well how to obtain the keys. https://www.youtube.com/watch?v=TddYMNVV14g&t=20s. 

# 📄 Company Brochure Generator

The **Company Brochure Generator** is a Python-based project that automates the process of searching for company-related information, extracting key details, and generating a well-structured brochure using OpenAI's GPT model. The project leverages **Google Search**, **web scraping**, and **LLMs** to create an insightful company brochure.

## 🚀 Features
- **Automated Company Search**: Uses Google Search API to find company-related pages.
- **Intelligent Web Scraping**: Extracts text and relevant links from company websites.
- **Link Selection with AI**: Uses GPT-4o-mini to determine which links are relevant for the brochure.
- **Brochure Generation**: Converts gathered data into a structured company brochure.
- **Interactive UI with Streamlit**: Provides an easy-to-use interface for users to input company names and receive a brochure.

---

## 📦 Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/company-brochure-generator.git
cd company-brochure-generator
```

- Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

- Install Dependencies
```bash
pip install -r requirements.txt
```

- Set Up API Keys

Create a .env file in the root directory and add the following:
```bash
GOOGLE_SEARCH_API=your-google-api-key
SEARCH_ENGINE_ID=your-google-search-engine-id
OPENAI_API_KEY=your-openai-api-key
```

## 🛠 Usage
```bash
streamlit run streamlit_app.py
```

## 🛠 How It Works
Enter the name of a company.
The system searches Google for the most relevant pages.
It scrapes the companys website for key details.
The AI selects relevant links.
OpenAI generates a structured company brochure.
The final brochure is displayed in the Streamlit interface.



