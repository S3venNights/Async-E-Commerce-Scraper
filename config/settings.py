import os

# Scraper Configuration
LIST_URL = "https://www.elcykelpunkten.se/elcyklar/recycle"
CONCURRENCY_LIMIT = 10
MAX_RETRIES = 3
REQUEST_TIMEOUT = 60000  # ms

# Selectors
SELECTORS = {
    "product_link": 'a[href*="/products/"]',
    "title": "h1",
    "current_price": ".text-tertiary.text-3xl",
    "regular_price_xpath": "//span[contains(text(), 'Rek.')] | //div[contains(text(), 'Nypris:')]",
    "mileage_xpath": "//*[contains(text(), 'ODO')]",
    "age_xpath": "//div[contains(text(), 'Årsmodell')]/following-sibling::div",
    "specs_tab_xpath": "//div[contains(text(), 'Specifikation')]",
    "load_more_xpath": "//button[contains(., 'VISA FLER')]",
    "list_view_xpath": "//button[@data-cy='plp-listview-button']",
}

# Storage Configuration
OUTPUT_DIR = "output"
OUTPUT_JSON_DIR = os.path.join(OUTPUT_DIR, "json")
OUTPUT_CSV_DIR = os.path.join(OUTPUT_DIR, "csv")
OUTPUT_HTML_DIR = os.path.join(OUTPUT_DIR, "reports")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
