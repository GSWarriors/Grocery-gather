#first go to safeway webpage

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.environ["PASSWORD"] = ""


#driver = webdriver.Chrome(ChromeDriverManager().install())
driver_options = Options()
driver_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driver_options)



#safeway credentials
email = "sid.punj@gmail.com"
password = os.environ["PASSWORD"]

#head to safeway login page
driver.get("https://www.safeway.com/")
signup_button = driver.find_element(By.CLASS_NAME, "menu-nav__profile-button")
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

final_signin_button.click()




#email = driver.find_element(By.id("label-email"))
#print("email: " + str(email))
