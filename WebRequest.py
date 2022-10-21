from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def web_request(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    driver.implicitly_wait(1)
    driver.get(url)

    return driver

def click_more(driver):
    while True:
        try:
            btn_more = driver.find_element(by=By.CSS_SELECTOR, value="button.historyPage_button__HbUS_")
            btn_more.click()
        except:
            break

def load_data_by_soup(soup):
    pick_list = soup.select(".historyPage_historyListBodyCol___et1p")

    if pick_list[0].text == "아직 뽑기 내역이 없습니다.":
        return -1
    if len(pick_list) < 1:
        return -1

    gatcha = list()
    for i in range(0, len(pick_list), 4):
        gatcha.append({"item_name": pick_list[i + 1].text, "card_name": pick_list[i + 2].text,
                       "timestamp": pick_list[i + 3].text})

    return gatcha[:-1]

def run_all(url):
    driver = web_request(url)
    if driver.title != "뽑기내역확인 - NGELGAMES":
        return False

    click_more(driver)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()

    gatcha = load_data_by_soup(soup)



    # gatcha = load_data(driver)
    return gatcha
