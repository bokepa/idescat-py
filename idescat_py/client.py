from pob_base import PobBase
import json
from io import StringIO

global c
c = PobBase()
c.setOperacio('cerca')
c.addCommonParamTipus('mun')
# Format. Default is JSON c.setFormat('xml')
#print (c.getUrl())
data = c.getData()

j = json.load(StringIO(data))

#TODO PArse response ang get the data

# try: 
#     print ('trying')
#     content = j['feed']['entry']['content']['content']
#     link = j['feed']['entry']['link']['href']
#     print ('Content')
#     print(content)
#     p(link)
#     print ('finishing')
# except (error):
# 	print ('some exceptio')
# 	print (error)
# 	pass
# except (KeyError, TypeError):
#     try:
#         content1 = j['feed']['entry'][0]['content']['content']
#         content2 = j['feed']['entry'][1]['content']['content']
#         link1 = j['feed']['entry'][0]['link']['href']
#         link2 = j['feed']['entry'][1]['link']['href']
#     except KeyError:
#         print(u'El paràmetre escollit no existeix')
# try:
#     if content2:
#         print(content1, '\t', content2)
#         link = link1 + '\n\t\t ' + link2
#         p(link)
# except UnboundLocalError:
#     pass


