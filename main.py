import json
import sys
import urllib.request
import pymysql
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
load_dotenv()
headers = {"User-Agent": "Mozilla/5.0"}

conn = pymysql.connect(host='127.0.0.1', user='root', password=os.environ.get("DB_PASSWORD"), db='PokedexDB', charset='utf8mb4')
cur = conn.cursor()
cur.execute("CREATE TABLE `pokemon` (`num_nat` INT NOT NULL, `name_kor` CHAR(20) NOT NULL, `name_jap` CHAR(20) NOT NULL, `name_eng` CHAR(30) NOT NULL, `base_stat` JSON NOT NULL, `types` JSON NOT NULL, `classification` CHAR(15) NOT NULL, `color` CHAR(10) NOT NULL, `height` DOUBLE NOT NULL, `weight` DOUBLE NOT NULL, `male_rate` DOUBLE NOT NULL, PRIMARY KEY (`num_nat`));")

pokemon_list = []

res1 = requests.get("https://namu.wiki/w/%ED%8F%AC%EC%BC%93%EB%AA%AC%EC%8A%A4%ED%84%B0/%EB%AA%A9%EB%A1%9D/%EC%A0%84%EA%B5%AD%EB%8F%84%EA%B0%90", headers=headers)
if res1.status_code == 200:
    html = res1.text
    soup = BeautifulSoup(html, 'html.parser')

    table1 = soup.select('#UHvnxwhkp > div:nth-child(12) > div.wiki-table-wrap.table-center > table > tbody > tr')
    for i in range (1, len(table1)):
        tr = table1[i]
        num_nat = tr.select_one("td:nth-child(1) > div").get_text()
        if not num_nat.isdigit():
            continue
        name_kor = tr.select_one("td:nth-child(3) > div").get_text()
        bracket_index = name_kor.find('[')
        if bracket_index >= 0:
            name_kor = name_kor[:bracket_index]
        pokemon_list.append({'name_kor': name_kor})

    table2 = soup.select('#UHvnxwhkp > div:nth-child(14) > div.wiki-table-wrap.table-center > table > tbody > tr')
    for i in range(1, len(table2)):
        tr = table2[i]
        num_nat = tr.select_one("td:nth-child(1) > div").get_text()
        if not num_nat.isdigit():
            continue
        name_kor = tr.select_one("td:nth-child(3) > div").get_text()
        bracket_index = name_kor.find('[')
        if bracket_index >= 0:
            name_kor = name_kor[:bracket_index]
        pokemon_list.append({'name_kor': name_kor})

    table3 = soup.select('#UHvnxwhkp > div:nth-child(16) > div.wiki-table-wrap.table-center > table > tbody > tr')
    for i in range(1, len(table3)):
        tr = table3[i]
        num_nat = tr.select_one("td:nth-child(1) > div").get_text()
        if not num_nat.isdigit():
            continue
        name_kor = tr.select_one("td:nth-child(3) > div").get_text()
        bracket_index = name_kor.find('[')
        if bracket_index >= 0:
            name_kor = name_kor[:bracket_index]
        pokemon_list.append({'name_kor': name_kor})

    table4 = soup.select('#UHvnxwhkp > div:nth-child(18) > div.wiki-table-wrap.table-center > table > tbody > tr')
    for i in range(1, len(table4)):
        tr = table4[i]
        num_nat = tr.select_one("td:nth-child(1) > div").get_text()
        if not num_nat.isdigit():
            continue
        name_kor = tr.select_one("td:nth-child(3) > div").get_text()
        bracket_index = name_kor.find('[')
        if bracket_index >= 0:
            name_kor = name_kor[:bracket_index]
        pokemon_list.append({'name_kor': name_kor})
else:
    print('error', res1.status_code)

