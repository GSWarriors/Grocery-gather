#first go to safeway webpage

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import requests
import difflib
import time

os.environ["PASSWORD"] = ""

def main():

    driver_options = Options()
    driver_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driver_options)
    driver.get("https://www.safeway.com/")



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


    #load logfile.json and get first item (apple) entered in search box on safeway website.
    file = open('logfile.json')
    data = json.load(file)

    first_elem = data['items'][0]
    first_item = first_elem['value']
    print("the first item from my grocery list: " + str(first_item))

    #for loop for going through all items in item list.
    #for entry in data['items']:
    #    print("entry: " + str(entry))
    #    print("value: " + str(entry['value']))
    #    print()


    #use the postman url for safeway to login, make sure the cookie is correct- will need to add that as variable too (later)
    url = "https://www.safeway.com/abs/pub/xapi/search/products?request-id=8116991186014&url=https://www.safeway.com&pageurl=https://www.safeway.com&pagename=search&rows=30&start=0&search-type=keyword&storeid=767&featured=true&search-uid=uid%253D1741673301335%253Av%253D12.0%253Ats%253D1659718319673%253Ahc%253D2&q=" + first_item + "&sort=&userid=41053869549&featuredsessionid=&screenwidth=782&dvid=web-4.1search&pp=true&user_id=41053869549&channel=pickup&banner=safeway"

    headers = {
      'authority': 'www.safeway.com',
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'adrum': 'isAjax:true',
      'cookie': 'visid_incap_1610353=1pXLDVBbSgyrYfiOswvWSTcy42IAAAAAQUIPAAAAAAB/GUHk1p65xEqFOXu/i356; _gcl_au=1.1.1184972799.1659056697; safeway_ga=GA1.2.1011543139.1659056697; _pin_unauth=dWlkPVptSmtPVFpoTkdZdFlXUmlOUzAwTVdGaExUbGhaalV0Tm1FMll6QmhNelJqTldReg; aam_uuid=22060803095681610201811891922264708611; _ga=GA1.1.1011543139.1659056697; __gsas=ID=61ea8edb28e8edbf:T=1659056847:S=ALNI_Mak_aXFOmmJcr2YS5N-8FNpdCxktQ; ECommBanner=safeway; AMCVS_A7BF3BC75245ADF20A490D4D%40AdobeOrg=1; at_check=true; SAFEWAY_MODAL_LINK=; s_cc=true; visid_incap_1712622=v7T7dKhASx2Re0OBopiPiX5Y6GIAAAAAQUIPAAAAAAC2wsMbywMyHKiavkEYZ1xb; nlbi_1712622=oWo9cH8EUj95H6wSgd9NwAAAAACx7zd+jDw91yWwj4+0Tdv0; incap_ses_975_1712622=k3RBQUV4BzPAiq8vC+aHDX5Y6GIAAAAA7kt829rAG7fXbbCltBSXyw==; SAFEWAY_RE_SIGN_IN=false; nlid=9d8571aa|1267d746; incap_ses_1161_1610353=C6hYD2Sbu33BY0FDA7QcEC906WIAAAAAxkAQaK1rcxjHGzlA8cDVtw==; SAFEWAY_KMSI=true; okta-oauth-redirect-params={"responseType":"code","state":"fun-bedroom-perry-bernardo","nonce":"nprLWuLUGw72E6SpbG8Od5kU3xqeFNJUUguRRsqarzSLqCUCU6X8CZynKuTDIiDE","scopes":["openid","profile","email","offline_access","used_credentials"],"urls":{"issuer":"https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6","authorizeUrl":"https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/authorize","userinfoUrl":"https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/userinfo"}}; okta-oauth-nonce=nprLWuLUGw72E6SpbG8Od5kU3xqeFNJUUguRRsqarzSLqCUCU6X8CZynKuTDIiDE; okta-oauth-state=fun-bedroom-perry-bernardo; ECommSSOActive=Y; ECommReInit=net; sapientHitCounter=2; s_sq=%5B%5BB%5D%5D; incap_ses_975_1610353=VpoRRJq7+Vkm5AcyC+aHDQpK7WIAAAAAeCLFn87f9aR8Z+cQTUCW4g==; SWY_SYND_USER_INFO=%7B%22firstName%22%3A%22%22%2C%22hhid%22%3A%22990060422113%22%2C%22storeAddress%22%3A%226150+Bollinger+Rd%2C+San+Jose%2C+CA+95129%22%2C%22storeId%22%3A%22767%22%2C%22storeZip%22%3A%2295129%22%2C%22preference%22%3A%22DUG%22%7D; abs_previouslogin=%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22houseId%22%3A%22990060422113%22%2C%22clubCard%22%3A%2241053869549%22%2C%22userType%22%3A%22R%22%2C%22banner%22%3A%22safeway%22%2C%22preference%22%3A%22DUG%22%2C%22isClosed%22%3A%22false%22%2C%22isCrossBannerMFCUser%22%3A%22false%22%2C%22isARenrolled%22%3A%22false%22%2C%22userData%22%3A%7B%7D%7D%2C%22SHOP%22%3A%7B%22storeId%22%3A%22767%22%2C%22zipcode%22%3A%2295129%22%2C%22address%22%3A%226150+Bollinger+Rd%2C+San+Jose%2C+CA+95129%22%2C%22userData%22%3A%7B%22signInCalled%22%3Afalse%2C%22driveUpAndGoIsEnabled%22%3A%22false%22%2C%22unattendedDeliveryIsEnabled%22%3A%22false%22%7D%7D%2C%22J4U%22%3A%7B%22storeId%22%3A%22767%22%2C%22zipcode%22%3A%2295129%22%2C%22address%22%3A%226150+Bollinger+Rd%2C+San+Jose%2C+CA+95129%22%2C%22userData%22%3A%7B%7D%7D%7D%7D; ECommSignInCount=0; SWY_SHARED_PII_SESSION_INFO=%7B%22version%22%3A%221%22%2C%22jti%22%3A%22AT.Td7ozA4p5GoXKaLiz2Vej_dqAbyT0Ud4eMBIPhXQALI.oar1kbfp1wskrPIi72p7%22%2C%22issuer%22%3A%22https%3A%2F%2Falbertsons.okta.com%2Foauth2%2Fausp6soxrIyPrm8rS2p6%22%2C%22audience%22%3A%5B%22Albertsons%22%5D%2C%22uniqueId%22%3A%2200u81zxz9ang2SjJL2p7%22%2C%22scope%22%3A%5B%22offline_access%22%2C%22profile%22%2C%22openid%22%2C%22email%22%5D%2C%22name%22%3A%22Siddartha%22%2C%22gid%22%3A%22520-000-0990060422113%22%2C%22uuid%22%3A%22358f0deb-4dab-4556-b05d-e2155ce2b9c8%22%2C%22userData%22%3A%7B%7D%7D; SWY_SHARED_SESSION=%7B%22accessToken%22%3A%22eyJraWQiOiJxYkpsN1lDa2NiYW5nNzlUWURYNk5HOER4Y2hhY2tPdG9tenVPVURqaFA4IiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULlRkN296QTRwNUdvWEthTGl6MlZlal9kcUFieVQwVWQ0ZU1CSVBoWFFBTEkub2FyMWtiZnAxd3NrclBJaTcycDciLCJpc3MiOiJodHRwczovL2FsYmVydHNvbnMub2t0YS5jb20vb2F1dGgyL2F1c3A2c294ckl5UHJtOHJTMnA2IiwiYXVkIjoiQWxiZXJ0c29ucyIsImlhdCI6MTY1OTcxODE1NiwiZXhwIjoxNjU5NzIwODU2LCJjaWQiOiIwb2FwNmt1MDFYSnFJUmRsNDJwNiIsInVpZCI6IjAwdTgxenh6OWFuZzJTakpMMnA3Iiwic2NwIjpbIm9mZmxpbmVfYWNjZXNzIiwicHJvZmlsZSIsIm9wZW5pZCIsImVtYWlsIl0sImF1dGhfdGltZSI6MTY1OTU1MzE5NywiemlwIjoiOTUxMjkiLCJzdWIiOiJzaWQucHVuakBnbWFpbC5jb20iLCJoaWQiOiI5OTAwNjA0MjIxMTMiLCJkbm0iOiJTaWRkYXJ0aGEiLCJhbG4iOiI0MTA1Mzg2OTU0OSIsImdpZCI6IjUyMC0wMDAtMDk5MDA2MDQyMjExMyIsImVjYyI6IjQxMDUzODY5NTQ5IiwiYXBzaSI6IlkiLCJsbm0iOiJQdW5qIiwianByIjoiIiwidXVpZCI6IjM1OGYwZGViLTRkYWItNDU1Ni1iMDVkLWUyMTU1Y2UyYjljOCIsImJhbiI6InNhZmV3YXkiLCJzdHIiOiI3NjciLCJ1bm0iOiJzaWQucHVuakBnbWFpbC5jb20iLCJwaG4iOiIiLCJiaWQiOiIiLCJhdnMiOiJZIn0.SrSAlBvVlrk80AUZxCSyXxCV5NZbsN_UsP8Gq5R6V3MNegMnu32bjZUBDXvPg30olpUWYB_Sgt69al8LK5NUcXIJTIj837R4fqqr9KC9tboGR-ZB77VAKPUeM6NzUh58bE52CGfMWtuYy7EbuaRqL3Nlv3XZzpPmRoMhUiNVXZKYrD9iph_khc1svF__CaN-pGeFFLGm7vilqhpBK4Z-2k69t6rnEraS7ZpDo8O14rvezLbpniS0YFZjNCTKSgwhyzGEe-rOYTbQpdqFYVVEk_X2jBHV-NmhCZK_RbSXoOQuBIEeYUH3JL0cZ39h0wfGp6Rn8v93LDxnhdg9sN0Bnw%22%2C%22refreshToken%22%3A%22ZlcHQS69Qrxir_qKrq7mqEnR9kmSdPEqQ56-qkuZsqE%22%2C%22issueTime%22%3A1659718156000%2C%22expireTime%22%3A1659720856000%7D; AMCV_A7BF3BC75245ADF20A490D4D%40AdobeOrg=-1124106680%7CMCIDTS%7C19210%7CMCMID%7C14572575991802793841405554439541398695%7CMCAAMLH-1660322956%7C9%7CMCAAMB-1660322956%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1659725356s%7CNONE%7CvVersion%7C5.2.0%7CMCCIDH%7C-748839835; s_vncm=1662015599190%26vn%3D1; s_ivc=true; reese84=3:fP8IaDFhSS7t10h4/Zl1YA==:fob15hfG3JUV0TsWpaVPJCtItlApy4in81khRNkfq+cEijOzl2Gkvem4ERDh/jX9k7zmjNi2I5Lh1hhURmzilOm+Q2jeuS7m5KkcYeJg6nQ+X3s0ZQE/A7ywjEkZNJkjjq3Bmmvdt3DfWT7YJvEknN3DJtJ1puqDIJQFica1HXub78IKYPlnPV728nurVt+ZkcuXl984sRQHgbkve9rirTBmDxg4q3V3ophdvGm0aAZSn0vYBUGllCDO3ykV0pyM7BfLQt6XIYe4X4fC/H846lz1fPGPkT1jQbRnCXzfCZtFHLHr0K8kWRK/29NbMCern2GgL9J1+ZwJazyEjAd2dvtUDN4+g3beCIJLwKeHEckRzxbtpDUSmlKiMGTeaJmNOCOcfe+raS0Nk5OdD2Z5IG2G6kf5M+epbkL5b7oqTTujAAm/2R7cfvNdnDH0aeH6JMFhNgRoywnji8/16bbEyH4o378Cwf+bjFwgyb7TAeY=:1+YY2txSvcu8cZLE6dsN7j2iKEedSDD8fBGtq1FUXfM=; safeway_ga_gid=GA1.2.1895759369.1659718158; nlbi_1610353=A118eWnZyRhaSbzt6eNT2gAAAAAmfsEsOOYkDb4/d4qWO8kf; _gat_gtag_UA_172784514_2=1; SWY_SHARED_SESSION_INFO=%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22houseId%22%3A%22990060422113%22%2C%22clubCard%22%3A%2241053869549%22%2C%22userType%22%3A%22R%22%2C%22banner%22%3A%22safeway%22%2C%22preference%22%3A%22DUG%22%2C%22isClosed%22%3A%22false%22%2C%22isCrossBannerMFCUser%22%3A%22false%22%2C%22isARenrolled%22%3A%22false%22%2C%22userData%22%3A%7B%7D%7D%2C%22SHOP%22%3A%7B%22storeId%22%3A%22767%22%2C%22zipcode%22%3A%2295129%22%2C%22address%22%3A%226150+Bollinger+Rd%2C+San+Jose%2C+CA+95129%22%2C%22userData%22%3A%7B%22signInCalled%22%3Afalse%2C%22driveUpAndGoIsEnabled%22%3A%22false%22%2C%22unattendedDeliveryIsEnabled%22%3A%22false%22%2C%22expireTime%22%3A%221659720856000%22%7D%7D%2C%22J4U%22%3A%7B%22storeId%22%3A%22767%22%2C%22zipcode%22%3A%2295129%22%2C%22address%22%3A%226150+Bollinger+Rd%2C+San+Jose%2C+CA+95129%22%2C%22userData%22%3A%7B%7D%7D%7D%7D; _clck=17t8qkj|1|f3r|0; _ga_LZL2CD3SX2=GS1.1.1659718328.1.0.1659718328.0; nlbi_1610353_2147483392=8qNSP44hjxZAWqRW6eNT2gAAAACMrUi/oMJQkEU+yLtlV4p9; s_nr30=1659718329751-New; gpv_Page=safeway%3Adelivery%3Asearch-results; _uetsid=8c2dd23014de11edacda356453061a25; _uetvid=8c2dff2014de11ed887acb56e9acb6dc; _br_uid_2=uid%3D1741673301335%3Av%3D12.0%3Ats%3D1659718319673%3Ahc%3D2; _clsk=13b8lf1|1659718330290|2|0|i.clarity.ms/collect; ADRUM=s=1659718336644&r=https%3A%2F%2Fwww.safeway.com%2Fshop%2Fsearch-results.html%3Fhash%3D1470976975; mbox=session#64289efc96114480847bbf7f6de1521b#1659720198|PC#64289efc96114480847bbf7f6de1521b.35_0#1722963138; nlbi_1610353=/Fj8Fux2fVAwitR36eNT2gAAAADKj+vG3C/KG2NJiurzSN73',
      'ocp-apim-subscription-key': 'e914eec9448c4d5eb672debf5011cf8f',
      'referer': 'https://www.safeway.com/shop/search-results.html?q=' + first_item + '',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }

    r = requests.request("GET", url, headers=headers)
    data = json.loads(r.text)
    #print(r.text)

    #save this request output to JSON file
    with open('safeway_search.json', 'w') as f:
        json.dump(data, f)

    #open file for reading and parse items from file

    f = open('safeway_search.json', "r")
    data = json.load(f)

    item_list = data['response']['docs']

    time.sleep(5)
    check_inventory_and_match(first_item, item_list, driver)






"""For now, only adding first item from search to shopping list, assuming safeway has good match algo"""
def check_inventory_and_match(first_item, item_list, driver):

    #check if search results returned something and the inventory is available for the item
    #once we verify this, have the item searched in safeway search bar and click "add button"


    if (item_list[0]['inventoryAvailable'] == "1") and (len(item_list) >= 1):
        #add this item to cart. the button id is addButton_pid
        pid = item_list[0]['pid']
        add_button_name = "addButton_" + str(pid)
        print("the add button name: " + str(add_button_name))


        #need to wait sometime before doing this
        search_bar = driver.find_element(By.ID, "skip-main-content")
        search_bar.click()
        search_bar.send_keys(first_item)
        search_bar.send_keys(Keys.ENTER)

        time.sleep(3)
        add_button = driver.find_element(By.ID, add_button_name)
        add_button.click()

        #loops through whole item list
        #for i in range(0, len(item_list)):
        #    print("safeway page item name: " + str(item_list[i]['name']))
        #    print("safeway page product id: " + str(item_list[i]['pid']))
        #    print()







main()
