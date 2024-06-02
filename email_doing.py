from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to extract emails from a webpage
def extract_emails_from_webpage(url):
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

    # Find all email elements (encoded and mailto links)
    email_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'mailto:') or contains(@href, '/cdn-cgi/l/email-protection')]")

    # Extract email addresses from the href attribute
    emails = []
    for elem in email_elements:
        href = elem.get_attribute('href')
        if 'mailto:' in href:
            emails.append(href.replace('mailto:', ''))
        elif '/cdn-cgi/l/email-protection' in href:
            encoded_string = elem.get_attribute('data-cfemail')
            email = decode_email_protection(encoded_string)
            if email:
                emails.append(email)

    return emails

# Function to decode Cloudflare's email protection
def decode_email_protection(encoded_string):
    try:
        r = int(encoded_string[:2], 16)
        email = ''.join([chr(int(encoded_string[i:i+2], 16) ^ r) for i in range(2, len(encoded_string), 2)])
        return email
    except Exception as e:
        print("Error decoding email:", e)
        return None

# URL of the webpage to extract emails from
url = 'https://salesleadsforever.com/free-list-of-companies-with-hr-email-details-of-indian-companies-2023/'

# Extract emails and print them
emails = extract_emails_from_webpage(url)
if emails:
    for email in emails:
        print(email)
else:
    print("No emails found")

# Close the WebDriver
driver.quit()
