import requests
from bs4 import BeautifulSoup
import csv

def get_page(url):
    response = requests.get(url)


#Error log
    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

#Scrape for product details Name,Price,Amount.
def get_detail_data(soup):
    try:
        product = soup.find('span',{'class':'a-size-large product-title-word-break'}).text
    except:
        product = ''

    try:
        price = soup.find('span',{'class':'a-size-medium a-color-price priceBlockBuyingPriceString'}).text.strip()
        currency, price = p.split(' ')
    except:
        currency = ''
        price = ''
    try:
        amount = soup.find('span', class_='a-size-medium a-color-state').find('a').text

    except:
        amount = ''

    data = {
        'product': product,
        'price': price,
        'currency': currency,
        'amount': amount,
    }
    return data
#Find all links
def get_index_data(soup):
    try:
        links = soup.find_all('a',class_='a-link-normal a-text-normal')
    except:
        links = []
    urls = [item.get('href') for item in links]

    return urls

#Create csv file
def write_csv(data, url):
    with open('hardware.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['product'], data['price'], data['currency'], data['amount'], url]

        writer.writerow(row)



#The Url we want to scrape.
def main():
    url = 'https://www.amazon.se/s?k=grafikkort&page=1'

    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page('https://www.amazon.se' + link))
        write_csv(data, link)

if __name__ == '__main__':
    main()
