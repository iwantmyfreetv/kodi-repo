import os, sys, re, json
import urllib2
#handler=urllib2.httphandler(debuglevel=1)
#opener = urllib2.build_opener(handler)
#urllib2.install_opener(opener)
reload(sys)

try:
    from xbmc import log
except:
    def log(msg):
        print(msg)

def normalise(linkSet):
    normalised= {}
    for acestreamUrl, title in linkSet:
        if (acestreamUrl not in normalised or str(normalised[acestreamUrl]=="")):
            normalised[acestreamUrl]= title
    normalisedLinkSet=[]
    for key in normalised:
        normalisedLinkSet.append((key, normalised[key]))
    return normalisedLinkSet

class AcestreamLinkProvider(object):
    def __init__(self, gameDataProvider, redditStreamProvider, footyBiteStreamProvider):
        self.gameDataProvider = gameDataProvider
        self.redditStreamProvider = redditStreamProvider
        self.footyBiteStreamProvider = footyBiteStreamProvider

    def get_acestreams(self, game_id):
        gameData=  self.gameDataProvider.get_game_data()
        acestreamItems=[]
        for competition in gameData:
            for event in competition['events']:
                if (str(event['id'])==str(game_id)):
                    fooyBiteUrl= event['redditEventLink']
                    if (fooyBiteUrl!=None):
                        acestreamItems.extend(self.footyBiteStreamProvider.get_acestreams(fooyBiteUrl))
                    acestreamItems.extend(self.redditStreamProvider.get_acestreams(event))
        return normalise(acestreamItems)
