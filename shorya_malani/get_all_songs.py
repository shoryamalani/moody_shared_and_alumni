from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import requests
from sys import argv
def set_up_driver(chromedriver_path):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(  options=options)
    return driver
def clickable(el,wait):
    return wait.until(expected_conditions.element_to_be_clickable(el))

def main(chromedriver_path,url):
    with set_up_driver(chromedriver_path) as driver:
        driver.set_window_size(1000, 10000)
        driver.get(url)
        time.sleep(60)
        wait = WebDriverWait(driver,20)
        # clickable((By.CLASS_NAME,"listPage"),wait)
        full_list = driver.find_elements(By.CLASS_NAME,"title")
        songs = []
        for song in full_list:
            songs.append(song.text.replace("\n"," "))
        final_songs = []
        for song in songs:
            if song != "":
                final_songs.append(song.replace("&", " and "))
    with set_up_driver(chromedriver_path) as driver:
        wait = WebDriverWait(driver,10)
        driver.get("https://www.mp3juices.cc")
        for song in final_songs:
            query_spot = clickable((By.ID,"query"),wait)
            query_spot.send_keys(song)
            clickable((By.ID,"button"),wait).click()
            try:
                result = clickable((By.ID,"result_1"),wait)
                result.find_element_by_class_name("download").click()
                not_done = True
                while not_done:
                    if clickable((By.CLASS_NAME,"progress"),wait).text == "The file is ready. Please click the download button to start the download.":
                        not_done = False
                        r = requests.get(clickable((By.CLASS_NAME,"url"),wait).get_attribute("href"), allow_redirects=True)
                        with open(song.replace(" ","_")+".mp3",'wb+') as f: 
                            f.write(r.content) 
            except:
                driver.get("https://www.mp3juices.cc")
                query_spot = clickable((By.ID,"query"),wait)
                query_spot.send_keys(song.split()[:5])
                clickable((By.ID,"button"),wait).click()
                try:
                    result = clickable((By.ID,"result_1"),wait)
                    result.find_element_by_class_name("download").click()
                    not_done = True
                    while not_done:
                        if clickable((By.CLASS_NAME,"progress"),wait).text == "The file is ready. Please click the download button to start the download.":
                            not_done = False
                            r = requests.get(clickable((By.CLASS_NAME,"url"),wait).get_attribute("href"), allow_redirects=True)
                            with open(song.replace(" ","_")+".mp3",'wb+') as f: 
                                f.write(r.content) 
                except:
                    pass
            driver.get("https://www.mp3juices.cc")
            
            
if __name__ == "__main__":
	main("",argv[1])