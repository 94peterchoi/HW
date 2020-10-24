#씁쓸맛숙제 최상욱 깃헙과 슬랙을 연동해요
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20201024', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div.music-list-wrap > table > tbody > tr')

for tr in trs:
    rank_tag = tr.select_one('td.number').text #순위
    if rank_tag is None:
        continue

    title_tag = tr.select_one('td.info > a.title').text #노래제목
    if title_tag is None:
        continue

    singer_tag = tr.select_one('td.info > a.artist').text #아티스트
    if singer_tag is None:
        continue

    # print(rank_tag[0:2].strip(), title_tag.strip(), singer_tag)
    rank_tag = rank_tag[0:2].strip()
    title_tag = title_tag.strip()

    print(rank_tag, title_tag)
    data = {
        'rank': int(rank_tag),
        'title': title_tag,
        'singer': singer_tag
    }

    db.genie.insert_one(data)