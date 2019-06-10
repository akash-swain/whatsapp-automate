from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import configparser
import os


class WhatsappMessage:
    """
    class for sending message via Whatsappweb
    """

    def __init__(self):
        "Configure app-data and user-data"
        self.friends_lists, self.message = self.get_config(
            'userconfig.ini', 'DEFAULT', 'FRIENDS', 'MESSAGE')
        self.url, self.chromedriver_path = self.get_config(
            'appconfig.ini', 'DEFAULT', 'WHATSAPP_WEB_URL', 'CHROMEDRIVER_PATH')

    def get_config(self, filename, config_section, *config_parameters):
        "Returns a list of configured values in filename passed"
        config = configparser.ConfigParser()
        config = configparser.ConfigParser()
        config_file = os.path.join(
            os.path.dirname(__file__), filename)
        config.read(config_file)
        parameter_value_list = []
        for i in config_parameters:
            parameter_value_list.append(config[config_section][i])
        return parameter_value_list

    def send_message(self):
        "Method to send messages"
        driver = webdriver.Chrome(
            executable_path=self.chromedriver_path)
        driver.maximize_window()
        driver.get(self.url)
        wait = WebDriverWait(driver, 600)
        group_title = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='side']")))
        search = driver.find_elements_by_xpath(
            '//*[@id="side"]/div/div/label/input')[0]
        for friend in eval(self.friends_lists):
            try:
                search.clear()
                search.send_keys(friend)
                x_arg = f'//span[contains(@title,"{friend}")]'
                try:
                    wait = WebDriverWait(driver, 5)
                    group_title = wait.until(EC.presence_of_element_located((
                        By.XPATH, x_arg)))
                    # print(group_title.text)
                except Exception as e:
                    print(f"{friend} not identified!", e)
                else:
                    group_title.click()
                    message = driver.find_elements_by_xpath(
                        '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
                    message.send_keys(eval(self.message))

                    try:
                        wait = WebDriverWait(driver, 2)
                        x_arg = '//*[@id="main"]/footer/div[1]/div[3]/button'
                        sendbutton = wait.until(EC.presence_of_element_located((
                            By.XPATH, x_arg)))
                    except Exception as e2:
                        print(e2)
                    else:
                        # pass
                        sendbutton.click()
            except Exception as e1:
                print("final", e1)
                continue

        driver.close()

