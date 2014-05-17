from municipi_base import MunicipiBase, buscaId
import urllib.request as req
import xml.etree.ElementTree as etree
from io import StringIO

class Municipi(MunicipiBase):
    def __init__(self, op=None):
        super(Municipi, self).__init__()
        if op:
            self.setOperacio(op)
        self.setFormat('xml')
        self.data = None

    def get(self):
        url = ''.join(self.getUrlBase())
        sol = req.urlopen(url)
        self.data = sol.read().decode('utf-8')
        return self.data

    def __getitem__(self, clau):
        if self.data:
            raw = StringIO(self.data)
            x = etree.parse(raw)
            root = x.getroot()
            for e in root.iter('f'): # addI(), necessitem 'i' en lloc de 'f'!! per fer!
                if e.attrib['id'] == clau:
                    result = []
                    for i in e.getchildren(): 
                        result.append(i.text.split(',')[0])
                    del result[0]
                    result[0] += ':'
                    return ' '.join(result)
        else:
            pass # raise...

def debug():
    global c
    c = Municipi('dades')
    c.addId(buscaId('Pallars Jussà'))
    c.addI('f2')
    c.get()
        
