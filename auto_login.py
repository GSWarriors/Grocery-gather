#first go to safeway webpage

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

#safeway credentials
email = "sid.punj@gmail.com"
password = ""

#head to safeway login page
driver.get("https://www.safeway.com/")
