#####################################
#             Garuda.inc            #
#####################################
#Author: Akula Guru Datta
#Date    : 01-10-2019
#pip install pyDes,requests,websocket

import requests
from pyDes import *
import base64
import websocket
import json
import os

if ('garuda_songs' in os.listdir('.')):
	pass
else:
	os.mkdir('garuda_songs')

def url_album_design(id):	
	k=requests.get('https://www.saavn.com/api.php?cc=in&_marker=0&albumid='+str(id)+'&_format=json&__call=content.getAlbumDetails')
	k=k.json()
	print(k['title'],k['release_date'])
	l={}
	name=des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
	for i in k['songs']:
		j=i['encrypted_media_url']
		j=base64.b64decode(j.strip())
		name1=name.decrypt(j, padmode=PAD_PKCS5).decode('utf-8')
		l[i['song']]=name1
	print('select an song to download')
	return l


def url_song_design(id):	
	k=requests.post('https://www.saavn.com/api.php?cc=in&_marker=0?_marker=0&_format=json&model=Redmi_5A&__call=song.getDetails&pids='+id)
	k=k.json()
	k=k[id]
	try:
		print(k['song'],k['album'],k['release_date'],k['language'],k['starring'])
	except Exception:
		pass
	l={}
	name=des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
	j=k['encrypted_media_url']
	j=base64.b64decode(j.strip())
	name1=name.decrypt(j, padmode=PAD_PKCS5).decode('utf-8')
	l[k['song']]=name1
	print('downloading song')
	downloader(name1,k['song'],k['album'])
	return l

def searcher(query):
	url='wss://ws.saavn.com/'
	ws = websocket.create_connection(url)
	msg='{"url":"\\\/api.php?__call=autocomplete.get&_marker=0&query='+query+'&ctx=android&_format=json&_marker=0"}'
	ws.send(msg)
	result = ws.recv()
	result=json.loads(result)
	result=result['resp']
	result=json.loads(result)
	top_query=[]
	song=[]
	album=[]
	for j in list(result.keys()):
		try:
			if (j=='topquery'):
				i=result[j]
				i=i['data'][0]
				if (i['type']=='album'):
					top_query.append({'id':i['id'],'title':i['title'],'music':i['music'],'year':i['more_info']['year'],'language':i['more_info']['language'],'movie':i['more_info']['is_movie'],'state':1})
				else:
					top_query.append({'id':i['id'],'title':i['title'],'album':i['album'],'primary_artists':i['more_info']['primary_artists'],'state':0})
		except Exception:
			pass
			
		if (j=='albums'):
			k=result[j]
			k=k['data']
			for i in k:
				album.append({'id':i['id'],'title':i['title'],'music':i['music'],'year':i['more_info']['year'],'language':i['more_info']['language'],'movie':i['more_info']['is_movie']})
		if (j=='songs'):
			k=result[j]
			k=k['data']
			for i in k:
				song.append({'id':i['id'],'title':i['title'],'album':i['album'],'primary_artists':i['more_info']['primary_artists']})
	ws.close()
	return (top_query,album,song)

def downloader(url,name,folder,no=0):
	no=int(input("enter the quality :\n 1) normal\n 2) HD \n:"))
	if (no==2):
		url=url.replace('_96','_320')
		name=name+'_HD'
	try:
		os.mkdir('garuda_songs/'+folder)
	except Exception:
		pass
	with open('garuda_songs/'+folder+'/'+name+'.mp3', "wb") as f:
		print("Downloading "+name)
		response = requests.get(url, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None: # no content length header
		    f.write(response.content)
		else:
		    dl = 0
		    total_length = int(total_length)
		    for data in response.iter_content(chunk_size=4096):
		        dl += len(data)
		        f.write(data)
		        done = int(50 * dl / total_length)
		        print('    ','■'*done,'  ',str(done*2)+'%',end='\r')
	print('    ','■'*done,'  ',str(done*2)+'%')
	print('••'*35)
	print(' downloaded in garuda_songs>>',folder,'>>',name+'.mp3')
	print('••'*35)
	
	
query=input('enter the song or movie you want:\t')
top_query,album,song=searcher(query)
l=[]
ab=[]
no=0
print('--'*35)
print('\ttopquery:-')
qr=1

for i in top_query:
	no+=1
	if (i['state']==1):
		l.append(i['id'])
		ab.append(i['title'])
		print('--'*35)
		print(no,') ',end='')
		print(i['title'],i['year'])
		print('   lan:',i['language'],'  music:',i['music'])
		if (i['movie']=='1'):
			print('   album of a movie')
		else:
			print('   album of some_playlist')
	else:
		qr=0
		l.append(i['id'])
		print('--'*35)
		print(no,') ',end='')
		print(i['title'],'  music:',i['primary_artists'])
		print('a song from',i['album'])


print('--'*35)
print('\talbums:-')

for i in album:
	no+=1
	l.append(i['id'])
	ab.append(i['title'])
	print('--'*35)
	print(no,') ',end='')
	print(i['title'],i['year'])
	print('   lan:',i['language'],'  music:',i['music'])
	if (i['movie']=='1'):
		print('   album of a movie')
	else:
		print('   album of some_playlist')
t=no

print('--'*35)
print('\tsongs:-')
for i in song:
	no+=1
	l.append(i['id'])
	print('--'*35)
	print(no,') ',end='')
	print(i['title'],'  music:',i['primary_artists'])
	print('a song from',i['album'])
print('--'*35)

no=int(input('choice a song or album:\t'))-1
if (no==0):
	if (qr==0):
		url_song_design(l[no])
	else:
		k=url_album_design(l[no])
		folder=ab[no]
		no=0
		l=[]
		for i in k.keys():
			no+=1
			print(no,')',i)
			l.append(k[i])
		no=int(input('choice a song:\t'))-1
		p=list(k.keys())
		downloader(l[no],p[no],folder,1)
elif (t<=no):
	url_song_design(l[no])
else:
	k=url_album_design(l[no])
	folder=ab[no]
	no=0
	l=[]
	for i in k.keys():
		no+=1
		print(no,')',i)
		l.append(k[i])
	no=int(input('choice a song:\t'))-1
	p=list(k.keys())
	downloader(l[no],p[no],folder,1)