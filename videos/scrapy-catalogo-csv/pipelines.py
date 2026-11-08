from scrapy.exceptions import DropItem


class LimpiaPrecio:
    def process_item(self, item, spider):
        item["precio"] = float(item["precio"].replace("£", ""))
        return item


class SinDuplicados:
    vistos = set()

    def process_item(self, item, spider):
        if item["titulo"] in self.vistos:
            raise DropItem(f"repetido: {item['titulo']}")
        self.vistos.add(item["titulo"])
        return item
