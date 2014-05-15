from municipi_base import MunicipiBase, buscaId
import urllib.request as req

class Municipi(MunicipiBase):
    def __init__(self, op):
        super(Municipi, self).__init__()
        self.setOperacio(op)

    def get(self):
        url = ''.join(self.getUrlBase())
        sol = req.urlopen(url)
        self.data = sol.read().decode('utf-8')
        return self.data

def debug():
    c = Municipi('dades')
    c.addId(buscaId('Collbató'))
    c.addI('f271')
    c.get()
        
