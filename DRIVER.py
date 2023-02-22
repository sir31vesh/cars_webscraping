from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pyautogui
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
import mimetypes
from email import encoders
from email.mime.base import MIMEBase

l1 = []
l2 = []
l3 = []
l4 = []
l5 = []

l1.append('Name')
l2.append('year')
l3.append('price')
l4.append('running')
l5.append('link')


def scrape(name, transmission, fuel):
    driver = webdriver.Firefox(executable_path=r"C:\Users\Aryan Dande\Downloads\gecko\geckodriver.exe")
    urls = ["https://www.cars24.com/buy-used-car?sort=P&storeCityId=2423&pinId=411001","https://www.cardekho.com/used-cars+in+pune"]
    list = []
    for j in range(2):
        driver.maximize_window()
        if j == 1:
            driver.get(urls[j])
            time.sleep(2)  # Allow 2 seconds for the web page to open

            driver.find_element(By.CSS_SELECTOR, "[title^='"+fuel+"']").click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, "[title^='"+transmission+"']").click()
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, '[name="brand"]').click()
            time.sleep(3)
            pyautogui.typewrite(name)
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, "[title='"+name+"']").click()
            time.sleep(3)
            scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
            screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
            i = 1
            count=0

            while True:
                # scroll one screen height each time
                driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                time.sleep(scroll_pause_time)
                # update scroll height each time after scrolled, as the scroll height can change after we sc
                # rolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")
                # Break the loop when the height we need to scroll to is larger than the total scroll height
                if screen_height * i > scroll_height:
                    break

            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content,"html.parser")
            time.sleep(5)

            Name_year = soup.find_all("div", class_="gsc_col-xs-7 carsName", limit=100)
            for k in Name_year:
                temp_str1=""
                p1 = k.a.getText()
                temp2 = p1.split()
                l2.append(temp2[0])
                for l in range(1,len(temp2)):
                    temp_str1 += temp2[l]
                    temp_str1 += " "
                l1.append(temp_str1)
            list.append(l1)
            list.append(l2)
            Price = soup.find_all("span", class_="amnt", limit=100)
            for k in Price:
                l3.append(k.getText())
            list.append(l3)
            Fuel = soup.find_all("div", class_="truncate dotlist-2", limit=100)
            for k in Fuel:
                p = k.getText()
                temp = p.split()
                l4.append(temp[0])
            list.append(l4)

            link_list = soup.find_all("a", href=True)
            for link in link_list:
                t = link['href']
                if t[0:23] == "/used-car-details/used-":
                    l5.append("https://www.cardekho.com"+t)

            list.append(l5)

        elif j == 0:
            driver.get(urls[j])
            time.sleep(2)  # Allow 2 seconds for the web page to open
            driver.find_element(By.CSS_SELECTOR, '[class^="css-bg1rzq-control search-select__control"]').click()
            time.sleep(1)
            pyautogui.typewrite(name)
            pyautogui.press("enter")
            time.sleep(5)
            driver.find_element(By.XPATH, "//span[contains(text(),'More Filters')]").click()
            time.sleep(3)
            driver.find_element(By.XPATH, "//div[contains(text(),'"+transmission+"')]").click()
            time.sleep(3)
            driver.find_element(By.XPATH, "//div[contains(text(),'"+fuel+"')]").click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, '[type^="button"]').click()

            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(15)
            scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
            screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
            i = 1

            while True:
                # scroll one screen height each time
                driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                time.sleep(scroll_pause_time)
                # update scroll height each time after scrolled, as the scroll height can change after we scrolled the
                # page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")
                # Break the loop when the height we need to scroll to is larger than the total scroll height
                if (screen_height) * i > scroll_height:
                    break

            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, "html.parser")
            time.sleep(5)
            count = 0
            count1 = 0
            name_lis = soup.find_all("h2", class_="_3FpCg")
            for k in name_lis:
                x = k.getText()
                y = x[5:len(x)]
                w = x[0:4]
                l1.append(y)
                count1+=1
                l2.append(w)

            km_lis = soup.find_all("ul", class_="bVR0c")
            for m in km_lis:
                x = m.getText()
                temp = x.split()
                l4.append(temp[0])

            price_list = soup.find_all("div", class_="_7udZZ")
            for z in price_list:
                q = z.getText()
                l3.append(q[1:len(q)])

            link_list = soup.find_all("a", href=True)
            for link in link_list:
                t = link['href']
                count += 1
                if t[0:31] == "https://www.cars24.com/buy-used" and count > 119 and count1>0:
                    l5.append(t)
                    count1=count1-1

    my_df = pd.DataFrame(list)

    my_df1 = my_df.T
    my_df1.columns=['Name','Year','Price','running','Link']
    for i in my_df1[['Name']]:
        ad=my_df1[i]

        print(type(ad))
        l7=name.split()

        for p,q in ad.items():

            temp_str = str(q)
            l8 = temp_str.split()
            for k in range(len(l7)):
                if l7[k] == l8[k]:
                    continue
                else:
                    my_df1.drop([p],axis=0,inplace=True)
                    break

    my_df1.to_csv('my_csv.csv', index=False, header=False)


def send_mail(to):

    emailfrom = "automationtesting@gmail.com"
    emailto = to
    fileToSend = "my_csv.csv"
    username = "automationtesting00xd@gmail.com"
    password = "testing23#"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Here is your choice of cars "
    msg.preamble = "Pls find it"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()






