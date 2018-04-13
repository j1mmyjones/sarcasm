# -*- coding: utf-8 -*-

import xbmcplugin, xbmc, xbmcaddon, urllib, xbmcgui, traceback, requests, re, os, base64
from lib import process
from BeautifulSoup import BeautifulSoup
import os, shutil, xbmcgui
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.sharemovies')
ICON = ADDON_PATH + '/icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
USERDATA_PATH = xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = USERDATA_PATH + '/plugin.video.sharemovies/'
favourites = ADDON_DATA + 'favourites'
if os.path.exists(favourites) == True:
    FAV = open(favourites).read()
else:
    FAV = []

base = 'http://sharemovies.net/'

def Main_Menu():
    Menu('Recently Added Movies',base,105,ICON,FANART,'','')
    Menu('Recently Added Tv Series',base,105,ICON,FANART,'','')
    Menu('Cinema Movies',base+'cinema-movies.html',100,ICON,FANART,'','')
    Menu('Tv Shows',base+'tv-series.html',106,ICON,FANART,'','')
    Menu('Country','',102,ICON,FANART,'','')
    Menu('Release',base,103,ICON,FANART,'','')
    Menu('Genres',base,104,ICON,FANART,'','')
    Menu('Cartoons',base+'cartoon.html',106,ICON,FANART,'','')
    Menu('Anime Series',base+'anime-series.html',106,ICON,FANART,'','')


#100
def mline_vids(url):
    html = process.OPEN_URL(url)
    match = re.compile('<div class="poster item-flip">.+?href="(.+?)".+?<img src="(.+?)".+?<div class="title">.+?>(.+?)</a>.+?<div class="shortStory">(.+?)</div>',re.DOTALL).findall(html)
    Next = re.compile('<a class="pagecurrent".+?href=(.+?) onClick=',re.DOTALL).findall(html)

    for url,img,name,desc in match:
        if 'Season' in name:
            process.Menu(name.replace('&amp;','&'),url,107,img,FANART,desc,'')
        else:
            process.Menu(name.replace('&amp;','&'),url,101,img,FANART,desc,'')
    for n in Next:
        process.Menu('Next Page',n,100,ICON,FANART,'','')
    


#101
def playlinks(url):
    html = BeautifulSoup(requests.get(url).content)
    conts = html.findAll('div', attrs= {'class' : "server_line"})
    for cont in conts:
        pages = cont.findAll('p', attrs= {'class' : "server_play"})
        for page in pages:
            plays=(page.findAll('a'))
            for play in plays:
                linkpg = play['href']
        servers = cont.findAll('p', attrs= {'class' : "server_servername"})
        for server in servers:
            servez = server.text 
            Play(servez,linkpg,108,ICON,FANART,'','')


#102
def country():
    html = process.OPEN_URL(base)
    match = re.compile('<span>Countries</span>(.+?)</div>',re.DOTALL).findall(html)
    match2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(match))
    for url,name in match2:
        process.Menu(name,url,100,ICON,FANART,'','')


#103
def release():
    html = process.OPEN_URL(base)
    match = re.compile('<span>Years</span>(.+?)</div>',re.DOTALL).findall(html)
    match2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(match))
    for url,name in match2:
        process.Menu(name,url,100,ICON,FANART,'','')

#104
def genre():
    html = process.OPEN_URL(base)
    match = re.compile('<span>Genres</span>.+?<ul class="reset">(.+?)</div>',re.DOTALL).findall(html)
    match2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(match))
    for url,name in match2:
        process.Menu(name,url,100,ICON,FANART,'','')
#105
def recent(name):
    html = process.OPEN_URL(base)
    if 'Series' in str(name):
        block = re.compile('<div class="pname">RECENTLY ADDED TV SERIES(.+?)<div class="clr"></div>',re.DOTALL).findall(html)
        match = re.compile('<div class="poster item-flip">.+?href="(.+?)".+?<img src="(.+?)".+?<div class="title">.+?>(.+?)</a>.+?<div class="shortStory">(.+?)</div>',re.DOTALL).findall(str(block))
        for url,img,name,desc in match:
            Menu(name.replace('&amp;','&'),url,107,img,FANART,desc,'')
    elif 'Movies' in str(name):
        block = re.compile('<div class="pname">RECENTLY ADDED MOVIES(.+?)<div class="clr"></div>',re.DOTALL).findall(html)
        match = re.compile('<div class="poster item-flip">.+?href="(.+?)".+?<img src="(.+?)".+?<div class="title">.+?>(.+?)</a>.+?<div class="shortStory">(.+?)</div>',re.DOTALL).findall(str(block))
        for url,img,name,desc in match:
            Menu(name.replace('&amp;','&'),url,101,img,FANART,desc,'')
#106
def tv_show(url):
    html = process.OPEN_URL(url)
    match = re.compile('<div class="poster item-flip">.+?href="(.+?)".+?<img src="(.+?)".+?<div class="title">.+?>(.+?)</a>.+?<div class="shortStory">(.+?)</div>',re.DOTALL).findall(html)
    Next = re.compile('<a class="pagecurrent".+?href=(.+?) onClick=',re.DOTALL).findall(html)

    for url,img,name,desc in match:
        process.Menu(name.replace('&amp;','&'),url,107,img,FANART,desc,'')
    for n in Next:
        Menu('Next Page',n,106,ICON,FANART,'','')
#107
def get_shop_eps(url,img):
    html = process.OPEN_URL(url)
    match = re.compile('<a class="episode episode_series_link active"(.+?)<div class="section-header">',re.DOTALL).findall(html)
    match2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(match))
    for url,name in match2:
        Menu('Episode '+name,url,101,img,FANART,'','')

#108
def play_playlinks(name,url):
    r = requests.get(url).content
    #print r
    url = re.findall('document.write.+?"([^"]*)', r)[0]
    #print url
    url = base64.b64decode(url)
    #print url
    url = re.findall('src="([^"]*)', url)[0] 
    Big_Resolve(name,url)


def Search():
    Dialog = xbmcgui.Dialog()
    Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    Search_name = Search_title.lower()
    
	
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
                contextMenu.append(('Remove from sharemovies Favorites','XBMC.RunPlugin(%s?mode=12&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to sharemovies Favourites','XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fav_mode=%s&fanart=%s&description=%s)'
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
                contextMenu.append(('Remove from sharemovies Favorites','XBMC.RunPlugin(%s?mode=12&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to share Favourites','XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fav_mode=%s&fanart=%s&description=%s)'
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
elif mode == 100: mline_vids(url)
elif mode == 101: playlinks(url)
elif mode == 102: country()
elif mode == 103: release()
elif mode == 104: genre()
elif mode == 105: recent(name)
elif mode == 106: tv_show(url)
elif mode == 107: get_shop_eps(url,iconimage)
elif mode == 108: play_playlinks(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))