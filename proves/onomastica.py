# -*- coding:utf-8 -*-

from base import Base

class Onomastica(Base):
    "Prepara i fa la petició a l'API"
    
    def setOperacio(self, op):
        if op in ['dades', 'cerca', 'sug']:
            self.op = op
        else:
            print('Operació no permesa. Triï entre "dades", "cerca" o "sug"')

    def setSub(self, sub):
        if sub in ['noms', 'cognoms', 'nadons']:
            self.subservei = sub
        else:
            print('Subservei no permès. Triï entre "noms", "cognoms" o "nadons"')

    def getOperacio(self):
        return self.op

    def getServei(self):
        return 'onomastica'

    def getUrlBase(self):
        try:
            self.url = super(Onomastica, self).getUrlBase()
        except AttributeError:
            print("Error en especificar l'operació: és un paràmetre obligatori!")
        try:
            self.url.insert(5, self.subservei)
            if self.subservei == 'dades':
                pass # per fer!!!!
            self.url.insert(6, '/')
            return self.url
        except AttributeError:
            print("Error en especificar el subservei: és un paràmetre obligatori!")
            
        
        
