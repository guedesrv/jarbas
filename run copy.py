import requests, json
from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='app/templates')  # still relative to module

companies = [
    ('Magazine Luiza', 'https://www.magazineluiza.com.br/busca/iphone+11/'),
    #('Americanas', 'https://www.americanas.com.br/busca/iphone-12'),
    #('ShopTime', 'https://www.shoptime.com.br/busca/iphone-12'),
    #('Casas Bahia', 'https://www.casasbahia.com.br/iphone-12/b'),
]

@app.template_filter()
def format_currency(value):
    return "R${:7,.2f}".format(float(value))

@app.route("/")
def home():
    for company, url in companies:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('a', {'class': 'product-li'})
        itens = []

        for item in data:
            _data = json.loads(item['data-product'])
            _item = {
                'company': company,
                'title': _data['title'],
                'link': item['href'],
                'installment_price': _data['price'],
                'cash_price': item.find('span', {'class': 'price-value'}).text.replace('\n', ' ').strip() if item.find('span', {'class': 'price-value'}) else '',
                'original_price': item.find('span', {'class': 'originalPrice'}).text.replace('\n', ' ').strip() if item.find('span', {'class': 'originalPrice'}) else ''
            }
            itens.append(_item)

        return render_template('home.html', itens=itens)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)