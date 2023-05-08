from selenium import webdriver
import time
from socket import timeout
from selenium import webdriver
import time
import time
import csv
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(r"C:\Users\abc\Desktop\driverchrome\chromedriver.exe",options=chrome_options)

script_arg = sys.argv[1]
key_f = open(script_arg,'r')
key_fi = key_f.read()

key_f = open("key_word.txt","w")
key_f.write(key_fi)
key_f.close()

ff = open("key_word.txt",'r')
ffa = ff.readlines()

for keyword_i in ffa:
# driver = webdriver.Chrome(a)  # Path to where I installed the web driver
    driver.get(f"https://www.google.com/search?q={keyword_i}&gs_lcp=Cgxnd&tbs=lf:1,lf_ui:2&tbm=lcl&rflfq")  ### Karnal School Data #####
    time.sleep(10)
    driver.save_screenshot("abs.jpg")

    field_names = ['School_Name', 'Address', 'Phone',"Image_url"]
    with open('Names.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()

    School_all_item = {}

    All_Controller = driver.find_elements(By.XPATH,"//div[@jscontroller='AtSb']")
    for controller in All_Controller:
        controller.click()
        time.sleep(2)
        try:
            school_name = driver.find_element(By.XPATH,"//div[@class='SPZz6b']").text
            print("School Name = ",school_name)
            School_all_item["School_Name"] = school_name
            item_names = driver.find_elements(By.XPATH,"//*[@class='Z1hOCe']")
            for item_name in item_names:
                name_item = item_name.text
                name_item =  name_item.split(":")
                School_all_item[name_item[0]]=name_item[1]
            # Image_find = driver.find_element(By.XPATH,'//div[@role="img"]').get_attribute("style")
            # Image_url = str(Image_find).split("url(")[1].split(")")[0].replace('"','')
            # print(Image_url)
            # School_all_item["Image_url"] = Image_url
            time.sleep(1)
        except:
            pass     
        with open('Names.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writerow(School_all_item)       
driver.quit()