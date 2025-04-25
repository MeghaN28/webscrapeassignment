import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL
url = 'https://www.worldometers.info/co2-emissions/us-co2-emissions'

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data from the summary div
summarydiv = soup.find('div', class_='border grid grid-cols-2 lg:grid-cols-6 px-3 py-3 text-center mb-12')

# Parse each block of the summary
datablocks = summarydiv.find_all('div', recursive=False)

summary_data = {}

# First block: Fossil CO2 Emissions
main_block = datablocks[0]
emissions_title = main_block.find('div', class_='text-2xl mb-2').get_text(strip=True)
emissions_value = main_block.find('div', class_='text-3xl font-bold').get_text(strip=True)
summary_data[emissions_title] = emissions_value

# Second block: Yearly Change
change_block = datablocks[1]
change_title = change_block.find('div', class_='text-xl mb-2').get_text(strip=True)
change_value = change_block.find('div', class_='text-2xl').get_text(strip=True)
summary_data[change_title] = change_value

# Third block: Global Share
share_block = datablocks[2]
share_title = share_block.find('div', class_='text-xl mb-2').get_text(strip=True)
share_value = share_block.find('div', class_='text-2xl').get_text(strip=True)
summary_data[share_title] = share_value

# Fourth block: Tons per capita
per_capita_block = datablocks[3]
per_capita_title = per_capita_block.find('div', class_='text-xl mb-2').get_text(strip=True)
per_capita_value = per_capita_block.find('div', class_='text-2xl').get_text(strip=True)
summary_data[per_capita_title] = per_capita_value


# Convert to DataFrame and save to Excel
summary_df = pd.DataFrame([summary_data])
summary_df.to_excel('us_co2_summary_2022.xlsx', index=False)



print("Summary CO₂ emissions data saved to 'us_co2_summary_2022.xlsx'")
