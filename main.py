from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

#parameters to change
LONG = 3
AGAIN = 10

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://orteil.dashnet.org/experiments/cookie/")


end = time.time() + (60 * LONG)

cookie = driver.find_element(By.ID, 'cookie')
check = time.time() + AGAIN

while True:
    cookie.click()
    # Check after 5 sec
    if time.time() > check:
        items = driver.find_elements(By.CSS_SELECTOR, '#store b')

    # all items in dict price - name {15: 'buyCursor', 100: 'buyGrandma'
        all_items = {}
        for i in items:
            price = i.text.split(' - ')
            if price == ['']:
                break
            cost = int(price[1].replace(",", ""))
            all_items[cost] = 'buy' + price[0]
        print(all_items)

    # check money vs price with all_items dict. , list with price, one max price
        money = driver.find_element(By.ID, 'money').text.replace(',', '')
        available = [i for i, j in all_items.items() if int(money) > i]
        maks = max(available)
        # ID of most expensive
        to_buy_item = all_items[maks]

        # cliiknij w najdroższe czyli z maxa
        driver.find_element(By.ID, to_buy_item).click()

    #znowu dodać 5 sek do odliczania
        check = time.time() + AGAIN

    #kiedy koniec petli

    if time.time() > end:

        cookie_per_s = driver.find_element(By.ID, "cps").text
        note = f"Time: {LONG} min, check: {AGAIN} sec, cookie per second: {cookie_per_s}\n"
        print(note)
        amount = driver.find_elements(By.CLASS_NAME, 'amount')
        for i in amount:
            print(i.text)
        with open('cookie-data.txt', 'a') as file:
            file.write(note)
        break
