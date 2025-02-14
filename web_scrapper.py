from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from playwright_stealth import stealth
import time

class Website:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.title = ""
        self.text = ""
        self.scrape()

    def scrape(self, max_retries=3):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        with sync_playwright() as p:
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"Attempt {attempt} to fetch {self.url}...")
                    
                    browser = p.chromium.launch(
                        headless=True,
                        args=[
                            "--no-sandbox", "--disable-setuid-sandbox",
                            "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"
                        ]
                    )
                    context = browser.new_context(ignore_https_errors=True, extra_http_headers=headers)
                    page = context.new_page()

                    stealth(page)

                    page.goto(self.url, timeout=20000)  
                    page.wait_for_load_state("networkidle") 

                    html = page.content()  
                    browser.close()

                    break

                except Exception as e:
                    print(f"⚠️ Attempt {attempt} failed: {e}")
                    browser.close()
                    time.sleep(3)  
                    if attempt == max_retries:
                        raise Exception(f"Error fetching the webpage {self.url} after {max_retries} attempts")

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
