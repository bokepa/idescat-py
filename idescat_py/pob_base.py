# -*- coding:utf-8 -*-

from base import Base
from excepcions import *
import re
import urllib.request as req
from urllib.request import Request, urlopen


class PobBase(Base):
    "Prepara la petició a l'API"
    servei = 'pob'
    
    def setOperacio(self, op):
        "Configura l'operació del servei"
        if op in ['cerca', 'sug']:
            self.op = op
            if self.op == 'cerca':
                self.q = None
                self.tipus = None
        else:
            raise OperacioNoPermesa('Operació no permesa. Triï entre "cerca" o "sug"')

    def addCommonParamQ(self, q):
        "Afegeix un paràmetre 'q' a l'URL"
        #TODO control error
        q = str(q)
        if (len(q)>1):
            self.q = q
        else:
            raise PobBaseParamQNoPermes('La longitud ha de ser més gran de 1')
            
    def addCommonParamTipus(self, tipus):
        "Afegeix un paràmetre 'tipus' a la URL"
        tipus = str(tipus)
        if tipus in ['cat','prov','mun','com']: #ToDo, més tipus
            self.tipus = tipus
        else:
            raise PobBaseParamTipusNoPermes('El filtre "tipus" només pot ser un string')
     #dhj 
    
    def addCercaParamSim(self, sim):
	    sim = str(sim)
	    if sim in ['0','1','2']:
	        self.sim = sim
	    else:
		    raise PobBaseParamSimNoPermeses('Parametres no permesos')
		
	# def addCercaParamSelect(self, selec):
	# 	selec = str(selec)
	
	# def addCercaParamOrderby(self, order):
	# 	order = str(order)
		
	# def addCercaParamPosicio(self, posicio):
	# 	posicio = str(posicio)
		
	# Common getters
	
    def getOperacio(self):
        "Retorna l'operació especificada a setOperacio()"
        # sobreescrivint Base.getOperacio()
        return self.op
    
    def getServei(self):
        "Retorna el servei que és sempre 'pob'"
        # sobreescrivint Base.getServei()
        return self.servei

    def __getUrlCerca(self):
        "Construcció específica de l'URL per l'operació dades"
        if self.q or self.tipus:
        	self.afegeixUrl('&p=')

        if self.q:
            self.afegeixUrl('q/', self.q)
        if self.tipus:
            self.afegeixUrl('tipus/', self.tipus)

    def __getUrlSug(self):
        "Construcció específica de l'URL per l'operació dades"
        if not (self.q or self.tipus):
            raise FiltreObligatori("Dins l'operació 'dades' és obligatori especificar el paràmetre 'id' o el 'i'")
        
        if self.i:
            self.afegeixUrl('&i=', self.i)
        if self.tipus:
            self.afegeixUrl('&tipus=', self.tipus)
        
    def getUrl(self):
        "Retorna l'url de la petició"
        if self.op == None:
            raise OperacioNoEspecificada("Error en especificar l'operació: és un paràmetre obligatori!")
        # cridem a la funció superior per obtenir l'url + bàsic
        self.url = super(PobBase,self).getUrl()
        if self.op == 'cerca':
            self.__getUrlCerca()
        if self.op == 'sug' and self.tipus:
            self.__getUrlSug()
        return self.url

    def getData(self):
	    '''Obté les dades -> string'''
	    url = ''.join(self.getUrl())
	    print ("Connexting to ..."+url)
	    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	    sol = urlopen(request)
	    self.data = sol.read().decode('utf-8')
	    return self.data
	    #print (self.data)

data = None

def buscaId(s):
    if globals()['data']:
        return __parse(s, data)  # evitem tornar a fer la petició!
    else:
        import urllib.request as req # ho importem dins la funció
        from io import StringIO # i només per primera vegada
        url = 'http://api.idescat.cat/pob/v1/nodes.json'
        sol = req.urlopen(url)
        globals()['data'] = sol.read().decode('utf-8')
        return __parse(s, data)

def __parse(value, obj):
    obj = obj.split(',"')
    result = None
    for i in range(len(obj)):
        if value in obj[i]:
            result = obj[i+1]  # traiem la resta que no
            result = result[5:-1]  # ens interessa
            return result
    if result == None:
        print("No s'ha trobat l'id")
        
def debug():
    "Per facilitar la feina de depuració"
    global c
    c = PobBase()
    c.setOperacio('cerca')
    #.addId(buscaId('Collbató'))
    #c.addTipus('com,cat')


    
