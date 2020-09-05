import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
from datetime import datetime
import re
import json
from jmespath import search
import os


def convert_type(price):
    number = price.split('R$')[-1]
    return float(number.replace('.', '').replace(',', '.').strip())


def gen_dataframe(headers, store):
    if store == 'cissa':
        cissa_process = get_cissa_product(headers, 'Processador')
        cissa_placa = get_cissa_product(headers, 'Mãe')
        cissa_video = get_cissa_video(headers, 'Vídeo')
        cissa_process_df = pd.DataFrame(cissa_process)
        cissa_placa_df = pd.DataFrame(cissa_placa)
        cissa_video_df = pd.DataFrame(cissa_video)
        return pd.concat([cissa_process_df, cissa_placa_df, cissa_video_df])
    elif store == 'combat':
        combat_process = get_combat_product(headers, 'ryzen')
        combat_placa = get_combat_product(headers, 'mãe')
        combat_video = get_combat_product(headers, 'geforce')
        combat_process_df = pd.DataFrame(combat_process)
        combat_placa_df = pd.DataFrame(combat_placa)
        combat_video_df = pd.DataFrame(combat_video)
        return pd.concat([combat_process_df, combat_placa_df, combat_video_df])
    elif store == 'gkinfo':
        gkinfo_process = get_gkinfostore_product(headers, 'Processador')
        gkinfo_placa = get_gkinfostore_product(headers, 'Mãe')
        gkinfo_video = get_gkinfostore_product(headers, 'Vídeo')
        gkinfo_process_df = pd.DataFrame(gkinfo_process)
        gkinfo_placa_df = pd.DataFrame(gkinfo_placa)
        gkinfo_video_df = pd.DataFrame(gkinfo_video)
        return pd.concat([gkinfo_process_df, gkinfo_placa_df, gkinfo_video_df])
    elif store == 'guerra':
        guerra_process = get_guerra_product(headers, 'AMD RYZEN')
        guerra_placa = get_guerra_product(headers, 'ASUS')
        guerra_video = get_guerra_product(headers, 'GEFORCE')
        guerra_process_df = pd.DataFrame(guerra_process)
        guerra_placa_df = pd.DataFrame(guerra_placa)
        guerra_video_df = pd.DataFrame(guerra_video)
        return pd.concat([guerra_process_df, guerra_placa_df, guerra_video_df])
    elif store == 'kabum':
        kabum_process = get_kabum_product(headers, 'Ryzen')
        kabum_placa = get_kabum_product(headers, 'Mãe')
        kabum_video = get_kabum_product(headers, 'NVIDIA')
        kabum_rtx = get_kabum_product(headers, 'RTX')
        kabum_process_df = pd.DataFrame(kabum_process)
        kabum_placa_df = pd.DataFrame(kabum_placa)
        kabum_video_df = pd.DataFrame(kabum_video)
        kabum_rtx_df = pd.DataFrame(kabum_rtx)
        return pd.concat([kabum_process_df, kabum_placa_df, kabum_video_df,
                         kabum_rtx_df])
    elif store == 'pichau':
        pichau_process = get_pichau_product(headers, 'Processador')
        pichau_placa = get_pichau_product(headers, 'Mae')
        pichau_video = get_pichau_product(headers, 'Video')
        pichau_process_df = pd.DataFrame(pichau_process)
        pichau_placa_df = pd.DataFrame(pichau_placa)
        pichau_video_df = pd.DataFrame(pichau_video)
        return pd.concat([pichau_process_df, pichau_placa_df, pichau_video_df])
    elif store == 'tera':
        tera_process = get_tera_product(headers, 'Processador')
        tera_placa = get_tera_product(headers, 'Mãe')
        tera_video = get_tera_product(headers, 'Vídeo')
        tera_process_df = pd.DataFrame(tera_process)
        tera_placa_df = pd.DataFrame(tera_placa)
        tera_video_df = pd.DataFrame(tera_video)
        return pd.concat([tera_process_df, tera_placa_df, tera_video_df])


def save_file(df, store, date):
    path = os.path.abspath('data')
    file_name = path + '/' + store + '.xlsx'
    try:
        with pd.ExcelWriter(file_name, mode='a') as writer:
            df.to_excel(writer, sheet_name=date, header=True, index=False)
    except FileNotFoundError:
        df.to_excel(file_name, sheet_name=date, header=True, index=False)
    print(f'Saved {store}.xlsx file for date {date} into hard drive.')


""" Terabyte"""


