import os
import hashlib
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Directory and file paths
base_dir = "C:/Users/Zeel Prajapati/Project/PennState/Data/PSUGreatValley"
data_dir = os.path.join(base_dir, "Static/admission")
excel_file_path = os.path.join(base_dir, "data_Updated.xlsx")
output_excel_path = os.path.join(base_dir, "scraped_data_with_hash_admission.xlsx")

# Ensure the output directory exists
os.makedirs(data_dir, exist_ok=True)

# Load the Excel file
pages_to_crawl_df = pd.read_excel(excel_file_path, sheet_name="Sheet2")

# Function to calculate the hash of a webpage
def calculate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

# Function to scrape a webpage and save its content
def scrape_and_save(page_name, link):
    try:
        response = requests.get(link, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {page_name} ({link}): HTTP {response.status_code}")
            return None
        content = response.text

        # Save the content to a .txt file
        file_path = os.path.join(data_dir, f"{page_name.replace(' ', '_')}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        # Calculate hash of the content
        page_hash = calculate_hash(content)
        print(f"Successfully scraped and saved: {page_name}")
        return page_hash
    except Exception as e:
        print(f"Error scraping {page_name}: {e}")
        return None

# Initialize a list to store the results
results = []

# Iterate over each page to scrape and process
for _, row in pages_to_crawl_df.iterrows():
    page_name = row["Page_Name"]
    link = row["Link"]

    # Scrape the page and get its hash
    page_hash = scrape_and_save(page_name, link)
    if page_hash:
        results.append({"Page_Name": page_name, "Link": link, "Hash_Code": page_hash})

# Create a DataFrame from the results
scraped_data_df = pd.DataFrame(results)

# Save the data to a new Excel file
scraped_data_df.to_excel(output_excel_path, index=False)
print(f"Scraping complete. Data saved to: {output_excel_path}")