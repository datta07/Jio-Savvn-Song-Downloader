import requests
from bs4 import BeautifulSoup

def get_lyrics(link="https://www.saavn.com/lyrics/ismart-title-song/EiJSSz9fcHs"):
	try:
		headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
		l1=link.split('/')
		l1[-2]=l1[-2]+'-lyrics'
		link='/'.join(l1)
		print(link)
		source=requests.get(link).text
		source=source.replace("<br/>","\n")
		soup=BeautifulSoup(source,'lxml')
		res=soup.find(class_='u-disable-select')
		res=res.find('p').text
		lyrics=str(res).replace("<span>","")
		lyrics=str(res).replace("</span>","")
		lyrics=lyrics.replace('<p class="lyrics"> ','')
		lyrics=lyrics.replace("</p>",'')
		return lyrics
	except Exception as e:
		print(str(e))
		return 'Sorry lyrics is not present\n'

print(get_lyrics())
