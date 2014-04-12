# -*- coding:utf-8 -*-

from base import Base
from excepcions import *
import re

class Onomastica(Base):
    "Prepara la petició a l'API"
    
    def setOperacio(self, op):
        "Configura l'operació del servei"
        if op in ['dades', 'cerca', 'sug']:
            self.op = op
            if self.op == 'dades':
                self.id = None
        else:
            raise OperacioNoPermesa('Operació no permesa. Triï entre "dades", "cerca" o "sug"')

    def setSub(self, sub):
        "Configura el subservei"
        if sub in ['noms', 'cognoms', 'nadons']:
            self.subservei = sub
        else:
            raise SubserveiNoPermes('Subservei no permès. Triï entre "noms", "cognoms" o "nadons"')

    def addId(self, i):
        "Afegeix un paràmetre 'id' a l'URL"
        self.id_str = False
        if self.op == 'dades':
            if type(i) is str:
                print("ATENCIÓ: l'operació no acceptarà cap més paràmetre")
                if input("Voleu continuar? (s/n): ") == 's':
                    self.id = i
                    self.id_str = True
            elif type(i) is int:
                self.id = i
            else:
                raise FiltreNoPermes('El paràmetre "id" només pot ser un string o un enter')
        elif self.op == None:
            raise OperacioNoEspecificada('Trieu abans una operació!')
        else:
            raise FiltreNoPermes("Error en especificar el filtre: el filtre 'id' només és permès per a l'operació 'dades'" \
            "(actualment teniu configurada l'operació %s)" % self.op)

    def addGeo(self, prefix, geo):
        g = prefix + ':' + geo
        print(g)
        if re.match('^%s:\d\d$' % prefix, g):
            if self.id_str:
                raise IdError("No es pot combinat el paràmtre 'id' en forma de string amb cap altre filtre")
            self.geo = g
        
            
    def getOperacio(self):
        "Retorna l'operació especificada a setOperacio()"
        # sobreescrivint Base.getOperacio()
        return self.op
    
    def getServei(self):
        "Retorna el servei que és sempre 'onomastica'"
        # sobreescrivint Base.getServei()
        return 'onomastica'

    def __getUrlDades(self):
        "Construcció específica de l'URL per l'operació dades"
        if not self.id:
            raise FiltreObligatori("Dins l'operació 'dades' és obligatori especificat el paràmetre 'id'")
        self.afegeixUrl('&id=', str(self.id), '&geo=', self.geo)

    def getUrlBase(self):
        "Retorna l'url de la petició"
        if self.op == None:
            raise OperacioNoEspecificada("Error en especificar l'operació: és un paràmetre obligatori!")
        # cridem a la funció superior per obtenir l'url + bàsic
        self.url = super(Onomastica, self).getUrlBase()  
        if self.subservei == None:
            raise SubserveiNoEspecificat("Error en especificar el subservei: és un paràmetre obligatori!")    
        self.url.insert(5, self.subservei)
        self.url.insert(6, '/')
        if self.op == 'dades':
            self.__getUrlDades()
        return self.url

def debug():
    "Per facilitar la feina de depuració"
    global c
    c = Onomastica()
    c.setOperacio('dades')
    c.setSub('noms')
    c.addId(2500)
    c.addGeo('com', '01')
