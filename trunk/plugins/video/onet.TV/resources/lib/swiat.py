import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
class Main:
	def __init__( self ) :
		self.getNames()
	def getNames(self):
		gl=[
			("Było sobie..",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=14&tags=%28By%C5%82o_sobie%29&rss=1'),
			("da Vinci Learning",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=14&tags=%28Da_Vinci_Learning%29&rss=1'),
			("Przytulaki",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=14&tags=%28Przytulaki%29&rss=1'),
			("Nauka i Zabawa",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=14&tags=%28Nauka_i_zabawa%29&rss=1'),
			("Wszystkie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=14&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True)