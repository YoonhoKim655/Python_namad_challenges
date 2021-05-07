import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"
indeed_url = requests.get(url)
tds_name = []
tds_code = []
cont = False

print("Hello! Please choose select a country by number:")

soup = BeautifulSoup(indeed_url.text, "html.parser")

pagination = soup.find("table", {"class":"table table-bordered downloads tablesorter"})

pages = pagination.find_all('tr')

for page in pages[1:]:
  tds_name.append(page.find("td").string.capitalize())
  tds_code.append(page.find("td").find_next("td").find_next("td").string)

for i, v in enumerate(tds_code):
  if v == None :
    del tds_code[i]
    del tds_name[i]

index = 0
for index, value in enumerate(tds_name): 
  print('# {} {}'.format(index, value))

while not cont :
  try:
    I_value = int(input('#: '))
    if I_value > index:
      print("Choose a number from the list.")
    else:
      print("You choose {}".format(tds_name[I_value]))
      print("The currency code is {}".format(tds_code[I_value]))
      cont = True
  except:
    print("That wasn't a number.")
