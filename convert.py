import csv

def guess_first_name(email):
    # Extract the part before the "@" symbol
    local_part = email.split('@')[0]
    
    # Split by common delimiters to guess the first name
    for delimiter in ['.', '_', '-']:
        if delimiter in local_part:
            return local_part.split(delimiter)[0].capitalize()
    
    # If no delimiter is found, use the entire local part as the first name
    return local_part.capitalize()

def guess_company_name(email):
    # Extract the domain part
    domain_part = email.split('@')[1]
    
    # Remove common TLDs and split by common delimiters
    domain_part = domain_part.split('.')[0]
    
    # Capitalize the guessed company name
    return domain_part.capitalize()

def convert_email_list_to_csv(input_file, output_file):
    # Read email addresses from the text file
    with open(input_file, 'r') as file:
        emails = [line.strip() for line in file if line.strip()]
    
    # Prepare data for CSV
    data = []
    for email in emails:
        first_name = guess_first_name(email)
        company_name = guess_company_name(email)
        data.append([first_name, email, company_name])
    
    # Write data to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Email', 'Company Name'])
        writer.writerows(data)
    
    print(f"Data successfully written to {output_file}")

# File paths
input_file = 'list of email.txt'
output_file = 'emails_with_names_and_companies_999999.csv'

# Convert the email list to CSV
convert_email_list_to_csv(input_file, output_file)