# -*- coding: utf-8 -*-

import xbmcplugin, xbmc, xbmcaddon, urllib, xbmcgui, traceback, requests, re, os
from lib import process
import os, shutil, xbmcgui
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.mst3k')
ICON = ADDON_PATH + '/icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
USERDATA_PATH = xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = USERDATA_PATH + '/plugin.video.mst3k/'
favourites = ADDON_DATA + 'favourites'
if os.path.exists(favourites) == True:
	FAV = open(favourites).read()
else:
	FAV = []

start_url ='http://www.club-mst3k.com'
genre_url = start_url+'/episodes?sort=genre'

def Main_Menu():
	Menu('Seasons',start_url+'/episodes?sort=episodes',100,ICON,FANART,'','')
	Menu('Genre',start_url+'/episodes?sort=genre',105,ICON,FANART,'','')
	Menu('Luaghs',start_url+'/episodes?sort=laughs',104,ICON,FANART,'','')
	# Menu('Search','',2,ICON,FANART,'','')


#100
def mst3k_season(url):
	html = requests.get(url).content
	block = re.compile('colspan="4" class="season(.+?)</body>',re.DOTALL).findall(html)
	grab_S = re.compile('_title">.+?(\d+).+?</th>',re.DOTALL).findall(str(block))
	for season in grab_S:
		season ='Season '+season
		process.Menu(season,'',101,ICON,FANART,'','')
  

#101
def episodes(name):
	season_name = name.replace('Season ','')
	html = requests.get(start_url).content
	regex_end = re.findall('<tr id="sort-control">(.+?)~#',html+'~#',re.DOTALL)
	for block in regex_end:
	    tr_ = re.findall('<tr(.+?)</tr>',str(block),re.DOTALL)
	    for tr in tr_:
	        get_info = re.findall('<a href="(.+?)">(.+?)</a>.+?<td class="viewers">(.+?)<.+?<div class="laughs mini">(.+?)<',str(tr),re.DOTALL)
	        for url, name, viewers, laughs in get_info:
	            ep_number = re.findall('(.+?) -',str(name))[0]
	            url = start_url + url
	            if 'k' in ep_number.lower():
	                season_no = '0'
	            elif 'pilot' in ep_number.lower():
	                season_no = '0'
	            elif len(ep_number) == 3:
	                season_no = ep_number[0]
	            elif len(ep_number) == 4:
	                season_no = ep_number[0:2]
	            if season_name == season_no:

	            	process.Menu(name,url,103,ICON,FANART,'','')
#103
def play_link(url):
	html = requests.get(url).content
	block = re.compile('class="full"><b>Full Episode: </b></td>(.+?)class="best"><b>Best of: </b></td>',re.DOTALL).findall(html)
	id_match = re.compile('class="link_button".+?id="(.+?)".+?</a>',re.DOTALL).findall(str(block))
	playlink= re.compile('class="link" id="link_(.+?)".+?src=\'(.+?)\'.+?</p>',re.DOTALL).findall(html)
	for it in id_match:
		for matched_id,link in playlink:
			if it == matched_id:
				if 'youtube'in link:
					embed = link.split('embed/')[1]
					host= link.split('//')[1].replace('www','')
					host = host.split('.')[1]
					process.PLAY(host,embed,102,ICON,FANART,'','')
	try:
		playlink= re.compile('class="link" id="link_(.+?)".+?href="(.+?)".+?</p>',re.DOTALL).findall(html)
		for matched_id,linkz in playlink:
			if 'club' not in linkz:
				if 'tube' not in linkz:
					if 'archive' in linkz:
						arch_html= requests.get(linkz).content
						arch_reg = re.compile('property="og:video" content="(.+?)"',re.DOTALL).findall(arch_html)
						linkzz = arch_reg[0].replace(' ','%20')
						host= linkz.split('//')[1].replace('www','')
						hostz= host.split('/')[0]
						process.PLAY(hostz,linkzz,20,ICON,FANART,'','')
	except:
		pass

