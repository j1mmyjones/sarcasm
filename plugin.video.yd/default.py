# -*- coding: utf-8 -*-

import xbmcplugin, xbmc, xbmcaddon, urllib, xbmcgui, traceback, requests, re, os
from lib import process
import os, shutil, xbmcgui
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.yd')
ICON = ADDON_PATH + '/icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
USERDATA_PATH = xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = USERDATA_PATH + '/plugin.video.yd/'
favourites = ADDON_DATA + 'favourites'
if os.path.exists(favourites) == True:
    FAV = open(favourites).read()
else:
    FAV = []

def Main_Menu():
    Menu('Trending','http://ydmoviez.com/most-viewed-movies/',100,ICON,FANART,'','')
    Menu('Featured','http://ydmoviez.com/movies/',100,ICON,FANART,'','')
    Menu('Top Rated','http://ydmoviez.com/top-rated-movies/',100,ICON,FANART,'','')
    Menu('Top Imdb','http://ydmoviez.com/top-imdb-movies/',104,ICON,FANART,'','')
    Menu('Genres','http://ydmoviez.com',102,ICON,FANART,'','')
    Menu('Search','',2,ICON,FANART,'','')


#100
def yd_vids(url):
    html = process.OPEN_URL(url)
    match = re.compile('article id="post-.+?img src="(.+?)" alt="(.+?)"><span class="quality">(.+?)</span><a href="(.+?)".+?class="texto">(.+?)</div>.+?</div></div>',re.DOTALL).findall(html)
    for img,name,rez,url,info in match:
        name = name.replace('&#8217;','\'')
        name = '%s [COLOR red](%s)[/COLOR]'%(name,rez)
        process.Menu(name,url,101,img,FANART,info,info)
    next_page= re.compile('class="pagination".+?class="current".+?href=\'(.+?)\'',re.DOTALL).findall(html)
    for page in next_page:
        process.Menu('Next Page',page,100,ICON,FANART,'','')    

#101
def yd_playlinks(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="metaframe.+?src="(.+?)"\s*frameborder',re.DOTALL).findall(html)
    for link in match:
        host = link.split('//')[1].replace('www.','')
        host = host.split('/')[0].lower()
        host = host.split('.')[0]
        process.PLAY(host,link,19,'','','','')

#102
def yd_cats(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="menu-item menu-item-type-taxonomy menu-item-object-genres menu-item.+?href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(html)
    for url,name in match:
        process.Menu(name,url,100,ICON,FANART,'','')

#103
def yd_in_search(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="result-item">.+?href="(.+?)".+?src="(.+?)" alt="(.+?)".+?class="contenido"><p>(.+?)</p>.+?</article>',re.DOTALL).findall(html)
    for url,img,name,info in match:
        process.Menu(name,url,101,img,FANART,info,'')

#104
def yd_top_imdb(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="top-imdb-item".+?href="(.+?)"><img src="(.+?)".+?class="title"><a href=".+?">(.+?)</a></div></div>',re.DOTALL).findall(html)
    for url,img,name in match:
        process.Menu(name,url,101,img,FANART,'','')


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
elif mode == 100: yd_vids(url)
elif mode == 101: yd_playlinks(url)
elif mode == 102: yd_cats(url)
elif mode == 103: yd_in_search(url)
elif mode == 104: yd_top_imdb(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))