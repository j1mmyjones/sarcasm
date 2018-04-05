import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os,requests
from lib import clean_name
from lib import process

ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.pantyraiders')
ICON = ADDON_PATH + '/icon.png'
FANART = 'special://home/addons/plugin.video.pantyraiders/fanart.jpg'
Dialog = xbmcgui.Dialog()
List = []



logo = 'https://www.watchmygf.me/images/logo.png'
base= 'https://www.watchmygf.me/'

#1019
def watchmygf_menu():
	process.Menu('Most Popular','https://www.watchmygf.me',1020,logo,FANART,'','')
	process.Menu('Newest','https://www.watchmygf.me/new/',1020,logo,FANART,'','')
	process.Menu('Top Rated','https://www.watchmygf.me/rated/',1020,logo,FANART,'','')
	process.Menu('Most Viewed','https://www.watchmygf.me/popular/',1020,logo,FANART,'','')

#1020
def watchmygf_vids(url):
	html = requests.get(url).content
	match = re.compile('class="item video.+?href="(.+?)".+?class="thumb" src="(.+?)" alt="(.+?)".+?class="icon time"></i>(.+?)</span>.+?</div>',re.DOTALL).findall(html)
	for url,img,name,time in match:
		time = time.strip()
		name = '([COLOR dodgerblue]%s[/COLOR]) %s'%(time,name)
		process.PLAY(name,url,1021,img,FANART,'','')

#1021
def watchmygf_playlink(url):
	html = requests.get(url).content
	match = re.compile('<iframe.+?</iframe>.+?var flashvars.+?video_id.+?video_url: \'(.+?)\'.+?preview_url',re.DOTALL).findall(html)
	for link in match:
		xbmc.Player().play(link)














