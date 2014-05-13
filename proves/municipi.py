from municipi_base import MunicipiBase, buscaId
import urllib.request as req

class Municipi(MunicipiBase):
    def __init__(self, op):
        super(Municipi, self).__init__()
        self.setOperacio(op)

    def get(self):
        url = self.getUrlBase()
        sol = req.urlopen(self.url)
        self.data = sol.read().decode('utf-8')
        
