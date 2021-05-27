import requests, json
from flask import render_template, current_app, jsonify
from flask_login import login_required
from bs4 import BeautifulSoup
from flask import Blueprint
from flask_mail import Mail, Message
from .magazine_luiza import MagazineLuizaSpider
from .americanas import AmericanasSpider
from .submarino import SubmarinoSpider
from .shoptime import ShopTimeSpider
from .extra import ExtraSpider

from ..admin.views import send_mail_promo
from . import home
from .. import mail

companies = [
    ('Magazine Luiza', 'https://www.magazineluiza.com.br/busca/iphone+11/'),
    #('Americanas', 'https://www.americanas.com.br/busca/iphone-12'),
    #('ShopTime', 'https://www.shoptime.com.br/busca/iphone-12'),
    #('Casas Bahia', 'https://www.casasbahia.com.br/iphone-12/b'),
]
products = [
    'iphone 11',
    'iphone 12'
]

less_word = [
    'capa',
    'silicone',
    'fonte',
    'carregador',
    'fone',
    'cabo',
    'película'
]

def request_json():

    itens = []
    for product in products:
        # magazine = MagazineLuizaSpider(product).extract_item()

        # for _magazine in magazine:
        #     itens.append(_magazine)

        # americanas = AmericanasSpider(product).extract_item()

        # for _americanas in americanas:
        #     itens.append(_americanas)

        # submarino = SubmarinoSpider(product).extract_item()

        # for _submarino in submarino:
        #     itens.append(_submarino)

        # shoptime = ShopTimeSpider(product).extract_item()

        # for _shoptime in shoptime:
        #     itens.append(_shoptime)

        extra = ExtraSpider(product).extract_item()

        for _extra in extra:
            itens.append(_extra)

    return json.dumps(itens)

def refactory_number(num):
    if ',' in num:
        num = num.split(',')[0]
    if '.' in num:
        num = num.replace('.', '')
    return num.replace('R$','').strip()

def recMin(nestedLis):
    if isinstance(nestedLis, int):
        return nestedLis
    if len(nestedLis) == 1:
        return recMin(nestedLis[0])
    if isinstance(nestedLis[0], list):
        return min(recMin(nestedLis[0]), recMin(nestedLis[1:]))
    if isinstance(nestedLis[0], int):
        return min(nestedLis[0], recMin(nestedLis[1:]))

def buscarMenor(lst, item1, item2):
    i = float("inf")
    for nr in lst:
        num = refactory_number(nr['cash_price'])
        if num < i:
            i = num

    return i

def busca_precos(lst):
    itens = []
    for nr in lst:
        if 'R$' in nr['cash_price']:
            idx = None
            num = float(refactory_number(nr['cash_price']))
            if not itens:
                itens.append(nr)
            else:
                last_item = None
                for key, item in enumerate(itens):
                    if item['company'] == nr['company'] and item['product'] == nr['product']:
                        last_item = item
                        idx = key

                if last_item:
                    if num < float(refactory_number(last_item['cash_price'])):
                        itens.pop(idx)
                        itens.append(nr)
                else:
                    itens.append(nr)
    return itens

def filter_json(list_itens):
    _list_itens = []
    for item in list_itens:
        check = False
        for word in less_word:
            if word.lower() in str(item['title']).lower():
                check = True
                break
        if not check:
            _list_itens.append(item)
    input_dict = busca_precos(_list_itens)
    return input_dict

@home.app_template_filter()
@login_required
def format_label(label):
    return label.capitalize()

@home.route("/spider_json")
@login_required
def spider_json():
    spider = {}
    spider['data'] = json.loads(request_json())
    return jsonify(spider)

@home.route("/")
@login_required
def homepage():
    return render_template('home/home.html')

@home.route("/enviar_produtos")
def enviar_produtos():
    request = request_json()
    itens = filter_json(json.loads(request))
    #return render_template('home/email.html', itens=itens)
    message = send_mail_promo(itens)
    return message