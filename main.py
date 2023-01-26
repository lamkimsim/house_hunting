import pandas as pd
import numpy as np
import pickle
import time
import undetected_chromedriver as uc  # Link: https://github.com/ultrafunkamsterdam/undetected-chromedriver

from datetime import datetime
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from sys import platform
from datetime import datetime
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class PropertyGuru(object):
    def __init__(self, area):
        self.URL = 'https://www.propertyguru.com.my/property-for-sale'
        self.area = area
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.driver.get(self.URL)

    def get_url(self):
        ads_btn = self.driver.find_elements(by=By.XPATH, value="//div[@class='bottom-ad']//a")
        if (len(ads_btn) > 1):
            ads_btn[0].click()
        else:
            pass

        search_field = self.driver.find_element(by=By.XPATH, value="(//input[@name='freetext'])[1]")
        search_field.send_keys(self.area)
        search_field.send_keys(Keys.RETURN)
        time.sleep(3)

        total_page = int(self.driver.find_element(by=By.XPATH, value='//li//a[@rel="nofollow"]').text)
        scrapped_df = pd.read_csv('Housing_Link.csv')
        scrapped_page = scrapped_df[scrapped_df['Area'] == self.area]['Page'].max()

        for i in range(scrapped_page, total_page + 1):
            url = 'https://www.propertyguru.com.my/property-for-sale/{}?freetext={}&search=true'.format(i, self.area)
            self.driver.get(url)
            # try:

            # except:
            # pass
            temp_link = self.driver.find_elements(by=By.XPATH, value='//section[@class = "main-content spotlight-gray"]//div[@class = "gallery-container"]//a')
            for link in temp_link:
                print('==> {} : {}'.format(i, link.get_attribute('href')))
                temp = {'Area': self.area,
                        'Page': i,
                        'URL': link.get_attribute('href')}
                data_link = pd.DataFrame(temp, index=[0])
                data_link.to_csv('Housing_Link.csv', index=False, mode='a', header=None)
        return None

    def search_by_url(self):
        scrapped_df = pd.read_csv('Housing_Link.csv')
        total_results_link = scrapped_df['scrapped_df'].unique().tolist()
        data = pd.DataFrame()
        for url in total_results_link:
            print("==> {}".format(url))
            self.driver.get(url)
            property_type = self.driver.find_element(by=By.XPATH, value="(//div[@class='section-content'])[2]//tbody[1]").text

            if 'Residential Land' not in property_type:
                lot_title = self.driver.find_element(by=By.XPATH, value="//meta[@name='description']").get_attribute("content")
                price = self.driver.find_element(by=By.XPATH, value="//span[@class = 'element-label price']").text
                bedroom = int(self.driver.find_element(by=By.XPATH, value="//span[@itemprop='numberOfRooms']").text)
                bathroom = int(self.driver.find_element(by=By.XPATH, value="//div[@class='property-info-element baths']").text)
                sqft = int(self.driver.find_element(by=By.XPATH, value="//div[@itemprop='floorSize']//meta[@itemprop='value']").get_attribute("content"))
                psf = self.driver.find_element(by=By.XPATH, value="(//div[@class='section-content'])[2]//tbody[3]").text
                furnishing = self.driver.find_element(by=By.XPATH, value="(//div[@class='section-content'])[2]//tbody[4]").text
                tenure = self.driver.find_element(by=By.XPATH, value="(//div[@class='section-content'])[2]//tbody[5]").text
                build_year = self.driver.find_element(by=By.XPATH, value="(//div[@class='section-content'])[2]//tbody[6]").text
                listing_id = self.driver.find_element(by=By.XPATH, value="(//div[@class='section-content'])[2]//tbody[7]").text

                temp_data = {"lot_title": lot_title,
                             "price": price,
                             "property_type": property_type,
                             "bedroom": bedroom,
                             "bathroom": bathroom,
                             "sqft": sqft,
                             "psf": psf,
                             "furnishing": furnishing,
                             "tenure": tenure,
                             "build_year": build_year,
                             "listing_id": listing_id}
                temp = pd.DataFrame(temp_data, index=[0])

                if data.empty:
                    data = temp
                else:
                    data = pd.concat([data, temp])
            else:
                pass

        return data

    def run(self):
        print("==> Scrapping {} Area ...".format(self.area))
        self.get_url()
        # scrapped_data = self.search_by_url()
        # print(scrapped_data)


if __name__ == "__main__":
    obj = PropertyGuru("Subang")
    obj.run()
