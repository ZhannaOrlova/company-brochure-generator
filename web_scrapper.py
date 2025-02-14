from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(self.url)
            driver.implicitly_wait(10)

            html = driver.page_source
        except Exception as e:
            driver.quit()
            raise Exception(f"Error loading the webpage: {e}")
        finally:
            driver.quit()

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

if __name__ == "__main__":
    url = "https://www.example.com"  # set any URL
    website = Website(url)
    print(website.get_contents())
    print("Extracted links:")
    for link in website.links:
        print(link)
