from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to extract emails from a webpage
def extract_data_from_webpage(url):
    # Open the webpage
    driver.get(url)
    
    # Wait for JavaScript to load and emails to decode
    time.sleep(10)  # Increased sleep time

    try:
        # Wait for the presence of elements containing encoded emails
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'mailto:') or contains(@href, '/cdn-cgi/l/email-protection')]"))
        )
    except TimeoutException:
        print("TimeoutException: No elements found within the specified wait time")
        return []

    # Find all rows in the table
    rows = driver.find_elements(By.XPATH, "//tbody/tr")

    # Extract data from each row
    data = []
    for row in rows:
        name_elem = row.find_element(By.XPATH, "./td[1]")
        company_elem = row.find_element(By.XPATH, "./td[3]")
        
        name = name_elem.text
        company = company_elem.text
        
        email = None
        email_elem = name_elem.find_element(By.XPATH, "./a[contains(@href, 'mailto:') or contains(@href, '/cdn-cgi/l/email-protection')]")
        href = email_elem.get_attribute('href')
        
        if 'mailto:' in href:
            email = href.replace('mailto:', '')
        elif '/cdn-cgi/l/email-protection' in href:
            encoded_string = email_elem.get_attribute('data-cfemail')
            email = decode_email_protection(encoded_string)
        
        data.append((name, email, company))

    return data

# Function to decode Cloudflare's email protection
def decode_email_protection(encoded_string):
    try:
        r = int(encoded_string[:2], 16)
        email = ''.join([chr(int(encoded_string[i:i+2], 16) ^ r) for i in range(2, len(encoded_string), 2)])
        return email
    except Exception as e:
        print("Error decoding email:", e)
        return None

# URL of the webpage to extract data from
url = 'https://salesleadsforever.com/free-list-of-companies-with-hr-email-details-of-indian-companies-2023/'

# Extract data and save to CSV
data = extract_data_from_webpage(url)
if data:
    with open('extracted_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Email', 'Company'])
        writer.writerows(data)
    print("Data extracted and saved to extracted_data.csv")
else:
    print("No data found")

# Close the WebDriver
driver.quit()
