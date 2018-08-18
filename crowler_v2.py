import urllib.request
from bs4 import BeautifulSoup

def get_shopping_top_10():
    response = urllib.request.urlopen('https://search.shopping.naver.com/best100v2/main.nhn')
    soup = BeautifulSoup(response.read(), 'html.parser')
    item_list = soup.select('ul[id="popular_srch_lst"] > li > span > a')

    dict = {}
    for index, item in enumerate(item_list):
        dict[index+1] = item.text
    return dict