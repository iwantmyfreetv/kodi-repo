import os, sys, re, json
import urllib2
#handler=urllib2.httphandler(debuglevel=1)
#opener = urllib2.build_opener(handler)
#urllib2.install_opener(opener)
# Update path so that praw doesnt complain
reload(sys)

try:
    from xbmc import log
except:
    def log(msg):
        print(msg)

outer_pattern= r'(\[[\w ]+\]\s+acestream://\w+)'
title_pattern= r'\[([\w ]+)\]'
acestream_pattern= r'(acestream://\w+)'

def get_reddits():
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    request = urllib2.Request("https://pastebin.com/raw/C5gN0E2C", None, headers)
    response = urllib2.urlopen(request)
    content= response.read()
    reddits = json.loads(content)
    return reddits


class RedditStreamProvider(object):
    def __init__(self, subRedditEvents):
        self.events = subRedditEvents
        self.reddits= get_reddits()
    
    def get_acestreams(self, event):
        acestreamItems= []
        homeTeam=event['homeTeam']['name'].lower()
        awayTeam=event['awayTeam']['name'].lower()
        for reddit in self.reddits:
            for redditEvent in self.events.get_events(reddit['subreddit']):
                gameTitle=redditEvent['title'].lower()
                if (gameTitle.find(homeTeam) > 0 or gameTitle.find(awayTeam) > 0):
                    redditAcestreamLinks = self.events.get_event_links(redditEvent['submission_id'])
                    for score, quality, acelink in redditAcestreamLinks:
                        acestreamItems.append((acelink, quality+" - "+str(score)))
        return acestreamItems

