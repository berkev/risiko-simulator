from spielfeld import spielfeld
import unittest
#from random import randrange,choices

class TestSpielfeldMethoden(unittest.TestCase):

    
    def setUp(self):
        grenzen = [(0,1),(0,2),(0,4),(0,7),(0,8),(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,5),(5,6),(6,7),(7,8)]
        self.feld = spielfeld(grenzen,[],[],[],[],[],[])
        
    def test_ist_erreichbar(self):

        for k in range(7):
            self.assertTrue(self.feld.ist_erreichbar(k,k+1,[i for i in range(8)]))
            self.assertTrue(self.feld.ist_erreichbar(k+1,k,[i for i in range(8)]))
            self.assertTrue(self.feld.ist_erreichbar(k,k,[k]))
            self.assertFalse(self.feld.ist_erreichbar(k+1,k,[]))
            self.assertFalse(self.feld.ist_erreichbar(k,k+1,[]))
        
        self.assertFalse(self.feld.ist_erreichbar(1,5,[1,5,2,0,7]))
        self.assertFalse(self.feld.ist_erreichbar(2,8,[2,3,4,8]))
        self.assertTrue(self.feld.ist_erreichbar(1,7,[1,7,0,8]))

        #Komponenten checken:
        self.assertEqual(self.feld.ist_erreichbar(1,-1,[1,6,5,0,8],True),{1,0,8})
        self.assertEqual(self.feld.ist_erreichbar(5,-1,[1,4,5,8],True),{5,4})
        self.assertEqual(self.feld.ist_erreichbar(4,-1,[4,3,1,6,7],True),{4,3,1})
        self.assertEqual(self.feld.ist_erreichbar(6,-1,[4,3,1,6,7],True),{6,7})

        #checken, ob die aufteilung der zusammenhangskomponenten komplett und 
        #korrekt ist
        spielerGebiete = set([8,0,3,5])
        zusammenhangsklassen = []

        while spielerGebiete:
            letzteKlasse = self.feld.ist_erreichbar(spielerGebiete.pop(),-1,spielerGebiete,True)
            zusammenhangsklassen.append(letzteKlasse)
            spielerGebiete -= letzteKlasse

        self.assertTrue(len(zusammenhangsklassen)==2, f"{len(zusammenhangsklassen)} Klassen zusammengehöriger Gebiete gefunden, müssen aber 2 sein.")
        self.assertTrue({3,5} in zusammenhangsklassen, " Klasse {3,5} wurde nicht erkannt")
        self.assertTrue({8,0} in zusammenhangsklassen, " Klasse {0,8} wurde nicht erkannt")