import os, sys, re, time
reload(sys)

try:
    from xbmc import log
except:
    def log(msg):
        print(msg)

class GameClient(object):
    def __init__(self, gameDataProvider, acestreamLinkProvider):
        self.gameDataProvider= gameDataProvider
        self.acestreamLinkProvider=acestreamLinkProvider

    def get_games(self, competition_id):
        gameData= self.gameDataProvider.get_game_data()
        games=[]
        for i in gameData:
            if (str(i['id'])==str(competition_id)):
                for g in i['events']:
                    if (g['status']['type']!="finished"):
                        streamsForGame= self.acestreamLinkProvider.get_acestreams(g['id'])
                        if (len(streamsForGame)>0):
                            if (g['status']['type']=="inprogress"):
                                prefix=g["homeScore"]['current']+" - "+g['awayScore']['current']+"  "
                                mins= int((time.time()-g["startTimestamp"])/60)
                                suffix="  "+str(mins)+" minutes ago"
                            elif (g['status']['type']=="finished"):
                                suffix= ""
                                prefix=g["homeScore"]['current']+" - "+g['awayScore']['current']+"  "
                            else:
                                prefix= g["startTime"]+"  "
                                suffix= ""
                            if (g['status']['type']!="finished"):
                                suffix+= "  ["+str(len(streamsForGame))+" Streams]"
                            title= prefix+ g['name']+ suffix
                            games.append(
                                (title, g['id'])
                            )
        return games
