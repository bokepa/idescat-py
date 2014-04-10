# -*- coding:utf-8 -*-

from base import Base
from excepcions import *

class Onomastica(Base):
    "Prepara la petició a l'API"
    
    def setOperacio(self, op):
        "Configura l'operació del servei"
        if op in ['dades', 'cerca', 'sug']:
            self.op = op
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
        try:
            if self.op == 'dades':
                if type(i) is str:
                    print("ATENCIÓ: l'operació no acceptarà cap més paràmetre")
                    if input("Voleu continuar? (s/n): ") == 's':
                        self.id = i
                elif type(i) is int:
                    self.id = i
                else:
                    raise FiltreNoPermes('El paràmetre "id" només pot ser un string o un enter')
            else:
                raise FiltreNoPermes("Error en especificar el filtre: el filtre 'id' només és permès per a l'operació 'dades'" \
                "(actualment teniu configurada l'operació %s)" % self.op)
        except AttributeError:
            raise OperacioNoEspecificada('Trieu abans una operació!')

    def getOperacio(self):
        "Retorna l'operació especificada a setOperacio()"
        # sobreescrivint Base.getOperacio()
        return self.op
    
    def getServei(self):
        "Retorna el servei que és sempre 'onomastica'"
        # sobreescrivint Base.getServei()
        return 'onomastica'

    def __urlDades(self, s):
        "Construcció específica de l'URL per l'operació dades"
        pass # per fer!!!!

    def getUrlBase(self):
        "Retorna l'url de la petició"
        try:
            # cridem a la funció superior per obtenir l'url + bàsic
            self.url = super(Onomastica, self).getUrlBase()  
        except AttributeError:
            raise OperacioNoEspecificada("Error en especificar l'operació: és un paràmetre obligatori!")
        try:
            self.url.insert(5, self.subservei)
            self.url.insert(6, '/')
            if self.op == 'dades':
                self.__urlDades(self.url)
            return self.url
        except AttributeError:
            raise SubserveiNoEspecificat("Error en especificar el subservei: és un paràmetre obligatori!")

def debug():
    "Per facilitar la feina de depuració"
    global c
    c = Onomastica()
    c.setOperacio('dades')
    c.setSub('noms')
