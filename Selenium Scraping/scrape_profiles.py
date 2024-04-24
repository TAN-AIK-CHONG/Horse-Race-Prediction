from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.chrome.options import Options
import time, json

# Read the JSON file
with open('horse_data.json', 'r') as file:
    horse_data:dict = json.load(file)

# Configure Chrome options for headless mode
options = Options()
options.headless = True

# Set up Selenium WebDriver with Chrome
driver = webdriver.Chrome(options=options)  
wait = WebDriverWait(driver, 10)  # Using explicit wait with a timeout of 10 seconds
df_list=[]

# Define the base URL and the number of pages
for name,url in horse_data.items():
    driver.get(url)
    
    # Wait until the table is present on the page
    while True: #page traversal
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table'))) #dont really need it
        time.sleep(4) #literally wait for the browser to load
        all_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.odd, .even')) )#selenium gets confused when elements are finished loading due to the way singapore turf loads their content
        for row in all_rows:
            try:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) < 18:  # Adjust the number as per your requirement
                    continue  # Skip processing this row
                row_data = {
                    'HorseName': name,
                    'Barrier': cells[8].text.strip(),
                    'CarriedWeight': cells[9].text.strip(),
                    'Distance': cells[5].text.strip(),
                    'Rating': cells[4].text.strip(),
                    'HorseWeight': cells[10].text.strip(),
                    'Going': cells[7].text.strip(),
                    'Track': cells[6].text.strip(),
                    'Jockey': cells[16].text.strip(),
                    'Trainer': cells[17].text.strip(),
                    'LBW': cells[12].text.strip(),
                }
                with open(f'horse_profiles.json', 'a') as f:
                    json.dump(row_data, f)
                    f.write('\n')
            except StaleElementReferenceException as e:
                continue
        all_rows.clear()
        if len(driver.find_elements(By.CLASS_NAME, 'paginate_button.next.disabled')) > 0: break #check if last page
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#DataTables_Table_0_next'))).click()

# Close the WebDriver
driver.delete_all_cookies()
driver.quit()

