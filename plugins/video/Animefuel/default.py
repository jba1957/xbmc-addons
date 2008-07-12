import urllib,urllib2,re,sys,xbmcplugin,xbmcgui

#Animefuel Plugin - By Voinage 2008.


def ExtractMediaUrl(url, data):
        
        if url.find("megavideo.com") > 0:
                codeRegex = '<ROW url="(.+?)" runtime=".+?" runtimehms=".+?" size=".+?" waitingtime=".+?" k=".+?"></ROW>'
                codeResults = re.findall(codeRegex, data, re.DOTALL + re.IGNORECASE)
                if len(codeResults) > 0:
                        code = codeResults[-1]
                        dictionary = {"0":":","%24": ".", "%25": "/", "%3A": "0", "%3B": "1", "8": "2", "9": "3", "%3E": "4", "%3F": "5", "%3C": "6", "%3D": "7", "2": "8", "3": "9", "a": "k", "b": "h", "c": "i", "d": "n", "e": "o", "f": "l", "g": "m", "h": "b", "i": "c", "k": "a", "l": "f", "m": "g", "n": "d", "o": "e", "p": "z", "s": "y", "%7E": "t", "y": "s","%7C": "v", "%7D": "w", "z": "p"}
                        return RegexReplaceDictionary(code, dictionary) 
                else:
                        return ""
        
def RegexReplaceDictionary(string, dictionary):
      
        rc = re.compile('|'.join(map(re.escape, dictionary)))
        def Translate(match):
                return dictionary[match.group(0)]
        return rc.sub(Translate, string)

def CATS():
        cat=[("http://www.animefuel.com", "Anime"),("http://www.animefuel.com/anime-movies/", "Anime Movies")]
        for url,name in cat:
                addDir(name,url,1,"")

def INDEX(url,name):
        res=[("http://www.animefuel.com/guyver-out-of-control/","Guyver Out of Control Movie"),("http://www.animefuel.com/category/g/the-guyver-bioboosted-armor-ova/","Guyver Bio Boosted Armour Ova"),("http://www.animefuel.com/category/g/guyver-the-bioboosted-armor/","Guyver Bio Boosted Armour")]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('#8217;','',link)
        code2=re.sub('.+?<span></span>','',code)
        code3=re.sub('news','',code2)
        code4=re.sub('&s','s',code3)
        response.close()
        p=re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a> </li>')
        p=re.compile('<li><a href="(.+?)">(.+)</a>+?.+?span style="color:#fc3737;font-size:12px;">')
        p=re.compile('<li><a href="(.+?)">(.+?)</a>')
        match=p.findall(code4)
        for url,name in match:
                res.append((url,name))
        for url,name in res:
                addDir(name,url,2,"")

def INDEX2(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<h2 id="post-.+?"><a href="(.+?)" rel=".+?" title=".+?">(.+?)</a></h2>')
        match=p.findall(link)
        for url,name in match:         
                addDir(name,url,3,"")
                pass
        p=re.compile('\r\n\r\n\t\t\t\t<span class="ppre"><a href="(.+?)">&.+?; (.+?)</a></span>')
        match=p.findall(link)
        for Previouspage,name in match:
                addDir(name,Previouspage,2,"")


def VIDLINK(url):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()        
        p=re.compile('\r\n\r\n<p><embed src="http://www.veoh.com\/.+?.swf\?player=videodetailsembedded&#038;type=v&#038;permalinkId=(.+?)&#038;id=.+?"')
        match=p.findall(link)
        for a in match:
                f=urllib2.urlopen("http://www.veoh.com/rest/video/"+str(a)+"/details")
                veo=f.read()
                comp=re.compile('fullPreviewHashPath="(.+?)"')
                for url in comp.findall(veo):
                        addLink("VEOH LOW QUALITY",url,"")
                addLink("VEOH AVI","http://127.0.0.1:64653/"+str(a)+"?.avi","")
        # Veoh 2
        p=re.compile('<embed src="http://www.veoh.com\/.+?.swf\?permalinkId=(.+?)\&#038;id=.+?;player=videodetailsembedded&#038;videoAutoPlay=0"')
        match=p.findall(link)
        for a in match:
                f=urllib2.urlopen("http://www.veoh.com/rest/video/"+str(a)+"/details")
                veo=f.read()
                comp=re.compile('fullPreviewHashPath="(.+?)"')
                for url in comp.findall(veo):
                        addLink("VEOH NORMAL",url+"?.avi","")
                addLink("VEOH AVI","http://127.0.0.1:64653/"+str(a)+"?.avi","")
                        
        #Dailymotion
        p=re.compile('<embed src="http://www.dailymotion.com/swf/(.+?)&#038.+?" type="application/x-shockwave-flash"')
        match=p.findall(link)
        for url in match:
                linkage="http://www.dailymotion.com/video/"+url
                
        try:
                req = urllib2.Request(linkage)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('url=rev=.+?&uid=.+?&lang=en&callback=.+?&preview=.+?&video=(.+?)%40%40spark')
                match=p.findall(link)
                for url1 in match:
                        decode=urllib.unquote(url1)
                        url2="http://www.dailymotion.com"+decode
                addLink("DAILYMOTION VIDEO",url2,"")
        except UnboundLocalError:
                pass
        # Megavideo.
        p=re.compile('<embed src="(.+?)" type="application/x-shockwave-flash"')
        match=p.findall(link)
        for a in match:
                if len(a)<79 and a.find('megavideo'):
                        a=a[:-43]
                        code=re.sub('http://www.megavideo.com/v/','v=',a)
                        url="http://www.megavideo.com/xml/videolink.php?"+code
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        new=ExtractMediaUrl(url,link)
                        flvappend="voinage.flv"
                        flvlink=new+flvappend
                        addLink("MEGAVIDEO LINK",flvlink,"")
                     
                
                elif len(a)<80 and a.find('megavideo'):
                                a=a[:-44]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("MEGAVIDEO LINK",flvlink,"")
                          
                                        
                                
                else:
                        if len(a)==80 and a.find('megavideo'):
                                a=a[:-45]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("MEGAVIDEO LINK",flvlink,"")
       
        #Myspace
        p=re.compile('<p><a href=".+?videoid=(.+?)">.+?</a>')
        match=p.findall(link)
        for a in match:
                f=urllib2.urlopen("http://mediaservices.myspace.com/services/rss.ashx?type=video&mediaID="+str(a))
                myspace=f.read()
                comp=re.compile('<media:content url="(.+?)"')
                for url in comp.findall(myspace):
                        addLink("MYSPACE LINK",url,"")
        #LIVEVIDEO
        p=re.compile('<a href="(.+?)">')
        match=p.findall(link)
        for item in match:
                link = 'http://clipnabber.com/gethint.php'
                data = "mode=1&url="+item
                req = urllib2.Request(link,data)
                response = urllib2.urlopen(req)
                results = response.read()
                p=re.compile(r'<a href=\'(.+?)\' >')
                flv=p.findall(results)
                for url in flv:
                        addLink("LIVE VIDEO",url,"")

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

      
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
       
params=get_params()
url=None
name=None
mode=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
        print "categories"
        CATS()
elif mode==1:
        print "index of : "+url
        INDEX(url,name)
elif mode==2:
        print "show Page: "+url
        INDEX2(url,name)
elif mode==3:
        print "show Page: "+url
        VIDLINK(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
