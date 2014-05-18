from municipi_base import MunicipiBase, buscaId
import urllib.request as req
import xml.etree.ElementTree as etree
from io import StringIO
from excepcions import *

class Municipi(MunicipiBase):
    def __init__(self, op=None):
        super(Municipi, self).__init__()
        if op:
            self.setOperacio(op)
        self.setFormat('xml')
        self.data = None

    def getData(self):
        url = ''.join(self.getUrlBase())
        sol = req.urlopen(url)
        self.data = sol.read().decode('utf-8')
        return self.data

    def __getitem__(self, clau):
        if self.data:
            raw = StringIO(self.data)
            x = etree.parse(raw)
            root = x.getroot()
            element = None
            if self.i:
                element = 'i' # si s'ha especificat self.i l'element és també 'i'
            if clau == 'f271':
                clau = 'f261'  # superfície, km2
            self.result = []
            for e in root.iter(element or 'f'): 
                if e.attrib['id'] == clau:
                    for i in e.getchildren():
                        try:
                            self.result.append(i.text.split(',')[0]) # culpa de les <cols>
                        except AttributeError:
                            pass  # problemes amb NoneType amb elements buits
                    if not self.i:
                        del self.result[0] # depèn de 'f' o 'i' s'ha de treure <c> repetit amb <calt>
                    self.result[0] += ':'
                    self.result = self.result[:3] # tallem (només per 'i')
                    return ' '.join(self.result)
        else:
            raise DataError('Primer es necessiten les dades (crideu self.getData())')
        if not self.result:
            print("No s'ha trobat l'indicador")

    def __get(self):
        if self.i:
            i = self.i.split(',') # tallem self.i
            for a in i:
                yield self.__getitem__(a) # pausem la funció!
        else:
            print('Aquesta funció només funciona si s\'ha sepecificat el filtre "i"')
        
    def getIndicadors(self):
        for i in self.__get():
            print(i)

def debug():
    global c
    c = Municipi('dades')
    c.addId(buscaId('Pallars Jussà'))
    c.addI('f2,f3,f4,f271')
    c.getData()
        
