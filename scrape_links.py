from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time, json

URL = 'https://racing.turfclub.com.sg/en/horse-performance/'
driver = webdriver.Chrome()  # Choose Chrome (you can choose anything)
wait = WebDriverWait(driver, 10)  # Using explicit wait with a timeout of 10 seconds

driver.get(URL)
horses = {}
verbose = True
json_file = True

while True:  # Page traversal
    time.sleep(3)  # Wait for the browser to load
    all_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.odd td.sorting_1 a, .even td.sorting_1 a')))
    for link in all_links:
        try:
            horse_name = link.text.strip()
            horse_link = link.get_attribute('href')
            if horse_name:
                horses[horse_name] = horse_link
        except StaleElementReferenceException as e:
            continue
    all_links.clear()
    if len(driver.find_elements(By.CLASS_NAME, 'paginate_button.next.disabled')) > 0:
        break  # Check if last page
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#DataTables_Table_0_next'))).click()

driver.delete_all_cookies()
driver.quit()  # Close the driver gracefully

if verbose:
    for horse_name, horse_link in horses.items():
        print(horse_name, horse_link)

# Write data to JSON file
if json_file:
    with open('horse_data.json', 'w') as json_f:
        json.dump(horses, json_f, indent=4)
