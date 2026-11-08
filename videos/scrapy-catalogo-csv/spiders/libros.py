import scrapy


class LibrosSpider(scrapy.Spider):
    name = "libros"
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        for ficha in response.css("article.product_pod"):
            yield {
                "titulo": ficha.css("h3 a::attr(title)").get(),
                "precio": ficha.css("p.price_color::text").get(),
                "stock": ficha.css("p.instock.availability::text").getall()[-1].strip(),
            }

        siguiente = response.css("li.next a::attr(href)").get()
        if siguiente:
            yield response.follow(siguiente, self.parse)
