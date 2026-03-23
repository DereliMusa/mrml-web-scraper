import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://unisis.ege.edu.tr/researcher=oguz.gurses")
time.sleep(5) # Wait for React to render

soup = BeautifulSoup(driver.page_source, 'html.parser')
# Let's find some key headers or sections to understand the layout
print("--- Extracted Text Preview ---")
print(soup.get_text(separator='\n', strip=True)[:2000])

print("\n--- Searching for specific sections ---")
for text in ['Profil', 'Metrikleri', 'Kurum Bilgileri']:
    elem = soup.find(lambda t: t.name and text in t.text)
    if elem:
        print(f"Found '{text}' in tag: {elem.name}, class: {elem.get('class')}")
    else:
        print(f"'{text}' not found directly.")

driver.quit()
