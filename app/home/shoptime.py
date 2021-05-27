import requests, json, csv
from urllib.parse import urlsplit, urljoin, urlencode, quote, unquote, quote_plus
from bs4 import BeautifulSoup


class ShopTimeSpider(object):
    def __init__(self, product):
        self.company = 'Shoptime'
        self.base_url = 'https://www.shoptime.com.br/busca/'
        self.links = set()
        self.items = []
        self.product = str(product)
        self.start_url = self.prepare_url(product)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }

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
        response = requests.get(self.start_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('div', {'class': 'epVkvq'})
        itens = []

        for item in data:
            company = self.company
            product = self.product
            title = item.select('span[class*="src__Name"]')[0].text
            link = self.refactory_url(item.find('a')['href'])
            installment_price = ''
            cash_price = item.find('a').select('span[class*="src__PromotionalPrice"]')
            original_price = item.find('a').select('span[class*="src__Price"]')
            if cash_price:
                cash_price = cash_price[0].text.replace('Prime', '')
            else:
                cash_price = ''

            if original_price:
                original_price = original_price[0].text.replace('Prime', '')
            else:
                original_price = ''
            
            if not original_price:
                installment_price = cash_price
            
            _item = {
                'company': company,
                'product': product,
                'title': title,
                'link': link,
                'installment_price': installment_price,
                'cash_price': cash_price,
                'original_price': original_price
            }
            itens.append(_item)
        return itens

    def parse_links(self, html, item_url_xpath):
        links = html.xpath(item_url_xpath)
        new_links = [self.prepare_url(l) for l in links]
        self.links = self.links.union(set(new_links))

    def set_base_url(self):
        self.base_url = urlsplit(self.start_url)._replace(path="", query="").geturl()

    def prepare_url(self, product):
        search = quote(product).replace('%20', '-')
        url = urljoin(self.base_url, search)
        return urlsplit(url)._replace(query="").geturl()

    def save_items(self, filename):
        keys = self.items[0].keys()
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.items)
    
    def refactory_url(self, url):
        product = url.split('?')[0]
        return 'http://www.shoptime.com.br{}'.format(product)