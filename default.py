import sys, xbmcaddon, xbmcplugin, urllib, urllib2, xbmcgui
import res, time


# plugin constants
__version__ = "1.0"
__plugin__ = "Vplus" + __version__
__url__ = "www.xbmc.com"

# xbmc hooks
__settings__ = xbmcaddon.Addon(id='plugin.video.vplus')
__language__ = __settings__.getLocalizedString
__dbg__ = __settings__.getSetting("debug") == "true"


def OPTIONS():
    re = vplayBrowser.ListResources();
    #addDir('Favorite', res.urls['shows'], 4, re.get_thumb('favorite'), 6)
    addDir('Favorite','http://vplus.ro/shows/' + __settings__.getSetting( "username" ), 7, re.get_thumb('favorite'), 0)
    addDir('Seriale TV', res.urls['serials'], 1, re.get_thumb('serials'), 30)
    addDir('Filme', res.urls['filme'], 8, re.get_thumb('filme'), 30)
    if __settings__.getSetting('last_movie'):
    	import simplejson as json
    	movie = json.loads(__settings__.getSetting('last_movie'))
        addDir(movie['name'], movie['url'], 6, re.get_thumb('last'), 0)    
    addDir('Cauta Seriale','http://vplus.ro/shows/?s', 5, re.get_thumb('search-icon'), 0)    
    addLink('Login','http://vplus.ro/login/', re.get_thumb('login') , 'login', True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def SERIAL(page=None, type=None, search=None):
    #print "SERIAL: page: " + str(page) + " type: " + str(type) + " search: " + str(search)
    if page == None:
        page = 1
    try:
        page = int(page)
    except:
        page = 1
        
    browser = vplayBrowser.ListResources()
    lst = browser.getSerials(page=page, type=type, search=search)
    last_page = browser.getLastPage()
    for i in lst:
        main = res.urls['main']
        url = main + str(i[0])

        addDir(i[1],url, 2, i[3])
    
    page += 1
    mode = 1;
    if search != None:
	mode = 5
    if page < last_page:
        t = browser.get_thumb('next')
        addNext('Next',page, 1, t)
    
    xbmc.executebuiltin("Container.SetViewMode(500)") 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def FILME(url, name, page=None, type=None, search=None):
    if page == None:
        page = 1
    try:
        page = int(page)
    except:
        page = 1
        
    browser = vplayBrowser.ListResources()
    lst = browser.getFilme(page=page, type=type, search=search)
    last_page = browser.getLastPage()
    for i in lst:
        main = res.urls['main']
        url = main + str(i[0])

        addDir(i[1],url, 9, i[3])
    
    page += 1
    mode = 8;
    if search != None:
	mode = 9
    if page < last_page:
        t = browser.get_thumb('next')
        addNext('Next',page, 1, t)
    
    xbmc.executebuiltin("Container.SetViewMode(500)") 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

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


def VIDEOLINKS(url,name):
    print url
    browser = vplayBrowser.ListResources()
    lst = browser.getEpisodes(url)
    for i in lst:
        url = res.urls['main']
        url = url + str(i[0])
        if len(i[5]) > 0 and i[5].find("Watched") != -1:
            name = str(i[3]) + " (Watched)"
        else:
            name = str(i[3])
        if len(i[5]) > 0 and  i[5].find("subs") != -1:
            name = name + "(Subed)"
        addLink(name, url, i[2], 'play_video', False)
    
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)