def get_tera_product(headers, flag):
    if flag == 'Mãe':
        url = "https://www.terabyteshop.com.br/busca?str=placa+m%C3%A3e+" \
              "asus+tuf"
        index = 1
    elif flag == 'Processador':
        url = "https://www.terabyteshop.com.br/busca?str=processador+ryzen"
        index = 0
    elif flag == 'Vídeo':
        url = "https://www.terabyteshop.com.br/busca?str=geforce"
        index = 2
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    prod_list = soup.findAll('div', class_="commerce_columns_item_inner")

    tera_list = []
    for prod in prod_list:
        name_class = prod.find("a", class_="prod-name")
        price_class = prod.find("div", class_="prod-new-price")
        if price_class is not None:
            price = convert_type(price_class.span.text)
            if name_class.text.split(' ')[index] == flag:
                tera = "https://www.terabyteshop.com.br/"
                relative = prod_list[0].find("a",
                                             class_="prod-name").attrs['href']
                prod_url = urllib.parse.urljoin(tera, relative)
                prod_dict = {'nome': name_class.text.strip(), 'url': prod_url,
                             'preco': price}
                tera_list.append(prod_dict)
    return tera_list


""" Pichau"""


def get_pichau_product(headers, flag):
    if flag == 'Mae':
        url = "https://www.pichau.com.br/catalogsearch/result/?q=placa+mae+" \
              "asus+tuf&product_list_limit=48"
        index = 1
    elif flag == 'Processador':
        url = "https://www.pichau.com.br/catalogsearch/result/index/?q=" \
              "processador+amd+ryzen&product_list_limit=48"
        index = 0
    elif flag == 'Video':
        url = "https://www.pichau.com.br/catalogsearch/result/index/?cat=4&" \
              "product_list_limit=48&q=geforce"
        index = 2
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    prod_list = soup.findAll('div', class_="product details "
                             "product-item-details")

    pichau_list = []
    for prod in prod_list:
        name = prod.a.text.replace('\n', '').split(',')[0]
        price_class = prod.find('span', class_='price-boleto')
        if price_class is not None:
            price = convert_type(price_class.span.text.split(' ')[-1])
            if name.split(' ')[index] == flag:
                prod_url = prod.a.attrs['href']
                prod_dict = {'nome': name, 'url': prod_url, 'preco': price}
                pichau_list.append(prod_dict)
    return pichau_list


""" Guerra Digital"""


def get_guerra_product(headers, flag):
    if flag == 'AMD RYZEN':
        url = "https://www.guerradigital.com.br/buscar?q=processador+ryzen"
    elif flag == 'ASUS':
        url = "https://www.guerradigital.com.br/buscar?q=Placa+m%C3%A3e+asus"
    elif flag == 'GEFORCE':
        url = "https://www.guerradigital.com.br/buscar?q=geforce"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    listagem = "listagem borda-alpha"
    info = 'info-produto'
    prod_list = soup.find('div', class_=listagem).find_all(class_=info)

    guerra_list = []
    for prod in prod_list:
        name = prod.a.text
        price_class = prod.find(class_="desconto-a-vista")
        if price_class is not None:
            price = convert_type(price_class.strong.text)
            if flag in name.upper():
                prod_url = prod.a.attrs['href']
                prod_dict = {'nome': name, 'url': prod_url, 'preco': price}
                guerra_list.append(prod_dict)
    return guerra_list


""" GK Infostore"""


def get_gkinfostore_product(headers, flag):
    if flag == 'Mãe':
        url = "https://www.gkinfostore.com.br/produtos?q=placa+m%C3%A3e+asus" \
              "+tuf&limit=48"
        index = 1
    elif flag == 'Processador':
        url = "https://www.gkinfostore.com.br/produtos?q=processador+ryzen&" \
              "limit=48"
        index = 0
    elif flag == 'Vídeo':
        url = "https://www.gkinfostore.com.br/produtos?q=geforce&limit=48"
        index = 2
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    prod_list = soup.find_all(class_='d-flex flex-column justify-content-'
                              'between w-100 h-100 product-link '
                              'position-relative')
    gkinfo_list = []
    for prod in prod_list:
        name = prod.attrs['aria-label']
        price_class = prod.find(class_='product-price-final')
        if price_class is not None:
            price = convert_type(price_class.span.text)
            if name.split(' ')[index] == flag:
                prod_url = prod.attrs['href']
                prod_dict = {'nome': name, 'url': prod_url, 'preco': price}
                gkinfo_list.append(prod_dict)
    return gkinfo_list


""" Cissa Magazine"""


