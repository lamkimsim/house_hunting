import pandas as pd
import numpy as np
import os
import time
import undetected_chromedriver as uc  # Link: https://github.com/ultrafunkamsterdam/undetected-chromedriver

from datetime import datetime
from tqdm import tqdm
from datetime import datetime
from twocaptcha import TwoCaptcha

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
        self.area = area
        self.URL = 'https://www.iproperty.com.my/sale/all-residential/?q={}'.format(self.area)
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.driver.get(self.URL)

    def search_lots(self):
        lots = self.driver.find_elements(by=By.XPATH, value='//div[@data-test-id="Hyperlink"]')
        data = pd.DataFrame()
        for lot in lots:
            lot.click()
            time.sleep(2)

            location = self.driver.find_element(by=By.XPATH, value='//h1').text
            price = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[1]').text
            bedroom = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/div[2]/div/div[1]/div[1]/ul/li[1]').text
            bathroom = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/div[2]/div/div[1]/div[1]/ul/li[2]').text
            carpark = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/div[2]/div/div[1]/div[1]/ul/li[3]').text

            details = self.driver.find_elements(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemContainer-dPQXaS GilNZ"]//div')
            for temp in details:
                if temp.text == 'Property Type:':
                    property_type = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Land Title:':
                    land_title = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Bumi Lot:':
                    bumi_lot = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Tenure:':
                    tenure = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Built-up Size:':
                    build_up_size = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Furnishing:':
                    furnishing = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Occupancy:':
                    occupancy = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Facing Direction:':
                    facing_direction = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Unit Type:':
                    unit_type = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Posted Date:':
                    posted_date = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text
                if temp.text == 'Reference No.:':
                    referemceNo = temp.find_element(by=By.XPATH, value='//div[@class="PropertyDetailsListstyle__AttributeItemData-jpQfWB HUTFZ"]').text

            link = self.driver.current_url

            print("==> {}".format(location))

            temp_data = {"location": location,
                         "price": price,
                         "property_type": property_type,
                         "bedroom": bedroom,
                         "bathroom": bathroom,
                         "carpark": carpark,
                         "land_title": land_title,
                         "furnishing": furnishing,
                         "tenure": tenure,
                         "bumi_lot": bumi_lot,
                         "build_up_size": build_up_size,
                         "occupancy": occupancy,
                         "facing_direction": facing_direction,
                         "unit_type": unit_type,
                         "posted_date": posted_date,
                         "link": link,
                         "referemceNo": referemceNo}
            temp = pd.DataFrame(temp_data, index=[0])
            if data.empty:
                data = temp
            else:
                data = pd.concat([data, temp])

            if os.exists('{}_Result.csv'.format(self.area)):
                data.to_csv('{}_Result.csv'.format(self.area), index=False, mode='a', header=None)
            else:
                data.to_csv('{}_Result.csv'.format(self.area), index=False)
            self.driver.back()
            time.sleep(2)

        return data

    def run(self):
        print("==> Scrapping {} Area ...".format(self.area))
        self.search_lots()


if __name__ == "__main__":
    obj = PropertyGuru("Subang")
    obj.run()
