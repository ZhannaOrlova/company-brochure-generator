import httpx
from bs4 import BeautifulSoup

class Website:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.title = ""
        self.text = ""
        self.scrape()

    def scrape(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        try:
            response = httpx.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()  # Ensure the request was successful
            html = response.text
        except Exception as e:
            raise Exception(f"⚠️ Could not fetch webpage {self.url}. It may be a highly dynamic site or blocked: {e}")

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
