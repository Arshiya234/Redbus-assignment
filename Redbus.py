from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time

driver = webdriver.Chrome()

driver.get("https://www.redbus.in/")
driver.maximize_window()
driver.save_screenshot('Launching_Application.png')
driver.implicitly_wait(30)
From_text_field = driver.find_element(By.ID,"src").send_keys("Mumbai")
time.sleep(2)
from_cities_suggestion_list = driver.find_elements(By.XPATH,"//ul[@class='sc-dnqmqq eFEVtU']//li")
option_from_cities_suggestion_list = driver.find_element(By.XPATH,"//text[text() = 'Borivali East']").click()
time.sleep(2)
Destination_text_field = driver.find_element(By.ID,"dest").send_keys("Bangalore")
time.sleep(2)
destination_cities_suggestion_list = driver.find_elements(By.XPATH,"//ul[@class='sc-dnqmqq eFEVtU']//li")
# for data in row_list2:
#     print(data.text)
option_dest_cities_suggestion_list = driver.find_element(By.XPATH, "//text[text() ='Indiranagar']").click()
time.sleep(2)
current_date = datetime.now() + timedelta(days=2)
formatted_date = current_date.strftime("%d-%m-%Y")
date_ = formatted_date[1] or formatted_date
day = f"//hr[@class='divider']/..//span[text()='{date_}']"
print(formatted_date)
print(date_)
Date_element = driver.find_element(By.XPATH,day).click()
time.sleep(5)
driver.execute_script("window.scrollTo(0,-100);")
driver.save_screenshot('Selecting_Cities_and_Date.png')
time.sleep(5)
search_button = driver.find_element(By.ID,"search_button").click()
time.sleep(5)
Seater_type_bus = driver.find_element(By.XPATH, "//label[text()='SEATER']").click()
time.sleep(5)
AC_type_bus = driver.find_element(By.XPATH, "//label[text()='AC']").click()
buses = driver.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
bus_list = [bus.text for bus in buses]
driver.save_screenshot('Availables_Buses.png')
prices = driver.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']/../..//div[@class='fare d-block']/child::span")
price_list = [price.text for price in prices]
d = {bus_list[index]: price_list[index] for index in range(len(bus_list))}
sort_d = sorted(d.items(), key=lambda x:x[-1])
convert_d = dict(sort_d)
sort_list = [[key, value] for key, value in convert_d.items()]
Bus = sort_list[0][0]
price = sort_list[0][1]
driver.save_screenshot('Bus_With_Min_Price.png')
print(Bus+" has the lowest fair of "+"Rs " +price+"/-")
time.sleep(2)
