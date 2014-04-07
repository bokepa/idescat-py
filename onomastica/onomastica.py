# onomastica.py
# A little program that helps with searching statistics throw the web
# http://api.idescat.cat

import urllib.request as request
import json
from io import StringIO
from onomasticaGeo import GEO_DICT
import re as regex

for i in ['cognoms', 'noms', 'nadons']:
    exec('REQ_%s = "http://api.idescat.cat/onomastica/v1/%s/cerca.json?q="' % (i.upper(), i))

def p(l):
    print('Per a més informació podeu també visitar el següent/s enllaç:')
    print('\t\t', l, '\n')
    input('Premeu retorn per acabar: ')

def re(pa, tipus, geo=False):
    """Sends the request"""
    if geo:
        if regex.match('com:\d\d', geo):
            com = geo
        else:
            chunk = capi(geo)
            com = GEO_DICT[chunk]
        exec("global req; req = request.urlopen(REQ_%s + pa + '&sim=0&geo=%s')" % (tipus.upper(), com))
    else:
        exec("global req; req = request.urlopen(REQ_%s + pa + '&sim=0')" % tipus.upper())
    return req

def capi(s):
    """Capitalize function"""
    # this seems weird
    if regex.match(".+'", s):
        count = 0
        l = []
        for e in s:
            if e == "'":
                l.append("'")
                l.append(s[count+1].capitalize())
                l.append(s[count+2:])
                break
            else:
                if not count:
                    l.append(e.capitalize())
                    count += 1
                else:
                    l.append(e)
                    count += 1
        return ''.join(l)
    l  = s.split(' ')
    l2 = []
    for e in l:
        l2.append(e.capitalize())
    return ' '.join(l2)

def fes(cog=None, nom=False, nadons=False, geo=False):  
    """Send a request, then process the data"""
    if cog:
        sol = re(cog, 'cognoms', geo=geo)
    if nom:
        sol = re(nom, 'noms', geo=geo)
    if nadons:
        sol = re(nadons, 'nadons', geo=geo)

    #IMPORTANT: change the byte type to str type
    data = sol.read().decode('utf-8')

    # make an object with a read() method, load and get the data

    j = json.load(StringIO(data))
    try:
        content = j['feed']['entry']['content']['content']
        link = j['feed']['entry']['link']['href']
        print(content)
        p(link)
    except (KeyError, TypeError):
        try:
            content1 = j['feed']['entry'][0]['content']['content']
            content2 = j['feed']['entry'][1]['content']['content']
            link1 = j['feed']['entry'][0]['link']['href']
            link2 = j['feed']['entry'][1]['link']['href']
        except KeyError:
            print(u'El paràmetre escollit no existeix')
    try:
        if content2:
            print(content1, '\t', content2)
            link = link1 + '\n\t\t ' + link2
            p(link)
    except UnboundLocalError:
        pass
