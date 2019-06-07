from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys


class WhatsappMessage:
    """
    class for sending message via Whatsappweb
    """

    def __init__(self, friends_lists, message, chromedriver_path, url="https://web.whatsapp.com/"):
        self.friends_lists = friends_lists
        self.message = message
        self.chromedriver_path = chromedriver_path
        self.url = url

    def send_message(self):
        "Method to send messages "
        driver = webdriver.Chrome(
            executable_path=self.chromedriver_path)
        driver.maximize_window()
        driver.get(self.url)
        wait = WebDriverWait(driver, 600)
        group_title = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='side']")))
        search = driver.find_elements_by_xpath(
            '//*[@id="side"]/div/div/label/input')[0]
        for friend in self.friends_lists:
            try:
                wait = WebDriverWait(driver, 5)
                search.clear()
                search.send_keys(friend)
                x_arg = f'//span[@title="{friend}"]'
                try:
                    group_title = wait.until(EC.presence_of_element_located((
                        By.XPATH, x_arg)))
                except Exception as e:
                    print(f"{friend} not identified!", e)
                else:
                    group_title.click()
                    message = driver.find_elements_by_xpath(
                        '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
                    message.send_keys(self.message)

                    try:
                        wait = WebDriverWait(driver, 2)
                        x_arg = '//*[@id="main"]/footer/div[1]/div[3]/button'
                        sendbutton = wait.until(EC.presence_of_element_located((
                            By.XPATH, x_arg)))
                    except Exception as e2:
                        print (e2)
                    else:
                        # pass
                        sendbutton.click()
            except Exception as e1:
                print ("final", e1)
                
        # driver.close()


# check for group names with icons
# check for unchatted contact

whatsapp_web_url = "https://web.whatsapp.com/"
chromedriver_path = 'C:\whatsapp-automate\src\chromedriver.exe'
friends_lists = ["Himanshi Swain", "No Title", "Save"]
message = "Test ping one more"

obj_whatsapp = WhatsappMessage(
    friends_lists, message, chromedriver_path, whatsapp_web_url)
obj_whatsapp.send_message()
