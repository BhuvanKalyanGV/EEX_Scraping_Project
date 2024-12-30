# Project Title: EEX Website Scraper
## Simple Overview of Use/Purpose
This project is a web scraper that extracts gas price data from the European Energy Exchange (EEX) website. It uses a Flask web application to provide a user interface for selecting the type, category, and date of the data to be scraped. The scraped data is then saved to an Excel file.

## Description
This project is designed to simplify the process of extracting gas price data from the EEX website. It uses Selenium WebDriver to navigate the website, select the desired filters, and scrape the resulting table. The data is then saved to an Excel file for further analysis.

## Getting Started
### Dependencies
* Python 3.x
* Flask
* Selenium WebDriver
* ChromeDriverManager
* pandas

### Installing
1. Clone the repository to your local machine
2. Install the required dependencies using `pip install -r requirements.txt`
3. Run the Flask application using `python app.py`

## Executing Program
1. Open a web browser and navigate to `http://localhost:5000`
2. Select the type, category, and date of the data to be scraped using the provided form
3. Click the "Scrape" button to start the scraping process
4. The scraped data will be saved to an Excel file named `output.xlsx`

## Help
* If you encounter any issues with the scraping process, check the console output for error messages
* Make sure that the ChromeDriverManager is installed and up-to-date
* If you need to modify the scraping process, refer to the Selenium WebDriver documentation for more information

## Author
Bhuvan Kalyan G V
[LinkedIn: in/bhuvan-kalyan-g-v-831435312](https://www.linkedin.com/in/bhuvan-kalyan-g-v-831435312/)

## Version History
 0.1: Initial Release
