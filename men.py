from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
import schedule

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

def parser():
    try:
        driver = init_webdriver()
        driver.maximize_window()
        driver.get('https://www.vinted.com/')
        time.sleep(6)
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='domain-select-modal-close-button']"))
        )
        close_button.click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "1904"))
        )
        
        print("Модальное окно закрыто, элемент 'Men' доступен для клика")
        # Поиск и клик по кнопке "Accept all"
        # accept_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        # )
        # accept_button.click()

        accept = driver.find_element(By.ID,"onetrust-accept-btn-handler").click()
        print("Кнопка 'Accept all' была найдена и кликнута")
        men = driver.find_element(By.ID,"5").click()
        time.sleep(5)
        all_link = driver.find_element(By.CSS_SELECTOR, "a[data-testid='category-item-5']").click()
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    
        brand_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='catalog--brand-filter--trigger']"))
        )
        brand_button.click()
        print("Кнопка 'Brand' была нажата")

        brand_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pile__element"))
        )
        print(len(brand_items))
        products = []
        cnt2 = 0
        for i in range(len(brand_items)): 
            try:
            
                checkbox = WebDriverWait(brand_items[i], 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']"))
                )
                nameBrand = WebDriverWait(brand_items[i], 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__title.web_ui__Text__left"))
                )
                print(nameBrand.text)  
                brand_dict = {
                    "nameBrand": nameBrand.text,
                    "items": [],  
                    "cnt" : 0
                }
                if not checkbox.is_selected(): 
                    print(f"Попытка клика по бренду: {brand_items[i].text}")
                    brand_items[i].click()
                    print(f"Клик по бренду: {brand_items[i].text} (выбран)")
                    print(checkbox.is_selected())
                    time.sleep(2)  
                    
                    WebDriverWait(driver, 10).until(
                        lambda driver: checkbox.is_selected()
                    )
                    cnt = 0 
                    flag = False
                    while True:
                        try:
                            cnt = cnt + 1
                            print(cnt)
                            html_content = driver.page_source
                            soup = BeautifulSoup(html_content, 'html.parser')
                            feed_grid = soup.find('div', class_='feed-grid')
                            if feed_grid:
                                print("Контейнер с классом 'feed-grid' найден.")
                            else:
                                print("Контейнер с классом 'feed-grid' не найден.")
                                break
                            
                            items = feed_grid.find_all('div', class_='feed-grid__item')

                            if items:
                                print(f"Найдено {len(items)} элементов.")
                            else:
                                print("Элементы не найдены.")
                                flag = True
                                break

                            for item in items:
                                product = {}
                                
                                seller_name_element = item.find('p', class_='web_ui__Text__text')
                                if seller_name_element:
                                    product['seller_name'] = seller_name_element.text
                                else:
                                    product['seller_name'] = None
                                
                                seller_link_element = item.find('a', class_='web_ui__Cell__link')
                                if seller_link_element:
                                    product['seller_link'] = seller_link_element['href']
                                else:
                                    product['seller_link'] = None
                                
                                image_url_element = item.find('img', class_='web_ui__Image__content')
                                if image_url_element:
                                    product['image_url'] = image_url_element['src']
                                else:
                                    product['image_url'] = None
                         
                                title_element = item.find('a', class_='new-item-box__overlay')
                                if title_element:
                                    product['title'] = title_element['title']
                                else:
                                    product['title'] = None
                            
                                price_element = item.find('p', class_='web_ui__Text__text web_ui__Text__caption')
                                if price_element:
                                    product['price'] = price_element.text
                                else:
                                    product['price'] = None
                                
                                brand_dict['items'].append(product)
                          
                            next_button = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="catalog-pagination--next-page"]'))
                            )
                            
                           
                            if next_button.is_displayed() and next_button.get_attribute("aria-disabled") == "false":
                                next_button.click()  
                                time.sleep(5) 
                            else:
                                print("Конец пагинации достигнут или кнопка не активна.")
                    

                        except Exception as ex:
                            print(f"Кнопка 'Следующая страница' не найдена или другая ошибка: {ex}")
                    brand_dict['cnt'] = len(brand_dict['items'])
                    products.append(brand_dict)
                    print(f"Бренд и его товары добавлены.")
                    if flag:
                        print('Возвращаемся к бренду и пытаемся повторить действия.')
                        time.sleep(5)
                        brand_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='catalog--brand-filter--trigger']"))
                        )
                        brand_button.click()
                        time.sleep(5)
                        print ("heheheheheheheheheh")
                        brand_items = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "pile__element"))
                        )   
                        brand_items[0].click()
                        # print(checkbox.is_selected())
                        print("lelelo")

                    print(f"Клик по бренду: {brand_items[0].text} (снят выбор)")
                    
                    time.sleep(2) 
                    continue
            except Exception as e:
                print(f"Не удалось кликнуть по бренду: {brand_items[i].text} - {e}")

        print("Все бренды выбраны.")
        with open('men.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(products, jsonfile, ensure_ascii=False, indent=4)
        print("Данные сохранены в 'men.json'")

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    schedule.every().day.at('19:24').do(parser)

    while True:
        schedule.run_pending()
    
    
if __name__ == '__main__':
    main()