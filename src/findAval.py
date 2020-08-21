# to find availability of a 512 gb macbook pro
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

# threading stuff:
import threading
def main():
    t = threading.Timer(60, main)
    t.start()
    check(t)

def found(location):
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()

    # Authentication
    s.login("rayhanfahmed@gmail.com", os.environ.get('EMAIL_PASSWORD'))

    # message to be sent
    message = 'Congrats we have found your order in New Hampshire. Check the apple for education website to order'
    print('FOUND: at '+ location)
    # sending the mail
    s.sendmail("rayhanfahmed@gmail.com", "ashlanahmed@gmail.com", message)
    s.sendmail("rayhanfahmed@gmail.com", "rayhanfahmed@gmail.com", message)

    # terminating the session
    s.quit()

def check (t):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path='/Users/rayhanahmed/Desktop/Coding Projects/AppleProductNotificationBot/src/chromedriver',
        options=chrome_options)

    # get list of stores
    driver.get('https://www.apple.com/us-hed/shop/buy-mac/macbook-pro/13-inch-space-gray-2.0ghz-quad-core-processor-with-turbo-boost-up-to-3.8ghz-512gb#')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="check-availability-search-section"]/div/div/div/div/button').click()
    driver.find_element_by_id('ii_searchreset').send_keys('03060')
    driver.find_element_by_xpath('//*[@id="as-retailavailabilitysearch-searchbutton"]/span').click()

    # check availability:
    time.sleep(2)
    counter = 0
    #Only searches through top 3 because anything farther away is outside of New Hampshire
    while (counter<3):
        counter += 1
        message = (driver.find_element_by_xpath('//*[@id="as-retailavailabilitysearch-storelist"]/li[{}]/label/div[3]/div[2]'.format(counter)).text)
        if (message=='Unavailable for Pickup'):
            message = (driver.find_element_by_xpath('//*[@id="as-retailavailabilitysearch-storelist"]/li[{}]/label/div[3]/div[2]'.format(counter)).text)
            if (counter == 2):
                print('not found checking again in 60 secs')
                driver.close()
        else:
            location = (driver.find_element_by_xpath('//*[@id="as-retailavailabilitysearch-storelist"]/li[{}]/label/div[2]/span[2]'.format(counter)).text)
            # Note: Location is just the closest availability to the zip code entered, may not be every availability though.
            location = "Congrats! We have found an availability for your macbook pro and airpods at: " + location
            found(location)
            driver.close()
            sys.exit()
main()

