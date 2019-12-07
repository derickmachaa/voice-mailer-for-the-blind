from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def browser(application,emailacc,password):
    if(application == '1'):
        web=webdriver.Firefox(executable_path='./bin/geckodriver',service_log_path='./tmp/log.txt')
    elif(application == '2'):
        options=Options()
        options.binary_location = './bin/chromedriver'
        web=webdriver.Chrome(options=options)
    url='https://accounts.google.com/signin'
    web.get(url)
    sleep(3)
    emailelement=web.find_element_by_xpath('//*[@id="identifierId"]')
    emailelement.send_keys(emailacc)
    sleep(1)
    web.find_element_by_xpath("//*[@id=\"identifierNext\"]/span/span").click()
    sleep(3)
    passwordelement=web.find_element_by_xpath("//*[@id=\"password\"]/div[1]/div/div[1]/input")
    web.implicitly_wait(20)
    passwordelement.send_keys(password)
    web.find_element_by_xpath("//*[@id=\"passwordNext\"]/span/span").click()
    sleep(3)
    url='https://myaccount.google.com/lesssecureapps'
    web.get(url)
    sleep(3)
    toggle_element=web.find_element_by_xpath('/html/body/c-wiz/div/div[3]/c-wiz/div/div[3]/div[1]/div/div/div/div[2]/div/div[3]/div')
    web.implicitly_wait(20)
    toggle_element.click()
    sleep(3)
    url="https://accounts.google.com/Logout"
    web.get(url)
    sleep(2)
    web.close()
