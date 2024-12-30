from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gas-price-scraper', methods=['POST'])
def gas_price_scraper():
    gas_value = request.form['gas_value']
    selected_category = request.form['selected_category']
    date = request.form['date']
    return scrape_gas_prices(gas_value, selected_category, date)

def scrape_gas_prices(gas_value,selected_category,date):
    try:
        # Fetch URL
        url = f'https://www.eex.com/en/market-data/natural-gas/futures#%7B%22snippetpicker%22%3A%22{gas_value}%22%7D'
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Accept cookies
        accept_cookies_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.bordered.uo_cookie_btn_type_0")))
        accept_cookies_button.click()
        next_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-footer']//button[@class='btn btn bordered grey close']")))
        driver.execute_script("arguments[0].click();", next_popup)

        # Filter by category
        filtered_div = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div#snippet-{gas_value}")))
        category_buttons = filtered_div.find_elements(By.CSS_SELECTOR, "div.mv-button-base.mv-hyperlink-button")
        already_selected = False
        for button in category_buttons:
            if button.text == selected_category and "mv-item-selected" in button.get_attribute("class"):
                already_selected = True
                break

        # Click the selected category button if it's not already selected
        if not already_selected:
            for button in category_buttons:
                if button.text == selected_category:
                    button.click()
                    break

        # Input the date
        div_tag = driver.find_element(By.CSS_SELECTOR, f"div#snippet-{gas_value}")
        input_tag = div_tag.find_element(By.CSS_SELECTOR, "input.mv-input-box")
        input_tag.clear()
        input_tag.send_keys(date)
        input_tag.send_keys(Keys.ENTER)
        time.sleep(1)  # Wait for the table to load

        # Scrape table
        filtered_div = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div#snippet-{gas_value}")))
        table = filtered_div.find_element(By.CSS_SELECTOR, "table.mv-quote")
        headers = [th.text for th in table.find_element(By.CSS_SELECTOR, "tr.mv-quote-header-row").find_elements(By.TAG_NAME, "th")]
        rows = []
        for tr in table.find_elements(By.CSS_SELECTOR, "tr.mv-quote-row"):
            row = [td.text for td in tr.find_elements(By.TAG_NAME, "td")[:len(headers)]]  # take only the first len(headers) columns
            rows.append(row)
        df = pd.DataFrame(rows, columns=headers)

        print(df)

        df.to_excel('output.xlsx', index=False)
        print("Data scraped successfully!")
        driver.quit()
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)