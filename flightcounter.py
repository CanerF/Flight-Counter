from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
import time
import sys
import pandas as pd


start_time = time.time()


# State the driver path, base_url and the path of text file
driver_path = "C:/Users/Caner Filiz/PycharmProjects/flightcounter/chromedriver.exe"
base_url = "https://flightaware.com/live/flight/{}/history"
txt_file = "C:/Users/Caner Filiz/PycharmProjects/flightcounter/code.txt"


# Read the text file
def read_txt(text):
    open_file = open(text, "r")
    registration_code_list = open_file.readlines()
    for Index in range(len(registration_code_list)):
        registration_code_list[Index] = registration_code_list[Index].replace("\n", "")
        registration_code_list[Index] = registration_code_list[Index].replace("-", "")
        open_file.close()
    return registration_code_list

def difference(now = datetime.strptime(datetime.now().strftime("%d-%b-%Y %I:%M%p"),"%d-%b-%Y %I:%M%p")):
    difference = (now-timedelta(days=1)).strftime("%d-%b-%Y %I:%M%p")
    return difference
print(difference())
# Open the Web Browser  & log in to the account
driver = webdriver.Chrome(executable_path=driver_path)
driver.get("https://flightaware.com/account/session")
driver.maximize_window()
time.sleep(1)
username = driver.find_element_by_css_selector(
    "#slideOutPanel > div.pageContainer > div > div.inline_form_box_content > div > form > div.creds > input[type=text]"
    ":nth-child(1)").send_keys("canerflz@gmail.com")
password = driver.find_element_by_css_selector(
    "#slideOutPanel > div.pageContainer > div > div.inline_form_box_content > div > form > div.creds > input[type=pass"
    "word]:nth-child(2)").send_keys("Caner1997.")
driver.find_element_by_css_selector("#slideOutPanel > div.pageContainer > div > div.inline_form_box_content > div > "
                                    "form > button").click()
print("User login is succesful!")
#read_txt("C:/Users/Caner Filiz/PycharmProjects/flightcounter/code.txt")

list_reg_code = []
list_flight_counter = []
for code in read_txt("C:/Users/Caner Filiz/PycharmProjects/flightcounter/code.txt"):
    driver.get(base_url.format(code))
    driver.implicitly_wait(5)
    date_elements = driver.find_elements_by_class_name("tablesaw-cell-content")
    if not date_elements:
        print("Tail ID: {} | Flights in 24h: {}".format(code, 0))
        list_reg_code.append(code)
        list_flight_counter.append(0)
        continue
#    time.sleep(3)
    date_list = []
    counter = 0
    for date in date_elements:
        if counter == 0:
            flight_date = ""
            flight_date += str(date.text)
            if "First" in flight_date:
                flight_date = flight_date.replace("First", "")
        elif counter == 4:
            flight_date_check = str(date.text).split(" ")[0]
            if flight_date_check == "First":
                flight_date += " " + str(date.text).split(" ")[2]
            else:
                flight_date += " " + str(date.text).split(" ")[0]
            date_list.append(flight_date)
        elif counter % 7 == 0 and counter != 0:
            flight_date = ""
            flight_date += str(date.text)
            counter = 1
            continue
        counter += 1
    flight_counter = 0
    for date in date_list:
        if datetime.strptime(date, "%d-%b-%Y %I:%M%p") > datetime.strptime(difference(), "%d-%b-%Y %I:%M%p"):
            flight_counter += 1
        else:
            print("Tail ID: {} | Flights in 24h: {}".format(code, flight_counter))
            list_reg_code.append(code)
            list_flight_counter.append(flight_counter)
            flight_counter = 0
            break
driver.quit()

dataframe = pd.DataFrame({'Registration Codes': list_reg_code, 'Number of Flights': list_flight_counter})
dataframe.to_excel(r'C:/Users/Caner Filiz/Desktop/data_output.xlsx', index=False)

print("--- %s seconds ---" % (time.time() - start_time))