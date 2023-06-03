import argparse
import pandas as pd
import google_custom_search
import asyncio
import re
from playwright.async_api import async_playwright

google = google_custom_search.CustomSearch(apikey="API_KEY", engine_id="ENGINE_ID")

def read_companies_names(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert the DataFrame column to a list
    data_list = df['company_name'].tolist()

    return data_list

def read_companies_links(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert the DataFrame column to a list
    data_list = df['company_link'].tolist()

    return data_list

async def search_company_url(companies_names):
    links = list()
    for company_name in companies_names:
        # Search for the company linkedin url in google
        results = await google.search_async(f"site: linkedin.com/company AND {company_name}")
        links.append(results[0].url)

    # Create the csv file for the companies links
    df = pd.DataFrame(links, columns=['company_link'])
    df.to_csv('links.csv', index=False)

async def get_number_of_employees(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        # Go to the company url
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        # Get the html text of the page
        text = await page.inner_html("*")
        # Get number of employees of the company using regex
        number_employees = re.findall(r'View all (\d+(?:,\d+)*) employees', text)

        await browser.close()

        return number_employees



async def main():

    # Input the companies names file as an argument
    parser = argparse.ArgumentParser(description='File Path of the csv file containing the companies names.')
    parser.add_argument('file_path')
    args = parser.parse_args()

    companies_names = read_companies_names(args.file_path)

    # generate csv file for the companies links
    print("Getting Companies links")
    await search_company_url(companies_names)
    # read the companies links from the generated csv
    companies_links = read_companies_links('links.csv')
    
    number_employees = list()
    # get N. of employees of the companies
    for link in companies_links:
        n_employees = await get_number_of_employees(link)
        print(f"Link: {link} Found: {n_employees} Employees")
        number_employees.append(n_employees)
    
    # Read the original CSV file
    df = pd.read_csv(args.file_path)

    # Add the new column to the DataFrame
    df['N. employees'] = number_employees
    df.to_csv(args.file_path, index=False)
    print("Original File Updated")



if __name__ == "__main__":
    asyncio.run(main())