import os, sys, re, json
import urllib2
#handler=urllib2.HTTPHandler(debuglevel=1)
#opener = urllib2.build_opener(handler)
#urllib2.install_opener(opener)
reload(sys)

try:
    from xbmc import log
except:
    def log(msg):
        print(msg)

class GameDataProvider(object):
    def __init__(self):
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        request = urllib2.Request('http://darsh.sportsvideo.net/api/top-matches-footybit?timezone=UTC', None, headers)
        response = urllib2.urlopen(request)
        content= response.read()
        self.gameData = json.loads(content)

    def get_game_data(self):
        return self.gameData