# -*- coding: UTF-8 -*-

"""
Módul que serveix de base per a fer les peticions a l'API d'idescat incialitzant
les dades comunes en totes elles.

ATENCIÓ: Necessita ser implementat en una classe filla per funcionar (vegeu
comentaris)
"""

class Base():
    "Inicialitza les constants del programa. Pensada només per ser implementada"
    REQ = "http://api.idescat.cat/"
    PARAM_LANG = "?lang=" 
    PARAM_CODIFICACIO = "&enc="
    
    def __init__(self):
        "Inicialitza valors per defecte"
        self.versio = 'v1'
        self.codificacio = 'utf-8'
        self.format = 'json'
        self.lang = 'ca'
    
    def setFormat(self, f):
        "Configura el format de la resposta de la petició"
        # totes les set[..] s'han de cridar expressament
        # per defecte json
        if f in ['xml', 'json', 'php']:
            self.format = f
        else:
            print('Format no permès. Triï entre: "xml", "json" o "php"')

    def setLang(self, l):
        "Configura l'idioma de la llengua de la petició"
        if l in ['ca', 'es', 'en']:
            self.lang = l
        else:
            print('Format no permès. Triï entre: "ca", "es" o "en"')
    
    def setCodificacio(self, c):
        "Configura la codificació de la resposta de la petició"
        if c in ['utf-8', 'iso-8859-1']:
            self.codificacio = c
        else:
            print('Format no permès. Triï entre: "utf-8" o "iso-8859-1"')
            
    def getServei(self):
        # aquesta funció necessita ser sobreescrita per funcionar
        pass

    def getOperacio(self):
        # ídem
        pass

    def getLang(self):
        "Retorna la llengua especificada"
        return self.PARAM_LANG + self.lang

    def getCodificacio(self):
        "Retorna la codificacio especificada"
        return self.PARAM_CODIFICACIO + self.codificacio
            
    def getUrlBase(self):
        "Retorna una llista amb tot l'url de la petició"
        self.url = []
        self.url.append(self.REQ)
        self.url.append(self.getServei())
        self.url.append('/')
        self.url.append(self.versio)
        self.url.append('/')
        self.url.append(self.getOperacio())
        self.url.append('.')
        self.url.append(self.format)

        # paràmetres generals

        self.url.append(self.getLang())
        self.url.append(self.getCodificacio())

        # les funcions getOperacio() i getServei() en una classe filla
        # s'han de sobreesciure en una classe filla
        # Rretorna una llista perquè és més fàcil treballar-hi en les classes filles
        return self.url
