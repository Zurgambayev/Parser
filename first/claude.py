from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException

def init_webdriver():
    driver = webdriver.Chrome()
    stealth(driver,
            platform="Win32",
            languages=["en-US", "en"],
            vendor="Google Inc.",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver



def find_and_click_last_element(driver):
    try:
        filter_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[data-testid^='catalog--selected-filter-brandIds-']"))
        )
        print('CLICKED')
        if filter_elements:
            last_element = filter_elements[-1]
            click_element(driver, last_element)
            time.sleep(5)
            return True
        return False
    except (StaleElementReferenceException, TimeoutException):
        print("Failed to find or click the last filter element.")
        return False

def scrape_items(driver):
    items = []
    while True:
        try:
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            feed_grid = soup.find('div', class_='feed-grid')
            
            if not feed_grid:
                print("Container with class 'feed-grid' not found.")
                break

            grid_items = feed_grid.find_all('div', class_='feed-grid__item')

            if not grid_items:
                print("No items found.")
                break

            print(f"Found {len(grid_items)} items.")

            for item in grid_items:
                product = {}
                product['seller_name'] = item.find('p', class_='web_ui__Text__text').text if item.find('p', class_='web_ui__Text__text') else None
                seller_link = item.find('a', class_='web_ui__Cell__link')
                product['seller_link'] = seller_link['href'] if seller_link else None
                image = item.find('img', class_='web_ui__Image__content')
                product['image_url'] = image['src'] if image else None
                title_element = item.find('a', class_='new-item-box__overlay')
                product['title'] = title_element['title'] if title_element else None
                price_element = item.find('p', class_='web_ui__Text__text web_ui__Text__caption')
                product['price'] = price_element.text if price_element else None
                items.append(product)

            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="catalog-pagination--next-page"]'))
            )

            if next_button.is_displayed() and next_button.get_attribute("aria-disabled") == "false":
                click_element(driver, next_button)
                time.sleep(2)
            else:
                print("End of pagination reached or button not active.")
                break

        except Exception as ex:
            print(f"Error while scraping items: {str(ex)}")
            break

    return items

try:
    driver = init_webdriver()
    driver.maximize_window()
    driver.get('https://www.vinted.com/')
    time.sleep(2)

    # Close initial modal
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='domain-select-modal-close-button']"))
    )
    click_element(driver, close_button)
    time.sleep(2)

    # Wait for 'Women' element to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "1904"))
    )
    print("Modal closed, 'Women' element is clickable")

    # Accept cookies
    accept = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    click_element(driver, accept)
    print("'Accept all' button was found and clicked")

    # Click 'Women' category
    women = driver.find_element(By.ID, "1904")
    click_element(driver, women)
    time.sleep(2)

    # Click 'All' link
    all_link = driver.find_element(By.CSS_SELECTOR, "a[data-testid='category-item-1904']")
    click_element(driver, all_link)
    time.sleep(2)

    # Click 'Brand' filter
    brand_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='catalog--brand-filter--trigger']"))
    )
    click_element(driver, brand_button)
    print("'Brand' button was clicked")

    # Find all brand items
    brand_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "pile__element"))
    )
    print(f"Found {len(brand_items)} brand items")

    products = []
    for i in range(len(brand_items)): 
        try:
            checkbox = WebDriverWait(brand_items[i], 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']"))
            )
            name_brand = WebDriverWait(brand_items[i], 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__title.web_ui__Text__left"))
            )
            print(f"Processing brand: {name_brand.text}")

            brand_dict = {
                "nameBrand": name_brand.text,
                "items": [],
                "cnt": 0
            }

            if not checkbox.is_selected():
                print(f"Attempting to click brand: {name_brand.text}")
                driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, -100);", brand_items[i])
                time.sleep(1)
                click_element(driver, brand_items[i])
                print(f"Clicked brand: {name_brand.text} (selected)")
                time.sleep(2)

                brand_dict['items'] = scrape_items(driver)
                brand_dict['cnt'] = len(brand_dict['items'])
                products.append(brand_dict)
                print(f"Brand and its items added. Total items: {brand_dict['cnt']}")

                if not find_and_click_last_element(driver):
                    print("Failed to unselect the brand. Moving to the next one.")
                time.sleep(2)

        except Exception as e:
            print(f"Failed to process brand {i}: {str(e)}")
            continue

    print("All brands processed.")
    with open('women.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(products, jsonfile, ensure_ascii=False, indent=4)
    print("Data saved to 'women.json'")

except Exception as ex:
    print(f"An error occurred: {str(ex)}")
finally:
    if 'driver' in locals():
        driver.close()
        driver.quit()