def SEZON(url, name):
    import simplejson as json
    movie = json.dumps({"name": name, "url": url})
    __settings__.setSetting('last_movie', movie)
    browser = vplayBrowser.ListResources()
    lst = browser.getSesons(url)
    for i in lst:
        url = res.urls['browse']
        url = url + str(i[0])
        addDir(i[-1],url, 3, '')
    
    xbmc.executebuiltin("Container.SetViewMode(550)") 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def FILM(url, name):
    import simplejson as json
    movie = json.dumps({"name": name, "url": url})
    __settings__.setSetting('last_movie', movie)
    browser = vplayBrowser.ListResources()
    lst = browser.getFilme(url)
    for i in lst[0:1]:
        url = res.urls['browse']
        url = url + str(i[0])
        addLink(name, url, i[2], 'play_video', False)
    xbmc.executebuiltin("Container.SetViewMode(550)") 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def FAVORITES(url, name):
    import simplejson as json
    browser = vplayBrowser.ListResources()
    lst = browser.getFavorites(url)
    for i in lst:
        main = res.urls['main']
        url = main + str(i[0])

        addDir(i[1],url, 2, i[3])
    
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def addNext(name,page,mode,iconimage):
    u=sys.argv[0]+"?url="+str(page)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addDir(name,url,mode,iconimage, len = 0):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems = len)
    return ok

def addLink(name,url,iconimage,action, watched):
    ok=True
    url=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&action="+ str(action) + "&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    infolabels = {}
    infolabels["Title"] = name
    if watched==True:
	infolabels['playcount'] = 1           
    liz.setInfo( type="Video", infoLabels=infolabels )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def checkVideoLink(url):
    return url
    import vplayCommon
    resp = urllib2.urlopen(vplayCommon.HeadRequest(url))
    newurl = resp.geturl();
    if newurl != url:
	print "CHECK URL: OLD VIDEO URL: " + url
	print "CHECK URL: NEW VIDEO URL: " + newurl
    return newurl

def startPlugin():
    params=get_params()
    url=None
    name=None
    mode=None
    action=None

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
    try:
        action = str(params['action'])
    except:
        pass

    print "Mode: "+str(mode)
    print "URL: "+str(url)
    print "Name: "+str(name)
    print "Handle: "+sys.argv[1]


    if mode==None or url==None or len(url)<1:
        if action == None:
            print "mode 0"
            OPTIONS()
            #__login__.login(login=True)
    elif mode==1 and action==None:
        print "mode 1"
        SERIAL(url, "Categorii")
    elif mode==2 and action==None:
        print "mode 2"
        SEZON(url, name)
    elif mode==3 and action==None:
        print "mode 3"
        VIDEOLINKS(url,name)
    elif mode==4 and action==None:
        print "mode 3"
        SERIAL(url, "Favorite")
    elif mode==5:
	if url.isdigit():
		SERIAL(url, "Search", __settings__.getSetting( "search" )); 
	else:
        	__search__.search()
		if __search__.getResponse() != None:
            		SERIAL(None, "Search", __search__.getResponse() )
    elif mode==6 and action==None:
        print "mode 6"
        SEZON(url, name)
    elif mode==7 and action==None:
        FAVORITES(url, name)
    elif mode==8 and action==None:
        FILME(url, name)
    elif mode==9 and action==None:
        FILM(url, name)
    elif mode==10:
	if url.isdigit():
		FILME(url, "Search", __settings__.getSetting( "search" )); 
	else:
        	__search__.search()
		if __search__.getResponse() != None:
            		FILME(None, "Search", __search__.getResponse() )
        
    if action == 'play_video':
        details = __link__.getRealLink(url)
        print details

	details['url'] = checkVideoLink(details['url'])

        player = xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ) 
        player.play(details['url'])
        while not player.isPlaying():
            time.sleep(1)
            
        #print "DEFAULT: -->" + str(details['subs'])
        s = None
        if 'ro' in details['subs']:
            s = details['subs']['ro']
        elif 'en' in details['subs']:
            s = details['subs']['en']
        if s != None:
            player.setSubtitles(s)
    elif action == 'login':
        __login__.login(display=True)


if (__name__ == "__main__" ):
    import login, search
    __search__ = search.Search()
    __login__ = login.Login()
    __login__.login();
    import vplayBrowser
    import vplayCommon
    import vplayScraper
    __link__ = vplayBrowser.linkResolution()
    startPlugin()


