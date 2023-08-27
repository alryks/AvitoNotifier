from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from undetected_chromedriver import Chrome

from settings import LINK, include, exclude


def wait(driver):
    try:
        waitDriver = WebDriverWait(driver, 10)
        waitDriver.until(EC.presence_of_element_located((By.CLASS_NAME, "styles-module-theme-CRreZ")))
    except:
        driver.stop_client()
        driver.quit()


def parse():
    driver = Chrome(headless=True)

    links = []

    page = 0
    while True:
        page += 1

        driver.get(LINK + str(page))
        wait(driver)
        sleep(2)

        linksContainer = driver.find_element(By.CSS_SELECTOR, '[data-marker="catalog-serp"]')
        if not linksContainer.text.strip():
            break

        items = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, '[data-marker="item-title"]').get_attribute('href')
            name = item.find_element(By.CSS_SELECTOR, '[style="-webkit-line-clamp:2"]').text
            description = item.find_element(By.CSS_SELECTOR, '[style="-webkit-line-clamp:4"]').text
            text = (name + '\n' + description).lower()
            if all([any([i in text for i in in_.split('\n')]) for in_ in include]) and not any([in_ in text for in_ in exclude.split('\n')]):
                links.append(link)

    driver.stop_client()
    driver.quit()

    return links