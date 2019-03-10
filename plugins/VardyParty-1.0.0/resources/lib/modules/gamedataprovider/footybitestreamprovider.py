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

outer_pattern= r'(\[[\w ]+\]\s+acestream://\w+)'
title_pattern= r'\[([\w ]+)\]'
acestream_pattern= r'(acestream://\w+)'

class FootyBiteStreamProvider(object):
    def get_acestreams(self, url):
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        content= response.read()
        matches= re.findall(outer_pattern, content)
        matches.extend(re.findall(acestream_pattern, content))
        unique= set(matches)
        acestreamItems= []
        for item in unique:
            titleMatch= re.findall(title_pattern, item)
            if (len(titleMatch)>0):
                title= titleMatch[0];
            else:
                title= None
            streamUrl= re.findall(acestream_pattern, item)
            if (len(streamUrl)>0):
                acestreamItems.append((streamUrl[0], title))
            else:
                log("DID NOT FIND ACESTREAM LINK IN "+item, 3)
        return acestreamItems