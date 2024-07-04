from selenium import webdriver
import time
import yagmail
import os

def get_driver():
  options=webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches",["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")
  driver=webdriver.Chrome(options=options)
  driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
  return driver
  
def cleantext(text):
  output=text.split(" ")[0]
  return float(output)

def sendmail(text):
  sender=os.getenv('SENDER_EMAIL')
  receiver=os.getenv("RECERIVER_EMAIL")
  subject="Stock price alert"
  contents=f"""The Stock Price is Now {text}"""
  yag = yagmail.SMTP(user=sender, password=os.getenv('PASSWORD'))
  yag.send(to=receiver, subject=subject, contents=contents)
  print("Email Sent!")


def main():
  driver=get_driver()
  time.sleep(2)
  element = driver.find_element(by="xpath",value='//*[@id="app_indeks"]/section[1]/div/div/div[2]/span[2]')
  seperatedtext=cleantext(element.text)
  if(seperatedtext<0.10):
    sendmail(str(cleantext))