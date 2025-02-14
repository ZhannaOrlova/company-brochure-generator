import cloudscraper
from bs4 import BeautifulSoup
import os

class Website:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.title = ""
        self.text = ""
        self.scrape()

    def scrape(self):
        scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "mobile": False})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        try:
            response = scraper.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"⚠️ Could not fetch {self.url} directly. Trying ScrapingBee API...")
            html = self.scrape_with_scrapingbee()
        
        self.parse_html(html)

    def scrape_with_scrapingbee(self):
        api_key = os.getenv("SCRAPINGBEE_API_KEY")
        if not api_key:
            raise Exception("⚠️ Missing ScrapingBee API key in environment variables.")

        url = f"https://app.scrapingbee.com/api/v1/?api_key={api_key}&url={self.url}&render_js=True"
        response = cloudscraper.get(url)

        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"⚠️ ScrapingBee API failed: {response.status_code}")

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"

        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        self.links = [link.get('href') for link in soup.find_all('a') if link.get('href')]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
