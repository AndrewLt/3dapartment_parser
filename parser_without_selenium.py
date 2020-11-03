import requests
import database
import time
from bs4 import BeautifulSoup


class Parser:
    @classmethod
    def get_list_of_rental_items(cls, offset=0):
        check_url = 'https://3dapartment.com/api/v1/listings/search?ne%5Blat%' \
                     '5D=42.364370655633074&ne%5Blng%' \
                     '5D=-71.06648580114529&sw%5Blat%' \
                     '5D=42.32948101404932&sw%5Blng%' \
                     '5D=-71.2293924478738&' \
                     f'zoom=13&is_map_main=true&offset={str(offset)}&limit=10&sort=default&' \
                     'neighborhoods%5B0%5D=21&neighborhoods%5B1%5D=45&' \
                     'neighborhoods%5B2%5D=132&neighborhoods%5B3%5D=104&' \
                     'neighborhoods%5B4%5D=156&neighborhoods%5B5%5D=23&' \
                     'neighborhoods%5B6%5D=42&neighborhoods%5B7%5D=47&' \
                     'neighborhoods%5B8%5D=433&neighborhoods%5B9%5D=335&' \
                     'neighborhoods%5B10%5D=98&neighborhoods%5B11%5D=153&' \
                     'is_no_fee=false&is_furnished=false&is_pet_friendly=false&' \
                     'is_tour=false&is_available_now=false&group_id=2&saleType=rent'
        result = requests.get(check_url)
        data = result.json()
        listing = data['data']['items']
        data_listing = []
        for item in listing:
            if item['type'] == 'listings':
                data_listing = item['items']
        return data_listing

    @classmethod
    def get_info_about_flats(cls):
        offset = 0
        while True:
            result = cls.get_list_of_rental_items(offset=offset)
            if result:
                offset += 10
                cls.save_flat_to_db(result)
                time.sleep(1)
            else:
                break

    @classmethod
    def save_flat_to_db(cls, flat_list: list):
        for flat in flat_list:
            address = f"{flat['building_number']['title']}, {flat['street']['title']}, #{flat['unit']}"
            price = str(flat['price'])
            beds = str(flat['beds'])
            baths = str(flat['baths'])
            nearest_subway_stations_count = cls.get_nums_of_subway_stations(flat['link'])
            is_active = flat['is_active']
            database.save_item_on_db(address, price, beds, baths, nearest_subway_stations_count, is_active)

    @classmethod
    def get_nums_of_subway_stations(cls, link):
        url = f'https://3dapartment.com/{link}'
        result = requests.get(url)
        soup = BeautifulSoup(result.content, 'html.parser')
        subway = soup.find_all('div', {"class": "item"})
        try:
            subway = len(subway)
        except Exception:
            subway = 0
        return str(subway)


neighborhoods_list = [21, 45, 132, 104, 156, 23, 42, 47, 433, 335, 98, 153]


if __name__ == '__main__':
    a = Parser()
    a.get_info_about_flats()
