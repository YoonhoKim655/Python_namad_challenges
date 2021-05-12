import requests
from flask import Flask, render_template, request
import os


def make_detail_url(id):
  return f"{base_url}/items/{id}"


def url_hits(url):
  url_json = requests.get(url).json()
  return url_json['hits']


def get_info(url):
  info = {}
  list_url = []

  hits = url_hits(url)

  for hit in hits:
    info = {
      'title' : hit['title'],
      'url' : hit['url'],
      'by' : hit['author'],
      'comment' : hit['num_comments'],
      'point' : hit['points'],
      'id' : hit["objectID"]
    }
    list_url.append(info)

  return list_url


def get_detail_info(id):
  url = make_detail_url(id)
  list_detail = []
  detail = {}
  name = ""
  child = ""
  info = requests.get(url).json()
  children = info["children"]
  
  detail ={
    'title' : info['title'],
    'by' : info['author'],
    'point' : info['points'],
    'url' : info['url']
  }
  list_detail.append(detail)
  for child in children:
    if child['author'] is None:
      name = "Del" 
    else:
      name = child['author']
    if child['text'] is None:
      comment = "Del" 
    else:
      comment = child['text']
    
    detail_1 ={
      'name' : name,
      'comment' : comment
    }
    list_detail.append(detail_1)

  return list_detail


os.system("clear")
dict_pop = []
dict_new = {}
dict_detail = []

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"
#dict_new = get_info(new)

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api

db = {}
app = Flask("DayNine")


@app.route("/")
def home():
  order = request.args.get('order_by', type=str, default='popular')
  
  if order == "popular":
    url = popular
  else:
    order = "new"
    url = new
  
  Data = db.get(order)

  if Data is not None:
    page_datas = Data
  else:
    page_datas = get_info(url)
    db[url] = page_datas
  
  return render_template("index.html", order = order, datas = page_datas)

@app.route("/＜id＞")
def ID(id):
  print(request.args.get())
  Data = db["detail"].get(id)
  if Data is not None:
    detail_datas = Data
  else:
    detail_datas = get_detail_info(id)
    db[id] = detail_datas

  return render_template("detail.html", datas = detail_datas)

app.run(host="0.0.0.0")