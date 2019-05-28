# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os,requests
from lib import clean_name
from lib import process
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.pantyraiders')
ICON = ADDON_PATH + '/icon.png'
FANART = 'special://home/addons/plugin.video.pantyraiders/fanart.jpg'
Dialog = xbmcgui.Dialog()
List = []

#1007
def porn_300_menu():
    process.Menu('Top Rated','https://www.porn300.com/top-rated/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
    process.Menu('Most Viewed','https://www.porn300.com/most-viewed/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
    process.Menu('Starz','https://www.porn300.com/pornstars/',1012,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
    process.Menu('VR Vidz','https://www.porn300.com/channel/vr-bangers/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
    process.Menu('Categories','https://www.porn300.com',1010,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
    process.Menu('Channels','https://www.porn300.com/channels/',1013,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
    process.Menu('Search','',1011,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')



#1008
def porn300_playlinks(url):
    html = process.OPEN_URL(url)
    match = re.compile('<div id="video-link".+?data-video="(.+?)"',re.DOTALL).findall(html)
    for link in match:
        xbmc.Player().play(link)

#1009
def porn300_vids(url):
    html = process.OPEN_URL(url)
    match = re.compile('<li class="grid__item.+?href="(.+?)".+?src="(.+?)" alt="(.+?)".+?</ul>.+?</li>',re.DOTALL).findall(html)
    for url,img,name in match:
        name = name.replace('&#039;','\'')
        url = 'https://www.porn300.com'+url
        process.PLAY(name,url,1008,img,FANART,'','')
    next_page= re.compile('<li class="pagination_item" itemprop="url"><a class="btn btn-primary--light btn-pagination" itemprop="name" href="(.+?)" title="Next">',re.DOTALL).findall(html)
    for page in next_page:
        page = 'https://www.porn300.com'+page
        process.Menu('Next Page',page,1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')

#1010
def porn300_cats(url):
    html = process.OPEN_URL(url)
    block = re.compile('class="grid grid--categories(.+?)id="techpump-paginator-ajax',re.DOTALL).findall(html)
    match = re.compile('href="(.+?)".+?gtmname="(.+?)".+?src="(.+?)".+?</li>',re.DOTALL).findall(str(block))
    for url,name,img in match:
        url = 'https://www.porn300.com'+url
        process.Menu(name,url,1009,img,FANART,'','')



    
#1011
def porn300_search():
    Dialog = xbmcgui.Dialog()
    Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    Search_name = Search_title.lower()
    url = 'https://www.porn300.com/search/?q='+Search_name.replace(' ','+')
    porn300_vids(url)

#1012
def porn300_starz(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="grid__item grid__item--pornstar-thumb".+?href="(.+?)".+?image" src=(.+?)alt="(.+?)".+?</ul>.+?</li>',re.DOTALL).findall(html)
    for url,img,name in match:
        # vid_count = vid_count.strip()
        url = 'https://www.porn300.com'+url
        process.Menu(name,url,1009,img,FANART,'','')    

#1013
def porn300_channels(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="grid__item grid__item--producer".+?href="(.+?)".+?image" src="(.+?)" alt="(.+?)".+?</a>.+?</li>',re.DOTALL).findall(html)
    for url,img,name in match:
        url = 'https://www.porn300.com'+url
        process.Menu(name,url,1009,img,FANART,'','')
    next_page= re.compile('class="paginador">.+?class="selected" href=".+?href="(.+?)".+?</li>',re.DOTALL).findall(html)
    for page in next_page:
        page = 'https://www.porn300.com'+page
        process.Menu('Next Page',page,1013,'https://www.porn300.com/android-icon-192x192.png',FANART,'','') 