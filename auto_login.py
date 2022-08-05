#first go to safeway webpage

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

os.environ["PASSWORD"] = "Gettingstuff#12"


#driver = webdriver.Chrome(ChromeDriverManager().install())
driver_options = Options()
driver_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driver_options)



#safeway credentials
email = "sid.punj@gmail.com"
password = os.environ["PASSWORD"]

#head to safeway login page
driver.get("https://www.safeway.com/")
"""signup_button = driver.find_element(By.CLASS_NAME, "menu-nav__profile-button")
signup_button.click()

signup_button2 = driver.find_element(By.ID, "sign-in-modal-link")
signup_button2.click()
print("signup button2: " + str(signup_button2))

#works! now enter email and password, and click the last "sign in" button
email_field = driver.find_element(By.ID, "label-email")
password_field = driver.find_element(By.ID, "label-password")
final_signin_button = driver.find_element(By.ID, "btnSignIn")

email_field.click()
email_field.send_keys(email)

password_field.click()
password_field.send_keys(password)

final_signin_button.click()"""


#load logfile.json and get first item (apple) entered in search box on safeway website.
file = open('logfile.json')
data = json.load(file)

first_elem = data['items'][0]
first_item = first_elem['value']

print("the first item: " + str(first_item))

search_bar = driver.find_element(By.ID, "skip-main-content")
search_bar.send_keys(first_item)
search_bar.send_keys(Keys.ENTER)

#for entry in data['items']:
#    print("entry: " + str(entry))
#    print("value: " + str(entry['value']))
#    print()



#search_button = driver.find_element(By.CLASS_NAME, "svg-icon svg-icon-search-grey")
#search_button.click()
