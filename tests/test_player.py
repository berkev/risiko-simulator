from player import player
import unittest

#Gültigkeit der Eingaben wird durch Instanzen des Spiels überprüft
#Diese Tests fallen weg, da zu restriktiv 


class TestPlayerMethoden(unittest.TestCase):
    """Teste die deterministischen Entscheidungen des players"""

    def setUp(self) -> None:
        pass
    
    """ def test_berechne_risiko(self):
        ort=[]
        geb=[]
        nachb = []
        truppen = []
        besatz = []
        ergebnisse = []
        
        geb.append([0,8,7])
        nachb.append([[1,2,4,7,8],[0,7],[8,6]])
        truppen.append([3,1,1,5,1,3,7,1,9])
        besatz.append([0,1,1,1,1,1,1,0,0])
        ergebnisse.append([2,-9,8])

        geb.append([0,8,7])
        nachb.append([[1,2,4,7,8],[0,7],[8,6]])
        truppen.append([3,3,3,5,1,3,7,1,9])
        besatz.append([0,1,2,1,1,1,1,0,0])
        ergebnisse.append([8,-9,8])

        geb.append([0,8,7])
        nachb.append([[1,2,4,7,8],[0,7],[8,6]])
        truppen.append([3,3,3,5,1,3,7,1,9])
        besatz.append([0,1,2,1,1,1,1,0,0])
        ergebnisse.append([8,-9,8])
        
        for k in range(len(geb)):
            for i in range(len(ergebnisse[k])):
            
                self.assertEqual(player("","").berechne_risiko(geb[k][i],geb[k],nachb[k],truppen[k],besatz[k]),ergebnisse[k][i])

    
    def test_wähle_manneuver(self):

        zsh=[]
        geb=[]
        nachb = []
        truppen = []
        besatz = []
        ergebnisse = []

        geb.append([0,8,7])
        zsh.append([{0,8,7}])
        nachb.append([[1,2,4,7,8],[0,7],[8,6]])
        truppen.append([3,1,1,5,1,3,7,1,9])
        besatz.append([0,1,1,1,1,1,1,0,0])
        ergebnisse.append((8,7,8))
        
        geb.append([0,8,7])
        zsh.append([{0,8,7}])
        nachb.append([[1,2,4,7,8],[0,7],[8,6]])
        truppen.append([3,3,3,5,1,3,7,1,9])
        besatz.append([0,1,2,1,1,1,1,0,0])
        ergebnisse.append((8,0,8))
        
        
        for k in range(len(zsh)):

            
            self.assertEqual(player("","").wähle_manneuver(zsh[k],geb[k],nachb[k],truppen[k],besatz[k]),ergebnisse[k])
 """