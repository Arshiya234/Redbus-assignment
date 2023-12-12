from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

application_url = 'https://www.redbus.in/'

starting_location_name = 'Mumbai'
destination_location_name = 'Bangalore'

from_cities_suggestion_xpath = '//*[@class="sc-dnqmqq eFEVtU"]//li//text[1]'
destination_cities_suggestion_xpath = '//ul[@class="sc-dnqmqq eFEVtU"]//li//text[1]'

one_option_from_starting_location = 'Borivali East'
one_option_from_destination_location = 'Indiranagar'

month_dates_xpath = '//div[contains(@class,"DatePicker__CalendarContainer")]//div[contains(@class,"DayTilesWrapper__RowWrap")]//span//span[1]'
single_date_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09']

search_button_xpath = '//button[@id="search_button"]'
page_title = 'Search Bus Tickets'

bus_types_filters_xpath = "//ul[@class='list-chkbox']//li/label[2]"

first_filter_name = 'SEATER'
second_filter_name = 'AC'

all_filtered_buses_xpath = '//parent::div//preceding::div[contains(@class,"travels")]'
filtered_buses_price_xpath = '//ul[@class="bus-items"]//*[contains(@class,"seat-fare ")]//span'

scrolling_element_one_xpath = "(//*[contains(text(),'ARRIVAL TIME')])[1]"
scrolling_element_two_xapth = "//*[contains(text(),'To view')]"

def launching_application():
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(application_url)
    # time.sleep(2)
    driver.save_screenshot('Launching_Application.png')

def selecting_cities():
    driver.find_element(By.ID,"src" ).send_keys(starting_location_name)
    time.sleep(2)
    From_cities_suggestion_list = driver.find_elements(By.XPATH, from_cities_suggestion_xpath)

    for city in From_cities_suggestion_list:
        try:
            if city.text == one_option_from_starting_location:
                city.click()
                time.sleep(1)
        except:
            pass
    driver.find_element(By.ID, "dest").send_keys(destination_location_name)
    time.sleep(2)
    Destination_cities_suggestion_list = driver.find_elements(By.XPATH, destination_cities_suggestion_xpath)
    for city in Destination_cities_suggestion_list:
        try:
            if city.text == one_option_from_destination_location:
                city.click()
                time.sleep(1)
        except:
            pass


def selecting_date_and_search_buses():
    month_dates = driver.find_elements(By.XPATH, month_dates_xpath)
    current_date = str(datetime.now().date()).split('-')[2]

    for date in month_dates:
        try:
            if current_date in single_date_list:
                current_date = str(str(datetime.now().date()).split('-')[2])[1]
                if date.text == str(current_date):
                    date_after_current_date = month_dates.index(date) + 2
                    month_dates[date_after_current_date].click()
                    break
            else:
                if date.text == str(current_date):
                    date_after_current_date = month_dates.index(date) + 2
                    month_dates[date_after_current_date].click()
                    break
        except:
            pass

    for i in range(5):
        action = ActionChains(driver)
        action.send_keys(Keys.ARROW_UP).perform()

    driver.save_screenshot('Selecting_Cities_and_Date.png')

    search_button = driver.find_element(By.XPATH, search_button_xpath)
    search_button.click()
    WebDriverWait(driver, 25).until(EC.title_is(page_title))
    WebDriverWait(driver, 25).until(EC.presence_of_all_elements_located((By.XPATH, bus_types_filters_xpath)))
    # time.sleep(5)


def filter_the_buses():
    bus_type_filters = driver.find_elements(By.XPATH, bus_types_filters_xpath)
    for filter in bus_type_filters:
        if filter.text.startswith(first_filter_name):
            filter.click()
        elif filter.text.strip().startswith(second_filter_name):
            filter.click()
    driver.execute_script("window.scrollTo(0,100);")
    driver.save_screenshot('Availables_Buses.png')


def capture_buses_on_lowest_fare():
    scrolling_element_two = driver.find_element(By.XPATH, scrolling_element_two_xapth)
    driver.execute_script("arguments[0].scrollIntoView();", scrolling_element_two)

    filtered_bus_prices = driver.find_elements(By.XPATH, filtered_buses_price_xpath)
    filtered_bus_prices_list = []
    all_filtered_buses_name_list = []

    for price in filtered_bus_prices:
        filtered_bus_prices_list.append(float(price.text))

    minimum_bus_fare = min(filtered_bus_prices_list)
    index_minimum_bus_fare_index = filtered_bus_prices_list.index(minimum_bus_fare)
    bus_names = driver.find_elements(By.XPATH, filtered_buses_price_xpath + all_filtered_buses_xpath)

    for bus_name in bus_names:
        all_filtered_buses_name_list.append(bus_name.text)
    bus_name_with_lowest_price = bus_names[index_minimum_bus_fare_index].text

    action = ActionChains(driver)
    action.move_to_element(filtered_bus_prices[index_minimum_bus_fare_index]).perform()
    time.sleep(2)
    driver.save_screenshot('Bus_With_Min_Price.png')
    print('Bus Name With Lowest Fare : ', bus_name_with_lowest_price)
    print(all_filtered_buses_name_list)

def closing_application():
   driver.close()

launching_application()
selecting_cities()
selecting_date_and_search_buses()
filter_the_buses()
capture_buses_on_lowest_fare()
closing_application()
