import unittest
from onomastica import *

class OnomasticaTest(unittest.TestCase):
    def testOperacioNoPermesa(self):
        self.assertRaises(OperacioNoPermesa, Onomastica.setOperacio, self, 'asdf')
    
    def testSubNoPermes(self):
        self.assertRaises(SubserveiNoPermes, Onomastica.setSub, self, 'asdf')
    
    def testOperacioNoExisteix(self):
        pass
        
        
        
if __name__ == '__main__':
    unittest.main()
    
