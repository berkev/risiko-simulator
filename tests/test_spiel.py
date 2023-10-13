import unittest
import spielfeld
import player
import karte
import spiel


class TestSpielMethoden(unittest.TestCase):
    """Testet alle Methoden mit Rückgabewerten"""
    def setUp(self):
        gebietsGrenzen = [(0,1),(0,2),(0,4),(0,7),(0,8),(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,5),(5,6),(6,7),(7,8)]
        gebietsNamen = ["Blork","Zungo","Schlob","Kahfi","Zuln","Mago","Brait","Copri","Formi"]
        regionsNamen = ["Kupferhöhen","Ostwall","Sturmkap"]
        gebietZuRegion = [0,1,0,1,0,1,2,2,2]
        regionsBoni = [2,2,1]
        testfeld = spielfeld.spielfeld( gebietsGrenzen,gebietsNamen,regionsNamen,regionsBoni,gebietZuRegion,[],[0,7,8])
        karten = [karte.karte(gebietsNamen[i],i%3) for i in range(9)] 
        spieler = [player.KIplayer("Kurt","",5),player.KIplayer("Bernd","",1),player.KIplayer("Abel","",3)]
        self.Spiel = spiel.spiel(spieler,testfeld,karten,False)

    def tearDown(self):
        karte.karte("","").karten_reset()
        

    def test_spiel_verstärken(self):
        #9 Gebiete auf 3 Spieler verteilt

        self.assertTrue(len(self.Spiel.gebieteVon[0]) == 3, f"Spieler hat {len(self.Spiel.gebieteVon[0])} statt 3 Gebiete")

        self.Spiel.besatzung = [0,0,0,1,1,1,2,2,2]
        self.Spiel.gebieteVon[0] = [0,1,2]
        self.Spiel.gebieteVon[1] = [3,4,5]
        self.Spiel.gebieteVon[2] = [6,7,8]

        self.Spiel.set_zustand(truppen=3)

        self.assertTrue(self.Spiel.get_zustand("truppen")==3)
        self.assertTrue(self.Spiel.truppenZahl==[3,3,3,3,3,3,3,3,3])
        
        #teste falsche Eingaben:
        #versuche zu viele Truppen zu verteilen
        argument1 = [0,1,1,2,2,3]
        self.Spiel.verstärken(0,*argument1)
        self.assertTrue(self.Spiel.truppenZahl[0]==4, f"{self.Spiel.truppenZahl[0]} ist nicht 4")
        self.assertTrue(self.Spiel.truppenZahl[1]==5)
        self.assertTrue(self.Spiel.truppenZahl[2]==3)
        self.assertEqual(0,self.Spiel.get_zustand("truppen"))

        self.assertTrue(self.Spiel.truppenZahl==[4,5,3,3,3,3,3,3,3], f"{self.Spiel.truppenZahl} muss [4,5,3,3,3,3,3,3,3] sein")
        self.Spiel.set_zustand(truppen=3)

        #Falsches Gebiet erhöhen wollen
        argument2 = [0,3]
        argument3 = [7,2]
        self.Spiel.verstärken(1,*argument2)
        self.assertEqual(3,self.Spiel.get_zustand("truppen"), "Spieler 1 darf nicht das Gebiet von Spieler 0 verstärken")
        self.assertTrue(self.Spiel.truppenZahl==[4,5,3,3,3,3,3,3,3])
        self.Spiel.verstärken(1,*argument3)
        self.assertEqual(3,self.Spiel.get_zustand("truppen"), "Spieler 1 darf nicht das Gebiet von Spieler 2 verstärken")
        self.assertTrue(self.Spiel.truppenZahl==[4,5,3,3,3,3,3,3,3])
        
        self.Spiel.set_zustand(truppen=3)
        #Falsches Format abfangen:
        argument4 = [6, 1, 7, 1, 8]
        self.Spiel.verstärken(2,*argument4)
        self.assertEqual(1,self.Spiel.get_zustand("truppen") , "Bei ungeradem Input wurde das letzte Argument nicht ignoriert")
        self.assertTrue(self.Spiel.truppenZahl==[4,5,3,3,3,3,4,4,3])

        self.Spiel.set_zustand(truppen=3)
        #Fremdes Gebiet unter Argument
        argument5 = [1,2,4,1,2,1]
        self.Spiel.verstärken(0,*argument5)
        self.assertEqual(1,self.Spiel.get_zustand("truppen"), "Funktion muss ab dem Fehler abgebrochen werden")
        self.assertTrue(self.Spiel.truppenZahl==[4,7,3,3,3,3,4,4,3])

        #korrekter input
        #verstärke das erste Gebiet des spielers um eins, das zweite um 2 das dritte um 3
        self.Spiel.set_zustand(truppen=8)
        argument6 = [0,1,1,2,2,3]
        argument7 = [0,2]
        self.Spiel.verstärken(0,*argument6)
        self.assertEqual(2,self.Spiel.get_zustand("truppen"), "Zwei Truppen müssen übrig bleiben")
        self.assertTrue(self.Spiel.truppenZahl==[5,9,6,3,3,3,4,4,3])
        #Rest verteilen
        self.Spiel.verstärken(0,*argument7)
        self.assertEqual(0,self.Spiel.get_zustand("truppen"), "Keine Truppen dürfen übrig bleiben")
        self.assertTrue(self.Spiel.truppenZahl==[7,9,6,3,3,3,4,4,3])
         
    def test_spiel_manneuver(self):

        self.assertTrue(len(self.Spiel.gebieteVon[0]) == 3, f"Spieler hat {len(self.Spiel.gebieteVon[0])} statt 3 Gebiete")

        self.Spiel.besatzung = [0,1,0,0,1,2,2,1,2]
        self.Spiel.gebieteVon[0] = [0,2,3]
        self.Spiel.gebieteVon[1] = [1,4,7]
        self.Spiel.gebieteVon[2] = [6,5,8]

        self.assertTrue(self.Spiel.truppenZahl==[3,3,3,3,3,3,3,3,3])

        #Falsche Eingaben
        #Ungültige Anzahl beim Mannöver 
        self.Spiel.manneuver(0,0,3,-3)
        self.assertTrue(self.Spiel.truppenZahl==[3,3,3,3,3,3,3,3,3])
        #Start oder Ziel liegt in feindlicher Hand
        self.Spiel.manneuver(0,1,3,2)
        self.assertTrue(self.Spiel.truppenZahl==[3,3,3,3,3,3,3,3,3])
        self.Spiel.manneuver(0,2,5,1)
        self.assertTrue(self.Spiel.truppenZahl==[3,3,3,3,3,3,3,3,3])
        #manneuver zwischen nicht erreichbaren orten ablehnen
        self.Spiel.manneuver(1,4,7,1)
        self.assertTrue(self.Spiel.truppenZahl==[3,3,3,3,3,3,3,3,3])
        #abrunden von zu großen inputs
        self.Spiel.manneuver(0,0,3,8)
        self.assertTrue(self.Spiel.truppenZahl==[1,3,3,5,3,3,3,3,3])

    def test_get_aktion(self):

        self.assertTrue(len(self.Spiel.gebieteVon[0]) == 3, f"Spieler hat {len(self.Spiel.gebieteVon[0])} statt 3 Gebiete")

        self.Spiel.besatzung = [0,1,0,0,1,2,2,1,2]
        self.Spiel.gebieteVon[0] = [0,2,3]
        self.Spiel.gebieteVon[1] = [1,4,7]
        self.Spiel.gebieteVon[2] = [6,5,8]

        self.Spiel.set_zustand(truppen=3)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('v' in commands, "'v' wird nicht angezeigt obwohl Truppen zu verteilen sind")
        self.assertFalse('z' in commands, "'z' und 'v' dürfen nie gleichzeitig sichtbar sein")
        self.assertFalse('a' in commands, "'a' und 'v' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('m' in commands, "'m' und 'v' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('e' in commands, "'e' und 'v' dürfen nie gleichzeitig Optionen sein")

        self.Spiel.set_zustand(mussKartenSetzen = True)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]

        self.assertTrue('k' in commands, "'k' wird nicht angezeigt obwohl Karten zu wählen sind")
        self.assertFalse('z' in commands, "'z' und 'k' dürfen nie gleichzeitig sichtbar sein")
        self.assertFalse('a' in commands, "'a' und 'k' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('m' in commands, "'m' und 'k' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('e' in commands, "'e' und 'k' dürfen nie gleichzeitig Optionen sein")

        self.Spiel.set_zustand(mussKartenSetzen = False, kannKartenSetzen = True)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('k' in commands, "'k' wird nicht angezeigt obwohl Karten wählen möglich ist")
        self.assertFalse('z' in commands, "'z' und 'k' dürfen nie gleichzeitig sichtbar sein")
        self.assertFalse('a' in commands, "'a' und 'k' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('m' in commands, "'m' und 'k' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('e' in commands, "'e' und 'k' dürfen nie gleichzeitig Optionen sein")
        
        
        self.Spiel.set_zustand(truppen=0,angreifer=[],angriffsZiele=[])
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('z' not in commands, "'z' als Option verfügbar obwohl keine Angreifer oder Ziele gefunden wurden")


        self.Spiel.set_zustand(truppen=0,angreifer=[3,4],angriffsZiele=[[1],[2,3,4]])
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertFalse('a' in commands, "'a' als Option verfügbar obwohl kein Ziel gewählt wurde")

        self.Spiel.set_zustand(wahlAng=3,trAng=3,ziel=1,trZiel=3)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('a' in commands, "'a' nicht verfügbar obwohl der Zustand es zulässt")
        self.assertFalse('i' in commands, "'i' darf keine Option sein, wenn trZiel>0")
        self.assertTrue('z' in commands, "'z' nicht verfügbar obwohl mehrere Ziele existieren")
        self.assertFalse('v' in commands, "während der Angriffsphase dürfen keine Truppen mehr verteilt werden")
        self.assertFalse('k' in commands, "während der Angriffsphase dürfen keine Karten mehr gelegt werden wenn kein Zwang besteht")
        
        self.Spiel.set_zustand(angreifer=[3],angriffsZiele=[[1]])
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertFalse('z' in commands, "'z' als Option verfügbar obwohl nur ein Ziel existiert")

        self.Spiel.set_zustand(trAng=1)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('a' not in commands, "'a' verfügbar obwohl der Zustand es nicht zulässt")

        self.Spiel.set_zustand(trAng=4,trZiel=0)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('i' in commands, "'i' ist keine Option, muss es aber sein")
        self.assertFalse('z' in commands, "'z' darf erst nach der Invasion wieder Option sein")
        self.assertFalse('a' in commands, "'a' darf keine Option sein, Ziel hat keine Truppen")

        self.Spiel.set_zustand(mussKartenSetzen=True)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('i' in commands, "'i' ist keine Option, muss es aber sein")

        self.Spiel.set_zustand(wahlAng=-1,trAng=3,ziel=-1,trZiel=0)
        commandsLong = self.Spiel.get_aktionen()[1]
        commands = [com[0] for com in commandsLong]
        self.assertTrue('k' in commands, "'k' ist keine Option, muss es aber sein")
        self.assertFalse('z' in commands, "'z' und 'k' dürfen nie gleichzeitig sichtbar sein")
        self.assertFalse('a' in commands, "'a' und 'k' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('m' in commands, "'m' und 'k' dürfen nie gleichzeitig Optionen sein")
        self.assertFalse('e' in commands, "'e' und 'k' dürfen nie gleichzeitig Optionen sein")
        

    def test_berechne_regionsboni(self):

        self.Spiel.besatzung = [0,1,0,0,1,2,2,1,2]

        bonus0 = self.Spiel.berechne_regionsboni(0)
        bonus1 = self.Spiel.berechne_regionsboni(1)
        bonus2 = self.Spiel.berechne_regionsboni(2)

        self.assertEqual(0,bonus0+bonus1+bonus2, "Jemand erhält Bonus ohne eine volle Region zu besitzen")

        self.Spiel.besatzung = [0,1,0,0,0,2,2,1,2]
        bonus4 = self.Spiel.berechne_regionsboni(0)
        self.assertEqual(bonus4, self.Spiel.map.regionBonus[self.Spiel.map.gebZuReg[0]], f"Spieler bekommt {bonus4}, aber {self.Spiel.map.regionBonus[self.Spiel.map.gebZuReg[0]]} erwartet")

        self.Spiel.besatzung = [1,1,1,1,1,1,1,1,0]
        bonus5 = self.Spiel.berechne_regionsboni(1)
        self.assertEqual(bonus5,4, f"Spieler bekommt {bonus5}, aber 4 erwartet")

        self.Spiel.besatzung = [2,1,2,1,2,1,2,2,2]
        bonus6 = self.Spiel.berechne_regionsboni(2)
        self.assertEqual(bonus6,3, f"Spieler bekommt {bonus6}, aber 3 erwartet")


    def test_pruefe_boni(self):

        MAXHANDKARTEN = 5
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==False, "'mussKartenSetzen' wurde noch nicht überprüft")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==False, "'kannKartenSetzen' wurde noch nicht überprüft")

        
        self.assertTrue(len(self.Spiel.hand[0])==0, "Spieler 0 hat noch keine Karten bekommen")
        self.Spiel.hand[0].append(karte.karte("",1))
        self.Spiel.hand[0].append(karte.karte("",1))

        self.Spiel.pruefe_boni(0)
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==False, "Zu wenig Karten für diese flag")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==False, "Bei zwei Karten wird keine flag gesetzt")

        self.Spiel.hand[0].append(karte.karte("",2))
        self.Spiel.pruefe_boni(0)
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==False, "Zu wenig Karten für diese flag")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==False, "Kombination der Karten gewährt keine Boni")

        self.Spiel.hand[0].append(karte.karte("",3))
        self.Spiel.pruefe_boni(0)
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==False, "Zu wenig Karten für diese flag")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==True, "Kombination der Karten gewährt Bonus aber flag wurde nicht gesetzt")

        self.Spiel.hand[0].append(karte.karte("",3))
        self.Spiel.pruefe_boni(0)
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==True, "MAXHANDKARTEN auf der Hand aber flag wurde nicht gesetzt")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==True, "Kombination der Karten gewährt Bonus aber flag wurde nicht gesetzt")

        self.Spiel.hand[0].pop()
        self.Spiel.pruefe_boni(0)
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==False, "Zu wenig Karten für diese flag")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==True, "Kombination der Karten gewährt Bonus aber flag wurde nicht gesetzt")

        self.Spiel.hand[0].pop()
        self.Spiel.pruefe_boni(0)
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==False, "Zu wenig Karten für diese flag")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==False, "Kombination der Karten gewährt keine Boni")

    def test_checke_boni(self):
        
        DIREKTBONUS = 2
        self.assertTrue(self.Spiel.get_zustand("truppen")==0 , "Vor Spielerzug darf keine Truppe berechnet worden sein")
        spielerZwei = 1
        self.Spiel.hand[spielerZwei] = [karte.karte("",1),karte.karte("",1),karte.karte("",2),karte.karte("",1)]
        self.Spiel.pruefe_boni(spielerZwei)
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==1, "Spieler kann Karten setzen aber die Prüfung sieht das nicht")

        #Falsche Kombi probieren
        self.Spiel.checke_boni(spielerZwei,0,1,2)
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==1, "'kannKartenSetzen' darf erst auf False gesetzt werden, wenn keine Handkarten mehr eintauschbar sind")
        self.assertTrue(len(self.Spiel.hand[spielerZwei])==4, "Nur gültige Kombinationen dürfen aus der Hand entfernt werden")

        #zu wenig Karten ausweisen
        self.Spiel.checke_boni(spielerZwei,0,1)
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==1, "'kannKartenSetzen' darf erst auf False gesetzt werden, wenn keine Handkarten mehr eintauschbar sind")
        self.assertTrue(len(self.Spiel.hand[spielerZwei])==4, "Nur gültige Kombinationen dürfen aus der Hand entfernt werden")

        #zu viele Karten ausweisen
        self.Spiel.checke_boni(spielerZwei,0,1,2,3)
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==1, "'kannKartenSetzen' darf erst auf False gesetzt werden, wenn keine Handkarten mehr eintauschbar sind")
        self.assertTrue(len(self.Spiel.hand[spielerZwei])==4, "Nur gültige Kombinationen dürfen aus der Hand entfernt werden")

        #index out of range
        self.Spiel.checke_boni(spielerZwei,0,1,4)
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==1, "'kannKartenSetzen' darf erst auf False gesetzt werden, wenn keine Handkarten mehr eintauschbar sind")
        self.assertTrue(len(self.Spiel.hand[spielerZwei])==4, "Nur gültige Kombinationen dürfen aus der Hand entfernt werden")

        #richtige Kombo wird akzeptiert
        self.Spiel.checke_boni(spielerZwei,0,1,3)
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==0, "'kannKartenSetzen' darf nicht gesetzt sein, da zu wenig Karten auf der Hand sind.")
        self.assertTrue(len(self.Spiel.hand[spielerZwei])==1, "Die gültige Kartenkombi muss aus der Hand entfernt werden.")
        self.assertTrue(self.Spiel.get_zustand("truppen")==4, "Karten mit Symbol 1 müssen einen Bonus von 4 geben")

        self.Spiel.set_zustand(truppen=0)

        self.Spiel.hand[spielerZwei] = [karte.karte("",1),karte.karte("",1),karte.karte("",2),karte.karte("",2),karte.karte("",3),karte.karte("",3),karte.karte("",3),karte.karte("",3)]
        self.Spiel.checke_boni(spielerZwei,0,2,4)
        self.assertTrue(self.Spiel.get_zustand("mussKartenSetzen")==1, "'mussKartenSetzen' muss wegen der Anzahl an Karten auf der Hand gesetzt sein.")
        self.assertTrue(self.Spiel.get_zustand("kannKartenSetzen")==1, f"'kannKartenSetzen' muss gesetzt sein, da noch {len(self.Spiel.hand[spielerZwei])} Karten auf der Hand sind.")
        self.assertTrue(len(self.Spiel.hand[spielerZwei])==5, "Die gültige Kartenkombi muss aus der Hand entfernt werden.")
        self.assertTrue(self.Spiel.get_zustand("truppen")==7, "Karten mit Symbol 1,2,3 müssen einen Bonus von 7 geben")

        self.Spiel.set_zustand(truppen=0)
        #Direktboni prüfen
        karte.karte("",1).karten_reset()
        self.Spiel.hand[spielerZwei] = [karte.karte("",1),karte.karte("",2),karte.karte("",2),karte.karte("",2),karte.karte("",3),karte.karte("",3),karte.karte("",3),karte.karte("",3)]
        self.Spiel.besatzung[1] = spielerZwei
        self.Spiel.besatzung[2] = spielerZwei
        self.Spiel.besatzung[3] = 0
        self.Spiel.gebieteVon[spielerZwei]=[1,2]
        self.Spiel.gebieteVon[0] = [3]

        self.assertEqual(self.Spiel.truppenZahl[1],3, "Gebiet muss 3 Truppen haben")
        self.assertEqual(self.Spiel.truppenZahl[2],3, "Gebiet muss 3 Truppen haben")
        self.assertEqual(self.Spiel.truppenZahl[3],3, "Gebiet muss 3 Truppen haben")

        self.Spiel.checke_boni(spielerZwei,1,2,3)
        self.assertEqual(self.Spiel.truppenZahl[1],5, "Gebiet muss 5 Truppen haben")
        self.assertEqual(self.Spiel.truppenZahl[2],5, "Gebiet muss 5 Truppen haben")
        self.assertEqual(self.Spiel.truppenZahl[3],3, "Gebiet muss 3 Truppen haben")
        self.assertTrue(self.Spiel.get_zustand("truppen")==5, "Karten mit Symbol 2 müssen einen Bonus von 5 geben")

