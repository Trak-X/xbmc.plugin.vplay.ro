import re

class Scrap:

    def scrapFavorite(self, page):
        pos = page.find("<h2>Seriale");
        if pos == -1:
            return [];
        page = page[:pos]
        match=re.compile('<a href="(/show/.+?/)" title="(.+?)"><span class="coll_poster" title="(.+?)" style="background-image:url\((.+?)\);"></span>').findall(page);
        return match


    def scrapFavorites(self, page):
        pos = page.find('<h2 style="color:#3b5998; font-size:17px; ">Cole');
        if pos == -1:
            return [];
        page = page[pos:]
        pos = page.find('<div id="footer" class="foooter-wrap">');
        if pos == -1:
            return [];
	    page = page[:pos]
        match=re.compile('<a href="(/show/.+?/)" title="(.+?)" style="float:left;" >\n*?\s*?<span class="coll_poster" title="(.+?)" style="background-image:url\((.+?)\);float:left;"></span>').findall(page);
        return match

    def scrapSearch(self, page):
        match=re.compile('<a href="(/show/.+?/)" title="(.+?)"><span class="coll_poster" title="(.+?)" style="background-image:url\((.+?)\);"></span>').findall(page)
        return match

    def scrapSearchf(self, page):
        match=re.compile('<a href="(.+?)" title="(.+?)"><span class="movie_poster" title="(.+?)" style="background-image:url\((.+?)\);"></span>').findall(page)
        return match
        
    def scrapSerials(self, page):
        print "Scrap Seriale"
        pos = page.find("<h2>Seriale");
        if pos == -1:
            return [];
        page = page[pos:]
        match=re.compile('<a href="(/show/.+?/)" title="(.+?)"><span class="coll_poster" title="(.+?)" style="background-image:url\((.+?)\);"></span>').findall(page);
        return match

    def scrapFilme(self, page):
        print "Scrap Filme"
        pos = page.find("<h2>Filme");
        if pos == -1:
            return [];
        page = page[pos:]
        match=re.compile('<a href="(.+?)" title="(.+?)"><span class="movie_poster" title="(.+?)" style="background-image:url\((.+?)\);"></span>').findall(page);
        return match

        
    def scrapSeasons(self, page):
        match=re.compile('href="(/show/.+?/\d+/)"><span>(Sezonul \d+)</span>').findall(page)
        return match
        
    def scrapEpisodes(self, page):
        #match = re.compile('<a href="(.+?)" title="(.+?)" class="coll-episode-box">\s*<span class="thumb" style="background-image:url\((.+?)\);"></span>\s*<span class="title" title="(.+?)">(.+?)</span>([.|\s|\t]+?)</a>').findall(page);
        match = re.compile('<a href="(.+?)" title="(.+?)" class="coll-episode-box">\s*<span class="thumb"><span style="background-image:url\((.+?)\);"></span></span>\s*<span class="title" title="(.+?)">(.+?)</span>((.|\n)*?)</a>').findall(page);
        print match[0]
        return match
        
    def scrapEpisodeId(self, page):
        match=re.compile('http://vplus.ro/watch/(.+?)/').findall(page)
        return match
        
    def scrapLastPage(self, page):
        match=re.compile('href="/show/1g6g9v5m/2/"><span>Sezonul 2</span>').findall(page)
        print "TESTTTTT"
        print page
        print match
        return match
