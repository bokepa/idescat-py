# -*- coding: utf-8 -*-

from municipi_base import MunicipiBase, buscaId
import urllib.request as req
import xml.etree.ElementTree as etree
from io import StringIO
from excepcions import *

class Municipi(MunicipiBase):
    def __init__(self, op=None):
        '''Inicialitza alguns paràmetres i crida l'__init__ del nivell superior'''
        super(Municipi, self).__init__()
        if op:
            self.setOperacio(op)
        self.setFormat('xml')
        self.data = None
        self.raw = []
        self.apunt = False

    def getData(self):
        '''Obté les dades -> string'''
        url = ''.join(self.getUrlBase())
        sol = req.urlopen(url)
        self.data = sol.read().decode('utf-8')
        return self.data

    def __busca(self, clau):
        r = StringIO(self.data)
        x = etree.parse(r)
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
                    self.raw.append(i.tag) # per self.get_raw()
                    self.raw.append(i.text) # ídem
                    try:
                        self.result.append(i.text.split(',')[0]) # culpa de les <cols>
                    except AttributeError:
                        self.result.append('')  # problemes amb NoneType amb elements buits, fem veure que hi ha un element
                if not self.i:
                    del self.result[0] # depèn de 'f' o 'i' s'ha de treure <c> repetit amb <calt>
                self.apunt = True # per self.get_raw()
                self.result[0] += ':'
                self.result = self.result[:3] # tallem (només per 'i')
                return ' '.join(self.result).strip() # sobren espais per culpa del NoneType (vegeu amunt)
        if not self.result:
            print("No s'ha trobat l'indicador")

    def __getitem__(self, clau):
        '''Retorna els valors dels indicadors'''
        if self.data:
            return self.__busca(clau)
        else:
            raise DataError('Primer es necessiten les dades (crideu self.getData())')

    def __get(self):
        if self.i:
            i = self.i.split(',') # tallem self.i
            for a in i:
                yield self.__getitem__(a) # pausem la funció!
        else:   
            print('Aquesta funció només funciona si s\'ha sepecificat el filtre "i"')
        
    def getIndicadors(self, printable=True):
        '''Mostra els valors dels indicadors'''
        for i in self.__get():
            if printable: 
                print(i)
            
    def get_raw(self):  # ES POT FER AMB JSON??
        '''Retorna les dades crues -> tuples list'''
        def dic():
            raw_tags = [self.raw[i] for i in range(0, len(self.raw), 2)] # obtenim una llista amb els tags
            raw_texts = [self.raw[i] for i in range(1, len(self.raw), 2)] # i una amb els valors
            return list(zip(raw_tags, raw_texts))
        if self.apunt:
            return dic()
        else:
            self.getIndicadors(printable=False)  # la cirdem per obtenir self.raw, res més
            return dic()


def debug():
    global c
    c = Municipi('dades')
    c.addId(buscaId('Collbató'))
    c.addI('f321,f262,f33,f271')
    c.getData()

# acabat (sense retocs) 18/05/14
