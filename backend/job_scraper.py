from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus
import time

def scrape_indeed_jobs(role, location):
    base_url = "https://in.indeed.com/jobs"
    
    # URL encode role and location
    query_role = quote_plus(role)
    query_location = quote_plus(location)
    url = f"{base_url}?q={query_role}&l={query_location}&radius=25"
    
    print("Scraping URL:", url)

    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up WebDriver using ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # Let the page load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        jobs = []

        for card in soup.select('a.tapItem')[:10]:  # Limit to top 10 jobs
            title_elem = card.find('h2')
            company_elem = card.find('span', class_='companyName')
            summary_elem = card.find('div', class_='job-snippet')
            href = card.get('href')

            title = title_elem.text.strip() if title_elem else 'No Title'
            company = company_elem.text.strip() if company_elem else 'No Company'
            summary = summary_elem.text.strip() if summary_elem else 'No Summary'
            link = f"https://in.indeed.com{href}" if href else 'No Link'

            jobs.append({
                'title': title,
                'company': company,
                'summary': summary,
                'link': link
            })
        
        return jobs

    finally:
        driver.quit()  # Make sure to quit the browser