#102
def play_fucker(url,name):
	url = 'plugin://plugin.video.youtube/play/?video_id='+ url
	resolve(name,url)

#104
def laughs_(url):
	html = requests.get(url).content
	block = re.compile('class="sort">(.+?)</html>',re.DOTALL).findall(html)
	grab_S = re.compile('<tr >.+?href="(.+?)">(.+?)</a>.+?class="laughs mini">(.+?)<div.+?</tr>',re.DOTALL).findall(str(block))
	for link,name,laughs in grab_S:
		link = start_url+link
		name = name.replace('&#39;','\'')
		name = '%s [COLOR dodgerblue][I]Laughs %s[/I][/COLOR]'%(name,laughs)
		process.Menu(name,link,103,ICON,FANART,'','')


#105
def genre(url):
	html = requests.get(genre_url).content
	block = re.compile('<tr>.+?class="season_title">(.+?)</th>.+?</tr>',re.DOTALL).findall(html)
	for genre in block:
		genre= genre.replace('      ','')
		genrez= genre.replace('\n','')
		genrez= genre.replace('    ','')
		genrez= genre.replace('\n','')
		process.Menu(genrez,genre_url,106,ICON,FANART,'','')

#106
def genre_shows(name,url):
	xbmc.log('************ LOG THIS '+repr(name.strip()),xbmc.LOGNOTICE)
	html = requests.get(url).content
	block = re.findall('class="season_title">(.+?)colspan="4"',html.replace('</table>','colspan="4"'),re.DOTALL)
	name = name.strip()
	for BS in block:
		if name in BS:
			shows =re.compile('<td>.+?href="(.+?)">(.+?)</a>.+?class="viewers".+?</td>',re.DOTALL).findall(str(BS))
			for link,titles in shows:
				link = start_url+link
				process.Menu(titles,link,103,ICON,FANART,'','')




def Search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://ydmoviez.com/?s='+Search_name.replace(' ','+')
	yd_in_search(url)
	
def setView(content, viewType):
	# set content type so library shows more views and info
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if ADDON.getSetting('auto-view')=='true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
		
		
def Menu(name,url,mode,iconimage,fanart,description,extra,showcontext=True,allinfo={}):
		fav_mode = mode
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&extra="+urllib.quote_plus(extra)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
		liz.setProperty( "Fanart_Image", fanart )
		if showcontext:
			contextMenu = []
			if showcontext == 'fav':
				contextMenu.append(('Remove from test Favorites','XBMC.RunPlugin(%s?mode=12&name=%s)'
									%(sys.argv[0], urllib.quote_plus(name))))
			if not name in FAV:
				contextMenu.append(('Add to test Favourites','XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fav_mode=%s&fanart=%s&description=%s)'
						 %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), fav_mode, urllib.quote_plus(fanart), urllib.quote_plus(description))))
			liz.addContextMenuItems(contextMenu)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
		

		
def Play(name,url,mode,iconimage,fanart,description,extra,showcontext=True,allinfo={}):
		fav_mode = mode
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&extra="+urllib.quote_plus(extra)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
		liz.setProperty( "Fanart_Image", fanart )
		if showcontext:
			contextMenu = []
			if showcontext == 'fav':
				contextMenu.append(('Remove from test Favorites','XBMC.RunPlugin(%s?mode=12&name=%s)'
									%(sys.argv[0], urllib.quote_plus(name))))
			if not name in FAV:
				contextMenu.append(('Add to test Favourites','XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fav_mode=%s&fanart=%s&description=%s)'
						 %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), fav_mode, urllib.quote_plus(fanart), urllib.quote_plus(description))))
			liz.addContextMenuItems(contextMenu)
			contextMenu.append(('Queue Item', 'RunPlugin(%s?mode=14)' % sys.argv[0]))
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Big_Resolve(name,url):
	import resolveurl
	try:
		resolved_url = resolveurl.resolve(url)
		xbmc.Player().play(resolved_url, xbmcgui.ListItem(name))
	except:
		xbmc.Player().play(url, xbmcgui.ListItem(name))
	xbmcplugin.endOfDirectory(int(sys.argv[1]))		
		
