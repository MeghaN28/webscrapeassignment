from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select         # for interacting with dropdowns
from selenium.webdriver.support.ui import WebDriverWait  # for explicit waits
from selenium.webdriver.support import expected_conditions as EC
import time                                             # increase wait time for debugging

browser = webdriver.Chrome()

# Load the page
url = "https://www.worldometers.info/co2-emissions/us-co2-emissions"
browser.get(url)


time.sleep(5)  

# Get the page source after JavaScript has rendered the content
page_source = browser.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find the table inside the 'datatable-container'
table = soup.find("table", class_="datatable w-full border border-zinc-200 font-bold datatable-table")
if not table:
    raise ValueError("Could not find the table inside datatable-container.")

# Extract headers from the table
headers = [th.get_text(strip=True).replace('\n', ' ') for th in table.find('thead').find_all('th')]

# Extract rows from the table
rows = []
for tr in table.find("tbody").find_all("tr"):
    cells = [td.get_text(strip=True).replace('\n', ' ') for td in tr.find_all("td")]
    if len(cells) == len(headers):  # Ensure the row matches the header length
        rows.append(cells)

# Create a DataFrame and save the data to an Excel file
df = pd.DataFrame(rows, columns=headers)
df.to_excel("us_co2_emissions_table.xlsx", index=False)

print("✅ CO₂ emissions table extracted and saved to 'us_co2_emissions_table.xlsx'")


browser.quit()
