import requests, json, csv
from urllib.parse import urlsplit, urljoin, urlencode, quote, unquote, quote_plus
from bs4 import BeautifulSoup


class MagazineLuizaSpider(object):
    def __init__(self, product):
        self.company = 'Magazine Luiza'
        self.base_url = 'https://www.magazineluiza.com.br/busca/'
        self.links = set()
        self.items = []
        self.product = str(product)
        self.start_url = self.prepare_url(product)
        #self.set_base_url()

    def crawl(self):
        self.get_links()
        self.get_items()

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self):
        item_url_xpath = "//a[@class='data-product']/@href"
        next_page_xpath = "//div[@class='product-showcase-bottom']/a/@href"
        r = requests.get(self.start_url)
        html = BeautifulSoup(r.text, 'html.parser')

        self.parse_links(html, item_url_xpath)
        next_page = html.xpath(next_page_xpath)[0]
        while next_page:
            r = requests.get(urljoin(self.base_url, next_page))
            html = BeautifulSoup(r.text, 'html.parser')
            self.parse_links(html, item_url_xpath)
            try:
                next_page = html.xpath(next_page_xpath)[1]
            except IndexError as e:
                next_page = None

    def get_items(self):
        for link in self.links:
            r = requests.get(link)
            html = BeautifulSoup(r.text, 'html.parser')
            self.items.append(self.extract_item(html, link))

    def extract_item(self):
        response = requests.get(self.start_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('a', {'class': 'product-li'})
        itens = []

        for item in data:
            _data = json.loads(item['data-product'])
            _item = {
                'company': self.company,
                'product': self.product,
                'title': _data['title'],
                'link': item['href'],
                'installment_price': self.format_currency(_data['price']),
                'cash_price': item.find('span', {'class': 'price-value'}).text.replace('\n', ' ').strip() if item.find('span', {'class': 'price-value'}) else '',
                'original_price': item.find('span', {'class': 'originalPrice'}).text.replace('\n', ' ').strip() if item.find('span', {'class': 'originalPrice'}) else ''
            }
            itens.append(_item)
        return itens

    def parse_links(self, html, item_url_xpath):
        print(item_url_xpath)
        new_links = html.xpath(item_url_xpath)
        print(new_links)
        new_links = [self.prepare_url(l) for l in new_links]
        self.links = self.links.union(set(new_links))

    def set_base_url(self):
        self.base_url = urlsplit(self.start_url)._replace(path="", query="").geturl()

    def prepare_url(self, product):
        search = quote_plus(product)
        url = urljoin(self.base_url, search)
        return urlsplit(url)._replace(query="").geturl()

    def save_items(self, filename):
        keys = self.items[0].keys()
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.items)

    def format_currency(self, value):
        try:
            return "R$ {:7,.2f}".format(float(value))
        except:
            return "R$ 0.00"