def get_cissa_product(headers, flag):
    if flag == 'Mãe':
        url = "https://www.cissamagazine.com.br/busca?q=placa+m%C3%A3e+" \
              "asus+tuf"
    elif flag == 'Processador':
        url = "https://www.cissamagazine.com.br/busca?q=processador+ryzen"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    prod_list = prod_list = soup.find_all(class_='in_stock')

    cissa_list = []
    for prod in prod_list:
        name = prod.find(class_="product-name").text.replace('\n', '').strip()
        price = prod.find(class_="price-big").text.replace('\n', '').strip()
        price = convert_type(price)
        if flag in name:
            prod_url = 'https:' + prod.attrs['href']
            prod_dict = {'nome': name, 'url': prod_url, 'preco': price}
            cissa_list.append(prod_dict)
    return cissa_list


def get_cissa_video(headers, flag):
    urls = ["https://www.cissamagazine.com.br/busca?q=geforce+1660+super",
            "https://www.cissamagazine.com.br/busca?q=geforce+rtx"]
    cissa_list = []
    for url in urls:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        prod_list = soup.find_all(class_='in_stock')
        for prod in prod_list:
            name = prod.find(class_="product-name").text.replace('\n',
                                                                 '').strip()
            price = prod.find(class_="price-big").text.replace('\n',
                                                               '').strip()
            price = convert_type(price)
            if flag in name:
                prod_url = 'https:' + prod.attrs['href']
                prod_dict = {'nome': name, 'url': prod_url, 'preco': price}
                cissa_list.append(prod_dict)
    return cissa_list


""" Kabum"""


def get_kabum_product(headers, flag):
    if flag == 'Mãe':
        url = 'https://www.kabum.com.br/cgi-local/site/listagem/listagem.' \
              'cgi?string=placa+m%E3e+asus+tuf&btnG='
        index = 9
    elif flag == 'NVIDIA':
        url = 'https://www.kabum.com.br/hardware/placa-de-video-vga/nvidia/' \
              'geforce-gtx-serie-16?pagina=1&ordem=5&limite=100'
        index = 8
    elif flag == 'RTX':
        url = 'https://www.kabum.com.br/hardware/placa-de-video-vga/nvidia/' \
              'geforce-rtx?pagina=1&ordem=5&limite=100'
        index = 8
    elif flag == 'Ryzen':
        url = 'https://www.kabum.com.br/cgi-local/site/listagem/listagem.' \
              'cgi?string=processador+ryzen&btnG='
        index = 9
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    script = soup.find_all('script', type='text/javascript')[index].string
    prods = re.search('listagemDados = (.*)', script, re.IGNORECASE).group(1)
    prods_json = json.loads(prods)
    src = "[?disponibilidade == `true`].{nome: nome, url: link_descricao, " \
          "preco: preco_desconto}"
    product_list = search(src, prods_json)
    kabum_url = 'https://www.kabum.com.br'
    for prod in product_list:
        if flag not in prod['nome']:
            product_list.remove(prod)
        prod['url'] = urllib.parse.urljoin(kabum_url, prod['url'])

    return product_list


""" Combat"""


def get_combat_product(headers, flag):
    if flag == 'geforce':
        url = 'https://www.combatinfo.com.br/procurar?page=1&q=geforce'
    elif flag == 'mãe':
        url = 'https://www.combatinfo.com.br/procurar?q=placa+m%C3%A3e+' \
              'asus+tuf'
    elif flag == 'ryzen':
        url = 'https://www.combatinfo.com.br/procurar?q=processador+ryzen'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    grid = 'products products-grid products-stylized'
    product_tags = soup.find('div',
                             class_=grid).find_all('div',
                                                   class_='product-info')
    combat_list = []
    for prod in product_tags:
        price = prod.div.strong.text
        if price != 'Indisponível':
            name = prod.a.text.replace('\r\n', '').strip()
            url = prod.a.attrs['href']
            price = convert_type(price)
            prod_dict = {'nome': name, 'url': url, 'preco': price}
            combat_list.append(prod_dict)
    return combat_list


if __name__ == "__main__":
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 '
               'Safari/537.36'}
    date = datetime.today().strftime('%Y-%m-%d')

    guerra_df = gen_dataframe(headers, 'guerra')
    save_file(guerra_df, 'guerra_digital', date)
    pichau_df = gen_dataframe(headers, 'pichau')
    save_file(pichau_df, 'pichau', date)
    tera_df = gen_dataframe(headers, 'tera')
    save_file(tera_df, 'terabyte', date)
    gkinfo_df = gen_dataframe(headers, 'gkinfo')
    save_file(gkinfo_df, 'gkinfo', date)
    cissa_df = gen_dataframe(headers, 'cissa')
    save_file(cissa_df, 'cissa', date)
    kabum_df = gen_dataframe(headers, 'kabum')
    save_file(kabum_df, 'kabum', date)
    combat_df = gen_dataframe(headers, 'combat')
    save_file(combat_df, 'combat', date)
