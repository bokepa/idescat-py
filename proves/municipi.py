# -*- coding:utf-8 -*-

from base import Base
from excepcions import *
import re

class MunicipiBase(Base):
    "Prepara la petició a l'API"
    
    def setOperacio(self, op):
        "Configura l'operació del servei"
        if op in ['dades', 'nodes']:
            self.op = op
            if self.op == 'dades':
                self.id = None
        else:
            raise OperacioNoPermesa('Operació no permesa. Triï entre "dades" o "nodes"')

    def addId(self, id):
        "Afegeix un paràmetre 'id' a l'URL"
        if self.op == 'dades' and re.match(r'\d{5}$', id):
            self.id = id
        else:
            raise IdNoPermes('El filtre "id" només pot ser un string de 5 xifres')
        if self.op == None:
            raise OperacioNoEspecificada('Trieu abans una operació!')
        elif self.op != 'dades':
            raise IdNoPermes("Error en especificar el filtre: el filtre 'id' només és permès per a l'operació 'dades'" \
            "(actualment teniu configurada l'operació %s)" % self.op)

    def addI(self, i):
        if type(i) is not str:
            raise INoPermes('El filtre "i" ha de ser un string')     
        if re.match(r'f\d\d\d?', i):
            self.i = i
        else:
            raise INoPermes('El filtre "i" ha de ser de la forma "f\d\d\d?"')
            
    def getOperacio(self):
        "Retorna l'operació especificada a setOperacio()"
        # sobreescrivint Base.getOperacio()
        return self.op
    
    def getServei(self):
        "Retorna el servei que és sempre 'onomastica'"
        # sobreescrivint Base.getServei()
        return 'emex'

    def __getUrlDades(self):
        "Construcció específica de l'URL per l'operació dades"
        if not self.id:
            raise FiltreObligatori("Dins l'operació 'dades' és obligatori especificat el paràmetre 'id'")
        try:
            self.afegeixUrl('&id=', self.id)
        except Exception: # si algun paràmetre no és especificat ens ho saltem silencionsament
            pass # amb l''id' n'hi ha prou
            
    def getUrlBase(self):
        "Retorna l'url de la petició"
        if self.op == None:
            raise OperacioNoEspecificada("Error en especificar l'operació: és un paràmetre obligatori!")
        # cridem a la funció superior per obtenir l'url + bàsic
        self.url = super(MunicipiBase, self).getUrlBase()
        if self.op == 'dades':
            self.__getUrlDades()
        return self.url

def debug():
    "Per facilitar la feina de depuració"
    global c
    c = MunicipiBase()
    c.setOperacio('dades')
    c.addId('44444')
