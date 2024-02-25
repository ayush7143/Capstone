import requests
from bs4 import BeautifulSoup
import time
from forex_python.converter import CurrencyRates

def get_exchange_rate(base_currency, target_currency):
    c = CurrencyRates()
    return c.get_rate(base_currency, target_currency)

def convert_to_inr(price, exchange_rate):
    return round(price * exchange_rate, 2)

cities = [
    "https://rentberry.com/apartments/s/austin-tx",
    "https://rentberry.com/apartments/s/fort-myers-fl",
    "https://rentberry.com/apartments/s/buffalo-ny",
    "https://rentberry.com/apartments/s/dallas-tx",
    "https://rentberry.com/apartments/s/jersey-city-nj",
    "https://rentberry.com/apartments/s/las-vegas-nv",
    "https://rentberry.com/apartments/s/miami-fl",
    "https://rentberry.com/apartments/s/orlando-fl",
    "https://rentberry.com/ca/apartments/s/ottawa-on-canada",
    "https://rentberry.com/ca/apartments/s/vancouver-bc-canada",
    "https://rentberry.com/ca/apartments/s/toronto-on-canada",
    "https://rentberry.com/apartments/s/hoboken-nj",
    "https://rentberry.com/apartments/s/fort-lauderdale-fl",
    "https://rentberry.com/apartments/s/long-beach-ca",
    "https://rentberry.com/apartments/s/mesa-az",
    "https://rentberry.com/apartments/s/phoenix-az",
    "https://rentberry.com/apartments/s/san-francisco-ca",
    "https://rentberry.com/apartments/s/san-jose-ca",
    "https://rentberry.com/au/apartments/s/sydney-nsw-australia",
    "https://rentberry.com/au/apartments/s/brisbane-qld-australia",
    "https://rentberry.com/au/apartments/s/perth-wa-australia",
    "https://rentberry.com/apartments/s/pittsburgh-pa",
    "https://rentberry.com/apartments/s/fort-lauderdale-fl"
]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
currentPage = 1
currentCity = 0

while currentCity < len(cities):
    city = cities[currentCity] if currentPage == 1 else cities[currentCity] + "?page=" + str(currentPage)
    print("------- Scrapping url --------------")
    print(city)
    print("Current Page: ", currentPage)
    print("-----------------------------------")
    
    page = requests.get(city, headers=headers)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Pull all text from the BodyText div
    apartments = soup.find(class_='apartments')
    items = apartments.findAll(class_='apartment-item')

    for item in items:
        priceEl = item.find(class_='property-card-bottom-price')
        addressEl = item.find(class_='property-card-bottom-address')
        labels = item.findAll(class_='labels__item')
        if priceEl:
            price = float(priceEl.find('p').contents[0].replace('$', '').replace(',', ''))  # Extract numeric value
            base_currency = 'USD'  #prices are in USD
            target_currency = 'INR'
            exchange_rate = get_exchange_rate(base_currency, target_currency)
            converted_price = convert_to_inr(price, exchange_rate)

            address = addressEl.find('a')
            print("Price: ", converted_price, " INR")
            print("Address: ", address.contents[0] if address else "N/A")
            print("Bedroom: ", str(labels[0].contents[0]) if labels and len(labels) > 0 else "N/A")
            print("Washroom: ", str(labels[1].contents[0]) if labels and len(labels) > 1 else "N/A")
            print("Area: ", str(labels[2].contents[0]) if labels and len(labels) > 2 else "N/A")
            print("")

    if(currentPage == 10):
        currentCity += 1
        currentPage = 0
    
    currentPage += 1
