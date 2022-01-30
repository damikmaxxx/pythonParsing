from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import keyboard as keyb
import time

# settings
__SITE = "site"
__SEARCH_NAME = "searchName"
__MAX_PRICE = "maxPrice"
__MIN_PRICE = "minPrice"
__SHOW_INTERFACE = "showInterface"

__EMAIL = "email"

# parsing info
__NAME = "name"
__PRICE = "price"
__URL = "url"


def avito(settings):
    name_price = []
    options = webdriver.ChromeOptions()

    if not settings[__SHOW_INTERFACE]:
        options.headless = True
        options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.avito.ru/")
    input_elem = driver.find_elements(By.CLASS_NAME, "input-input-Zpzc1")
    input_elem[0].send_keys(settings[__SEARCH_NAME])
    input_elem[0].send_keys(Keys.RETURN)
    driver.find_element(By.XPATH, "//input[@data-marker='price/to']").send_keys(settings[__MAX_PRICE])
    driver.find_element(By.XPATH, "//input[@data-marker='price/from']").send_keys(settings[__MIN_PRICE])
    driver.find_element(By.XPATH, "//input[@data-marker='search-form/by-title']/..").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//button[@data-marker='search-filters/submit-button']").click()
    items = driver.find_elements(By.XPATH, "//div[@data-marker='item']")
    count = 0
    try:
        count = int(driver.find_element(By.XPATH, "//span[@data-marker='page-title/count']").text)
    except NoSuchElementException:
        with open("infoParsing.txt", 'w', encoding="utf-8") as f:
            f.write("SITE: " + settings[__SITE] + "      ")
            f.write("SEARCH NAME: " + settings[__SEARCH_NAME] + "      ")
            f.write("MIN_PRICE: " + str(settings[__MIN_PRICE]) + "      ")
            f.write("MAX_PRICE: " + str(settings[__MAX_PRICE]) + "₽\n\n")
            f.write("Nothing found")
            return False
    print("4")
    for i in range(0, count):

        name = items[i].find_element(By.TAG_NAME, "h3").text
        price = items[i].find_element(By.CLASS_NAME, "price-text-_YGDY").text
        print(name + " " + str(price))
        if not price.replace("₽", "").replace(" ", "").isnumeric():
            continue
        items[i].click()
        driver.switch_to.window(driver.window_handles[1])
        url = driver.current_url
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # driver.switch_to.window(driver.window_handles[])
        name_price.append({__NAME: name, __PRICE: price, __URL: url})

    print(name_price)
    # with open("infoParsing.txt", 'r', encoding="utf-8") as f:
    #     for line in f:
    #         _line = line.rstrip()
    #         key = _line.split(":")[0]
    #         value = _line.split(":")[1]
    #         if key == __SITE:
    with open("infoParsing.txt", 'w', encoding="utf-8") as f:
        f.write("SITE: " + settings[__SITE] + "      ")
        f.write("SEARCH NAME: " + settings[__SEARCH_NAME] + "      ")
        f.write("MIN_PRICE: " + str(settings[__MIN_PRICE]) + "      ")
        f.write("MAX_PRICE: " + str(settings[__MAX_PRICE]) + "₽\n\n")
        for obj in name_price:
            print(obj)
            _name, _price, _url = obj[__NAME], obj[__PRICE], obj[__URL]
            print(_name + _price + _url)
            f.write(_name + " "*(55 - len(_name)) + _price + " "*(10 - len(_price)) + _url + '\n')


def dns(settings):
    name_price = []
    options = webdriver.ChromeOptions()
    if not settings[__SHOW_INTERFACE]:
        options.headless = True
        options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def get_settings():
    settings_info = {}
    with open("Settings.txt", 'r', encoding="utf-8") as f:
        for line in f:
            _line = line.rstrip()
            key = _line.split(":")[0]
            value = _line.split(":")[1]
            if key == __SITE:
                settings_info[key] = value
            if key == __SHOW_INTERFACE:
                try:
                    if (int(value) == 0) or (value.lower() == "false"):
                        settings_info[key] = False
                    else:
                        settings_info[key] = True
                except:
                    settings_info[key] = True
            # avito
            if key == __SEARCH_NAME:
                settings_info[key] = value
            if key == __MAX_PRICE:
                settings_info[key] = int(value)
            if key == __MIN_PRICE:
                settings_info[key] = int(value)

            # for dns
            if key == __EMAIL:
                settings_info[key] = value

    return settings_info


def main():
    def print_pressed_keys(e):
        print(e, e.event_type, e.name)
    keyb.hook(print_pressed_keys)
    while True:
        try:
            settings_info = get_settings()
            if settings_info[__SITE] == "avito":
                avito(settings_info)
            time.sleep(5)
        except:
            continue


if __name__ == "__main__":

    main()
