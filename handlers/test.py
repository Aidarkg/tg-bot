import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://debank.com/ranking?page=1"

driver = webdriver.Chrome()
driver.get(url)

try:
    # Находим элемент <img> внутри указанного <div>
    img_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '(//div[@class="db-user-avatar-container is-clickable"]/img)[2]'))
    )

    # Получаем ссылку на изображение (атрибут 'src' элемента <img>)
    img_src = img_element.get_attribute('outerHTML')

    pattern = r'logo/([^/]+)'

    # Поиск по регулярному выражению
    match = re.search(pattern, img_src)

    if match:
        extracted_string = match.group(1)
        print(extracted_string)
    else:
        print("Совпадения не найдены")


    # Печатаем ссылку на изображение
    # print("Ссылка на изображение:")
    # print(img_src)

finally:
    driver.quit()
