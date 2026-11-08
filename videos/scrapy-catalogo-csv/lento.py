import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/catalogue/page-1.html"

respuesta = requests.get(URL, timeout=20)
respuesta.encoding = "utf-8"
sopa = BeautifulSoup(respuesta.text, "html.parser")

for ficha in sopa.select("article.product_pod"):
    titulo = ficha.h3.a["title"][:38]
    precio = ficha.select_one(".price_color").text
    print(f"{titulo:40s} {precio}")

print(f"\nfilas: {len(sopa.select('article.product_pod'))}")
print("paginas del catalogo: 50")
