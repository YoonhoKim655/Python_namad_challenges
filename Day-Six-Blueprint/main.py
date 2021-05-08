import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

url = "https://www.iban.com/currency-codes"
indeed_url = requests.get(url)
tds_name = []
tds_code = []
first_country = -1
second_country = -1
convert_rate = 0
money = 0
cont = False

print("Welcome to CurrencyCovert Pro 2000\n")

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

print("\nWhere are you from? Choose a country by number.\n")

while not cont :
  try:
    first_country = int(input('#: '))
    if first_country > index:
      print("Choose a number from the list.\n")
    else:
      print(tds_name[first_country])
      print()
      cont = True
  except:
    print("That wasn't a number.\n")

print("Now choose another country.")

cont = False
while not cont :
  try:
    second_country = int(input('#: '))
    if second_country > index:
      print("Choose a number from the list.\n")
    else:
      print(tds_name[second_country])
      print()
      cont = True
  except:
    print("That wasn't a number.\n")

print("How many {} do you want to convert to {}?".format(tds_code[first_country], tds_code[second_country]))

cont = False
while not cont :
  try:
    money = int(input(''))
    cont = True
  except:
    print("That wasn't a number.\n")

goal_url = "https://wise.com/gb/currency-converter/{}-to-{}-rate?amount=50".format(tds_code[first_country], tds_code[second_country])
goal_indeed_url = indeed_url = requests.get(goal_url)

convert_soup = BeautifulSoup(goal_indeed_url.text, "html.parser")

goal_rate = float(convert_soup.find("span", {"class":"text-success"}).string)

origin = format_currency(money, tds_code[first_country], locale="ko_KR")
target = format_currency(money * goal_rate, tds_code[second_country], locale="ko_KR")

print("{} is {}".format(origin, target))