import os
import hashlib
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Directory and file paths
base_dir = "C:/Users/Zeel Prajapati/Project/PennState/Data/PSUGreatValley"
data_dir = os.path.join(base_dir, "Static/academics")
excel_file_path = os.path.join(base_dir, "data_Updated.xlsx")
output_excel_path = os.path.join(base_dir, "scraped_data_with_hash_academic.xlsx")

# Ensure the output directory exists
os.makedirs(data_dir, exist_ok=True)

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

# Load existing scraped data if available
if os.path.exists(output_excel_path):
    existing_data_df = pd.read_excel(output_excel_path)
else:
    existing_data_df = pd.DataFrame(columns=["Page_Name", "Link", "Hash_Code"])

# Load the Excel file with the list of pages to crawl
pages_to_crawl_df = pd.read_excel(excel_file_path, sheet_name="Sheet1")

# Detect updated pages
updated_pages = []
for _, row in pages_to_crawl_df.iterrows():
    page_name = row["Page_Name"]
    link = row["Link"]

    # Check if the page exists in the existing data
    existing_entry = existing_data_df[existing_data_df["Page_Name"] == page_name]
    if not existing_entry.empty:
        # Compare the hash values
        existing_hash = existing_entry.iloc[0]["Hash_Code"]
        new_hash = scrape_and_save(page_name, link)
        if new_hash and existing_hash != new_hash:
            print(f"Page updated: {page_name}")
            updated_pages.append({"Page_Name": page_name, "Link": link, "Old_Hash_Code": existing_hash, "New_Hash_Code": new_hash})
    else:
        # If the page is not in the existing data, scrape it
        new_hash = scrape_and_save(page_name, link)
        if new_hash:
            updated_pages.append({"Page_Name": page_name, "Link": link, "Old_Hash_Code": None, "New_Hash_Code": new_hash})

# Convert updated pages to a DataFrame
updated_pages_df = pd.DataFrame(updated_pages)

# Display the updated pages (console output for verification)
if not updated_pages_df.empty:
    print("Updated Pages:")
    print(updated_pages_df)
else:
    print("No pages were updated.")

# Save the updated pages to a separate Excel file (optional)
updated_pages_output_path = os.path.join(base_dir, "updated_pages_academic.xlsx")
updated_pages_df.to_excel(updated_pages_output_path, index=False)
print(f"Updated pages saved to: {updated_pages_output_path}")
