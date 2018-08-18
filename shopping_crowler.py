from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome('chromedriver', chrome_options=options)

def get_shopping_top_10():
    driver.get('https://search.shopping.naver.com/best100v2/main.nhn') 
    dict = {}
    for i in range(1, 11):
        xpath = "//*[@id='popular_srch_lst']/li[%d]/span[1]/a" % i
        dict[i] = driver.find_element_by_xpath(xpath).text
    return dict