import os
import csv
import requests
from bs4 import BeautifulSoup
import re

def save_to_file(company, name):
  file = open("{}.csv".format(name), mode = "w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for comp in company:
    writer.writerow(list(comp.values()))
  return

def get_html(URL):
  indeed_url = requests.get(URL)
  soup = BeautifulSoup(indeed_url.text, "html.parser")
  return soup

def get_name(PAGE):
  name = PAGE.find("span",{"class":"company"}).string
  name = re.sub("\|/*<>:?","",name)
  return name

def get_link(PAGE):
  LINK = (PAGE.find("a")["href"])
  return LINK

def get_data():
  return

os.system("clear")
alba_url = "http://www.alba.co.kr"
#svae_to_file("csv")

COMP_name = []
COMP_link = []
dict_company = {}
company = []

soup = get_html(alba_url)
pagination = soup.find("div", {"id":"MainSuperBrand"}).find("ul", {"class":"goodsBox"})

pages = pagination.find_all("li")

for page in pages[:-4]:
  COMP_name.append(get_name(page))
  COMP_link.append(get_link(page))

temp_link = COMP_link[0]
Ex = ["summaryView"]

for index, temp_link in enumerate(COMP_link):
  com_soup = get_html(temp_link)
  com_pagination = com_soup.find("div", {"id":"NormalInfo"}).find("tbody")
  com_pages = com_pagination.find_all("tr", class_=lambda x: x not in Ex)

  for com_page in com_pages:
    com_title = com_page.find("span", {"class":"company"}).string
    com_place = com_page.find("td", {"class": "local first"}).get_text()
    com_time = com_page.find("td", {"class":"data"}).string
    com_pay = com_page.find("span", {"class" : "payIcon"}).string + com_page.find("span", {"class" : "number"}).string
    com_date = com_page.find("td", {"class":"regDate last"}).string
    dict_company = {"place":com_place.replace(u'\xa0', u' '), "title": com_title, "time":com_time, "pay":com_pay, "date":com_date}
    company.append(dict_company)

  print(company)
  save_to_file(company, COMP_name[index])