# ===============================Favourites-----------Not sure whos code this is but credit due to them-------------------------------

def addFavorite(name, url, mode, iconimage, fanart, description, extra):
	favList = []
	xbmc.log(extra)
	try:
		name = name.encode('utf-8', 'ignore')
	except:
		pass
	if os.path.exists(favourites) == False:
		favList.append((name, url, mode, iconimage, fanart, description, extra))
		a = open(favourites, "w")
		a.write(json.dumps(favList))
		a.close()
	else:
		a = open(favourites).read()
		data = json.loads(a)
		data.append((name, url, mode, iconimage, fanart, description, extra))
		b = open(favourites, "w")
		b.write(json.dumps(data))
		b.close()


def getFavourites():
	if not os.path.exists(favourites):
		favList = []
		favList.append(('test Favourites Section', '', '', '', '', '', ''))
		a = open(favourites, "w")
		a.write(json.dumps(favList))
		a.close()
	else:
		items = json.loads(open(favourites).read())
		for i in items:
			name = i[0]
			url = i[1]
			try:
				iconimage = i[3]
			except:
				iconimage = ''
			try:
				fanart = i[4]
			except:
				fanart = ''
			try:
				description = i[5]
			except:
				description = ''
			try:
				extra = i[6]
			except:
				extra = ''

			if i[2] == 20:
				Play(name, url, i[2], iconimage, fanart, description, extra, 'fav')
			else:
				Menu(name, url, i[2], iconimage, fanart, description, extra, 'fav')


def rmFavorite(name):
	data = json.loads(open(favourites).read())
	for index in range(len(data)):
		if data[index][0] == name:
			del data[index]
			b = open(favourites, "w")
			b.write(json.dumps(data))
			b.close()
			break
	xbmc.executebuiltin("XBMC.Container.Refresh")		

def resolve(name,url): 
	xbmc.Player().play(url, xbmcgui.ListItem(name))
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2: 
				params=sys.argv[2] 
				cleanedparams=params.replace('?','')
				if (params[len(params)-1]=='/'):
						params=params[0:len(params)-2]
				pairsofparams=cleanedparams.split('&')
				param={}    
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]
								
		return param
		
params=get_params()
url=None
name=None
iconimage=None
mode=None
fanart=None
description=None
trailer=None
fav_mode=None
extra=None

try:
	extra=urllib.unquote_plus(params["extra"])
except:
	pass

try:
	fav_mode=int(params["fav_mode"])
except:
	pass

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		iconimage=urllib.unquote_plus(params["iconimage"])
except:
		pass
try:        
		mode=int(params["mode"])
except:
		pass
try:        
		fanart=urllib.unquote_plus(params["fanart"])
except:
		pass
try:        
		description=urllib.unquote_plus(params["description"])
except:
		pass

#####################################################END PROCESSES##############################################################		
		
if mode == None: Main_Menu()
elif mode == 2 : Search()

elif mode == 10: getFavourites()
elif mode==11:
	try:
		name = name.split('\\ ')[1]
	except:
		pass
	try:
		name = name.split('  - ')[0]
	except:
		pass
	addFavorite(name, url, fav_mode, iconimage, fanart, description, extra)
elif mode==12:
	try:
		name = name.split('\\ ')[1]
	except:
		pass
	try:
		name = name.split('  - ')[0]
	except:
		pass
	rmFavorite(name)
elif mode == 14 : queueItem()
elif mode == 19 : Big_Resolve(name,url)	
elif mode == 20: resolve(name,url)
elif mode == 100: mst3k_season(url)
elif mode == 101: episodes(name)
elif mode == 102: play_fucker(url,name)
elif mode == 103: play_link(url)
elif mode == 104: laughs_(url)
elif mode == 105: genre(url)
elif mode == 106: genre_shows(name,url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))