from selenium import webdriver
import time
import database


class ApartmentsParser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1377, 700)
        self.base_url = 'https://3dapartment.com/listings/rent'
        self.base_url_for_apartment_page = ''

    def open_greater_boston(self):
        self.driver.get(self.base_url)
        time.sleep(4)
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/section[1]/nav/div[1]/div[1]/div/span/select/option[2]'
        ).click()
        time.sleep(4)

    def get_list_by_neighborhoods(self, neighborhood_names: list):
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[1]/section[2]/section/header/div/div[2]/button'
            ).click()  # open filters
        except:
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[1]/section[2]/section/header/div/div[1]/button'
            ).click()
        time.sleep(2)
        for nb_name in neighborhood_names:
            self.driver.find_element_by_xpath("//input[@placeholder='enter the neighborhood']").send_keys(nb_name)
            time.sleep(3)
            item = self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/section[2]/section/div/div[2]'
                                                     '/div/div[2]/div[1]/div[6]/div[2]/div/div[2]/div/a[1]/span')
            item.click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/section[2]/section/div/div[2]/div/div[2]/div[1]/div[9]/div/div[3]/button'
        ).click()  # push Show button
        time.sleep(2)

    def save_on_page(self):
        time.sleep(3)
        address = self.driver.find_element_by_xpath('//div[@class=\'listing-address\']').text
        price = self.driver.find_element_by_xpath("//div[@class='price main-value']").text
        try:
            beds, baths = self.driver.find_elements_by_xpath("//div[@class='num main-value']")
        except ValueError:
            beds = '0'
            baths = self.driver.find_elements_by_xpath("//div[@class='num main-value']")
        nearest_subway_stations_count = len(self.driver.find_elements_by_xpath(
            "//div[@class='stations-cont']//div[@class='item']"
        ))
        is_active = self.driver.find_element_by_xpath(
            "//div[@class='listing-available-inform exclusive-listing-label']").text
        is_active_status = False
        if is_active == 'Available Now':
            is_active_status = True
        database.save_item_on_db(address, price, beds.text, baths.text, nearest_subway_stations_count, is_active_status)

    def save_apartment_list_new(self):
        links_array = []
        nums = self.driver.find_element_by_xpath("//a[@class='pagination-link is-current']").text
        for _ in range(int(nums)):
            elems = self.driver.find_elements_by_xpath("//a[@class='listing-grid-card']")
            for elem in elems:
                links_array.append(elem.get_attribute("href"))
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/section[2]/section/div/div[2]/div/nav/a[2]').click()
            time.sleep(4)

        for link in links_array:
            self.driver.get(link)
            time.sleep(4)
            self.save_on_page()


if __name__ == '__main__':
    a = ApartmentsParser()
    a.open_greater_boston()
    a.get_list_by_neighborhoods(['Brighton', 'Allston', 'North Brookline', 'Corey Hill', 'Griggs Park'])
    a.save_apartment_list_new()
