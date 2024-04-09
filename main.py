from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("D:\\python scripts\\Python programmes\\selenium\\digipplus_assignment\\data\\secret_key.json", scopes = scopes)

file = gspread.authorize(creds)
workbook = file.open("GMB_listing_data")
sheet = workbook.sheet1

f = open("./business_categories.txt")
business_categories = f.readlines()
f.close()

f = open("./country_capital.txt")
places = f.readlines()
f.close()

'''
name, rating, adress, phone.no, website_link
'''
adress_link = "https://www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png"
phone_no_link = "https://www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png"
website_link = "https://www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png"

block_a = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div["
block_b = "]/div/a"

name_a = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div["
name_b = "]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[1]/div[2]"

rating_a = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div["
rating_b = "]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[3]/div/span[2]/span/span[1]"

no_of_reviews_a = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div["
no_of_reviews_b = "]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[3]/div/span[2]/span/span[2]"

img_class = "Liguzb"

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps/")

def click_block(i):
    try:
        block = block_a + str(i) + block_b
        block_elem = driver.find_element(By.XPATH, block)
        block_elem.click()
        return 1
    except:
        print("Error finding block")
        return 0

def get_basic_info(i):
    # print(i);
    # path = patha + str(i) + pathb
    name = name_a + str(i) + name_b
    rating = rating_a + str(i) + rating_b;
    no_of_reviews = no_of_reviews_a + str(i) + no_of_reviews_b
    # adress = adress_a + str(i) + adress_b

    try:
        # print(path)
        name_elem = driver.find_element(By.XPATH, name)
        # print(name_elem.get_attribute("innerHTML"), end = " ")
        name_value = name_elem.get_attribute("innerHTML")
    except:
        name_value = ""

    try:
        # print(path)
        rating_elem = driver.find_element(By.XPATH, rating)
        # print(rating_elem.get_attribute("innerHTML"), end = " ")
        rating_value = rating_elem.get_attribute("innerHTML")
    except:
        rating_value = ""
    
    try:
        # print(path)
        reviews_elem = driver.find_element(By.XPATH, no_of_reviews)
        review_no_value = reviews_elem.get_attribute("innerHTML")
        # print(reviews_elem.get_attribute("innerHTML"), end = " ")
    except:
        review_no_value = ""
    
    return (name_value, rating_value, review_no_value)

    


def get_value(img):
    try:
        # driver.implicitly_wait(5)
        b = img.find_element(By.XPATH, "../../..")
        img_content = b.find_element(By.XPATH, "./div[2]/div[1]")
        img_value = img_content.get_attribute("innerHTML")
        # print(img_content.get_attribute("innerHTML"))
    except:
        img_value = ""
    
    return img_value

def get_adv_info():
    # driver.implicitly_wait(5)
    img_elem = driver.find_elements(By.CLASS_NAME, img_class)


    adress_value = ""
    phone_no_value = ""
    website_value = ""


    for img in img_elem:
        # print(a.get_attribute("src"))
        # print(img.get_attribute("src"))
        img_src = img.get_attribute("src")
        if ( img_src == adress_link):
            # driver.implicitly_wait(3)
            adress_value = get_value(img)
        
        
        if(img_src == phone_no_link):
            # driver.implicitly_wait(3)
            phone_no_value = get_value(img)
        
        

        if(img_src == website_link):
            driver.implicitly_wait(3)
            website_value = get_value(img)
    
    
    return (adress_value, phone_no_value, website_value)
    

row_count = 1
def search(category, place):
    global row_count
    search_key = category + " in " + place
    
    search_elem= driver.find_element(By.NAME, "q")
    search_elem.clear()
    search_elem.send_keys(search_key)
    search_elem.send_keys(Keys.RETURN)

    driver.implicitly_wait(3)




    for j in range(1,3):
        i = 2*j + 1
        sleep(2)
        name_value, rating_value,review_no_value = get_basic_info(i)
        sleep(2)
        click_block(i)
        sleep(3)


        adress_value, phone_no_value, website_link = get_adv_info()

        if (len(review_no_value) > 2):
            review_no_value = review_no_value[1:len(review_no_value)-1]

        value_list = [category, name_value, rating_value, review_no_value, adress_value, phone_no_value, website_link]
        rng = "A" + str(row_count) + ":G" + str(row_count)
        sheet.update(rng , [value_list])
        row_count += 1
        # print(f'{name_value} | {rating_value} | {adress_value} | {phone_no_value} | {website_link}')
        # print()

def start():
    n = 10
    for i in range(len(business_categories)):
        places_random = random.sample(places, n)
        for j in range(10):
            category = business_categories[i][:-1]
            place = places_random[j][:-1]
            search(category, place)

start()
    
# category = "Pizza"
# place = "Moscow, Russia"

# search(category, place)
# search("Gym", "Delhi, India")
    


