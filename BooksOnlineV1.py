# Import :
import requests
from bs4 import BeautifulSoup
import csv

# Variables :
page = "http://books.toscrape.com/index.html"
pages = [""] * 20
urls = []
MainD = {}

# Liste d'urls
mainurl = requests.get(page)
main = BeautifulSoup(mainurl.text, "html.parser")
links = main.findAll("h3")
for h3 in links:
    a = h3.find("a")
    link = "http://books.toscrape.com/" + a['href']
    urls.append(link)

# Scraping d'informations sur les Books:
for i in range(len(urls)):
    D = {"product_page_url": "", "universal_product_code (upc)": "",
         "title": "", "price_including_tax": "", "price_excluding_tax": "", "number_available": "",
         "product_description": "", "category": "", "review_rating": "", "image_url": ""}
    tds = []
    response = requests.get(urls[i])
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
# URL :
        D["product_page_url"] = urls[i]
# Titre :
        title = soup.find("h1").string
        D["title"] = title
# Catégorie :
        uls = soup.find("ul", {"class": "breadcrumb"})
        for a in uls:
            cats = uls.findAll("a")
        cat = cats[len(cats)-1].string
        D["category"] = cat
# product description :
        art = soup.find("div", {"id": "product_description"})
        des = art.findNext("p").string
        D["product_description"] = des
# Image :
        car = soup.find("div", {"class": "carousel-inner"})
        imgs = car.find("img")
        img = imgs["src"]
        img = img.replace("../../", "http://books.toscrape.com/")
        D["image_url"] = img
# UPC ; Prix sans TVA ; Prix avec TVA ; Quantité ; Nombre de vu :
        ths = ["universal_product_code (upc)", "price_excluding_tax",
               "price_including_tax", "number_available", "review_rating"]
        temoin = ["UPC", "Price (excl. tax)", "Price (incl. tax)", "Availability", "Number of reviews"]
        tab = soup.find("table", {"class": "table table-striped"})
        for b in range(len(temoin)):
            ta = tab.find(string=temoin[b])
            D[ths[b]] = ta.find_next("td").string
    MainD[i] = D

# Ecriture un fichier csv :
with open('BooksOnline.csv', 'w', newline='', encoding="utf-8") as csvfile:
    w = csv.DictWriter(csvfile, fieldnames=D.keys(), quotechar=',', quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for y in range(len(urls)):
        w.writerow(MainD[y])