res2 = requests.get("https://pokemon.fandom.com/ko/wiki/%EC%A2%85%EC%A1%B1%EA%B0%92_%EB%AA%A9%EB%A1%9D", headers=headers)
if res2.status_code == 200:
    html = res2.text
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.select('#mw-content-text > div > table > tbody > tr')
    num = 1
    for i in range (1, len(table)):
        tr = table[i]
        tr_num = int(tr.select_one("td:nth-child(1) > b").get_text())
        if num == tr_num:
            if num > 493:
                break
            tr_h = int(tr.select_one("td:nth-child(4)").get_text())
            tr_a = int(tr.select_one("td:nth-child(5)").get_text())
            tr_b = int(tr.select_one("td:nth-child(6)").get_text())
            tr_c = int(tr.select_one("td:nth-child(7)").get_text())
            tr_d = int(tr.select_one("td:nth-child(8)").get_text())
            tr_s = int(tr.select_one("td:nth-child(9)").get_text())
            base_stat = {"h": tr_h, "a": tr_a, "b": tr_b, "c": tr_c, "d": tr_d, "s": tr_s, "total": tr_h + tr_a + tr_b + tr_c + tr_d + tr_s}
            pokemon_list[num - 1]["base_stat"] = base_stat

            # image = tr.select_one("td:nth-child(2) > a > img")
            # if num <= 3:
            #     urllib.request.urlretrieve(image['src'], 'images/icons/icon_' + str(num) + '.jpg')
            # else:
            #     urllib.request.urlretrieve(image['data-src'], 'images/icons/icon_' + str(num) + '.jpg')

            num += 1
        else:
            continue
else:
    print('error', res2.status_code)

for i in range(493):
    res = requests.get("https://pokemon.fandom.com/ko/wiki/" + pokemon_list[i]['name_kor'] + "_(포켓몬)", headers=headers)
    if res.status_code == 200:
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.select_one('#mw-content-text > div > div')

        name_kor = div.select_one('div.head > div.name > div:nth-child(1)').get_text().strip()
        name_jap = div.select_one('div.head > div.name > div:nth-child(2) > span').get_text().strip()
        name_eng = div.select_one('div.head > div.name > div:nth-child(3) > span').get_text().strip()

        # image = div.select_one('div:nth-child(2) > a > img')
        # urllib.request.urlretrieve(image['data-src'], 'images/pictures/picture_' + str(i + 1) + '.jpg')

        div_type1 = div.select_one('table > tbody > tr:nth-child(2) > td:nth-child(1) > div > span > a:nth-child(2) > span')
        div_type2 = div.select_one('table > tbody > tr:nth-child(2) > td:nth-child(1) > div > span > a:nth-child(3) > span')
        types = {"type1": div_type1.get_text()}
        if div_type2 is not None:
            types["type2"] = div_type2.get_text()
        classification = div.select_one('table > tbody > tr:nth-child(2) > td:nth-child(2)').get_text().strip()
        color = div.select_one('table > tbody > tr:nth-child(11) > td:nth-child(1) > span')['style'][11:]
        height = float(div.select_one('table > tbody > tr:nth-child(13) > td:nth-child(1)').get_text().strip()[:-1])
        weight = float(div.select_one('table > tbody > tr:nth-child(13) > td:nth-child(2)').get_text().strip()[:-2])
        male_rate = 0.5
        div_rate = div.select_one('table > tbody > tr:nth-child(15) > td:nth-child(2)').get_text().strip()
        if div_rate == '무성':
            male_rate = -1.0
        else:
            div_rate_percent_index = div_rate.find('%')
            male_rate = float(div_rate[3:div_rate_percent_index]) / 100

        pokemon_list[i]["name_jap"] = name_jap
        pokemon_list[i]["name_eng"] = name_eng
        pokemon_list[i]["types"] = types
        pokemon_list[i]["classification"] = classification
        pokemon_list[i]["color"] = color
        pokemon_list[i]["height"] = height
        pokemon_list[i]["weight"] = weight
        pokemon_list[i]["male_rate"] = male_rate
    else:
        print('error', res.status_code)


for i in range(len(pokemon_list)):
    p = pokemon_list[i]
    curStr = "INSERT INTO `pokemon` VALUES (%d, \"%s\", \"%s\", \"%s\", \'%s\', \'%s\', \"%s\", \"%s\", %s, %s, %s)" % ((i + 1), p["name_kor"], p["name_jap"], p["name_eng"], json.dumps(p["base_stat"]), json.dumps(p["types"], ensure_ascii=False), p["classification"], p["color"], p["height"], p["weight"], p["male_rate"])
    cur.execute(curStr)
conn.commit()
conn.close()