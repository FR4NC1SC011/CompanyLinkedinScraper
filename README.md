# CompanyLinkedinScraper
This Python module allows you to scrape company data from LinkedIn, including the company's LinkedIn URL and number of employees. It uses Google Custom Search for finding the LinkedIn URL based on the company name, and Playwright for extracting the number of employees from the LinkedIn company page.

## Requirements

- Python 3.x
- pandas
- google_custom_search
- playwright
- argparse
- asyncio
- re

## Usage

1. Prepare a CSV file containing a list of company names. Each company name should be in a separate row under the column name 'Company Name'.

2. Execute the module by running `python main.py [csv_file_path]`.

3. The module will perform the following steps for each company:
   - Use Google Custom Search to find the LinkedIn URL for the company.
   - Use Playwright to extract the number of employees from the LinkedIn company page.
   - Update the original CSV file by adding a new column 'Number of Employees' with the extracted data.

4. Once the execution is complete, you will find the updated CSV file with the added column.

## Configuration

The module uses the following configuration options:

- Google Custom Search API Key: Obtain an API key from the Google Developers Console and provide it in the `api_key` in `main.py`.
- Google Custom Search Engine ID: Create a custom search engine and get the Engine ID from the Control Panel. Provide it in the `engine_id` in `main.py`.

## License

This project is licensed under the [MIT License](LICENSE).