import requests
import os

Keep = True

while Keep:
  print("Welcome to IsItDown.py!\n",
  "Please write a URL or URLs you want to check. (separated by comma)")

  url = input()
  urls = url.split(',')
  for i in range(len(urls)):
    urls[i] = urls[i].replace(" ", "")
    if urls[i][len(urls[i])-4:] == ".com":
      if len(urls[i]) > 7:
        if urls[i][:7] != "http://" :
          urls[i] = "http://" + urls[i]
      else:
        urls[i] = "http://" + urls[i]
      try:
        requests.get(urls[i])
        print(urls[i], " is up!")
      except:
        print(urls[i], " is down!")
    else:
      print(urls[i], " is not a valid URL.")
  cont_1 = True
  while cont_1:
    print("Do you want to start over? y/n ")
    cont = input()
    if cont == 'y':
      Keep = True
      os.system('clear')
      cont_1 = False
    elif cont == 'n':
      print("Ok, bye")
      Keep = False
      cont_1 = False
    else:
      print("That's not a valid answer.")

