import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class Website:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.title = ""
        self.text = ""
        self.scrape()

    def scrape(self):
        options = Options()
        options.add_argument("--headless")  # No GUI mode
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(self.url)
            time.sleep(5)  # Allow JavaScript to load
            html = driver.page_source
        except Exception as e:
            driver.quit()
            raise Exception(f"⚠️ Error fetching webpage {self.url}: {e}")

        driver.quit()
        self.parse_html(html)

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
