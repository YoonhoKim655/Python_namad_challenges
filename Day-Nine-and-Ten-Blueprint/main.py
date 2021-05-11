import requests
from flask import Flask, render_template, request
import os


def make_detail_url(id):
  return f"{base_url}/items/{id}"


def url_hits(url):
  url_json = requests.get(url).json()
  return url_json['hits']


def get_info(url):
  title = []
  url_list = []
  point = []
  by = []
  comment = []
  ID = []
  dict_url = {}

  hits = url_hits(url)

  for hit in hits:
    title.append(hit['title'])
    url_list.append(hit['url'])
    by.append(hit['author'])
    point.append(hit['points'])
    comment.append(hit['num_comments'])
    ID.append(hit["objectID"])

  dict_url['title'] = title
  dict_url['url'] = url_list
  dict_url['by'] = by
  dict_url['comment'] = comment
  dict_url['point'] = point
  dict_url['id'] = ID

  return dict_url


def get_detail_info(id):
  url = make_detail_url(id)
  name = []
  comment = []
  dict_detail = {}

  children = requests.get(url).json()["children"]

  for child in children:
    if child['author'] is None:
      name.append("Del") 
    else:
      name.append(child['author'])
    if child['text'] is None:
      comment.append("Del") 
    else:
      comment.append(child['text'])
  dict_detail['name'] = name
  dict_detail['text'] = comment

  return dict_detail


os.system("clear")
dict_pop = {}
dict_new = {}
dict_detail = {}

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"
#dict_new = get_info(new)

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

dict_pop = get_info(popular)

#print(len(dict_pop.get("title")))
"""
for i in range(len(dict_pop.get("title"))):
  print(dict_pop.get("title")[i])"""


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api

db = {}
app = Flask("DayNine")


@app.route("/")
def home():
  order = request.args.get('order_by', type=str, default='popular')

  """if order == "popular":
    r_pop = requests.get(popular)
  else:
    r_new = requests.get(new)"""
  
  Data = db.get(order)
  
  if Data:
    page_datas = Data
  else:
    db[order] = get_info(order)

  return render_template("index.html", order = order, page_datas = page_datas)

"""@app.route("/＜id＞")
def ID(id):
  if "detail" in db:
    Data = db["detail"].get(id)
    if Data:
      detail_datas = Data
    else:
      return redirect("/")
  else:
    db["detail"] = get_detail_info(id)
    from_detail_DB = db["detail"].get(id)

  return render_template("detail.html", dbdata = from_detail_DB)"""

app.run(host="0.0.0.0")