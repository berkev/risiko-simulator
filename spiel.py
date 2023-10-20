import random
#from karte import karte
import karte
from player import player,KIplayer,HumanPlayer
from spielfeld import spielfeld
from spielconfig import *
import time
import numpy as np
import datetime
import csv
import os
"""
Hauptklasse des Projektes die alle nötigen Datenstrukturen für eine
Spielausführung bereithält.

Karten, Spieler und das Spielfeld sind Teil des Spiels und werden beim init übergeben.

Da es interessant ist, welche Angriffe und Eroberungen, aber auch welche 
Truppenbewegungen und Truppenverteilungen stattfanden, soll eine Funktion
dieser Klasse sein, alle Ergebnisse in einem geeigneten Datenformat abzuspeichern.

Gefechte werden durch eine eigene Funktion simuliert, wobei als Eingabe 
 die kämpfenden Gebiete eingesetzt werden.

Ein Spielzug bezeichnet alle von einem Spieler getätigten Handlungen. 

1. Er beginnt mit dem Erhalt neuer Truppen abhängig von der Anzahl aktiver Truppen und optionaler Regions-Boni. 
Diese darf ein Spieler frei auf seinen im Besitz befindlichen Gebieten verteilen. Dannach kann ein Spieler, 
sofern seine durch Eroberungen erhaltenen Karten die richtige Kombination an Symbolen enthalten, 
Zusatztruppen durch Eintauschen der Karten ebenso verteilen. Je Karte, die ein Gebiet des Spielers zeigt,
darf der Spieler 2 Truppen auf diese Gebiete stellen. Hat der Spieler 5 Karten, muss er 3 davon einlösen.
Es kann auch passieren, dass der Spieler mehr Truppen verteilen dürfte,
als er besitzt. In diesem Fall verteilt der Spieler so viele Truppen wie er hat. 

2. In einem Spielzug können keine, ein oder mehrere Gefechte stattfinden. 
Wird mindestens ein Gefecht gewonnen, erhält der Spieler eine zufällige Karte vom Stapel. Wird ein Gefecht gewonnen,
marschieren mindestens die am Kampf beteiligten Truppen in das eroberte Gebiet ein oder weitere Truppen aus dem 
Aggressorgebiet. Ein Gefecht kann auch jederzeit abgebrochen werden.

2b. Wird ein Spieler durch eine Eroberung eliminiert (das heißt er verlor sein letztes Gebiet),
 erhält der Angreifer alle seine Gebietskarten. Falls dadurch mehr als
5 Karten in der Hand des aktiven Spielers sind, darf er diese ungehend gegen neue Einheiten eintauschen.

3. Möchte der Spieler keine weiteren Gefechte führen, darf er noch ein Mannöver durchführen. Dabei darf eine beliebige Menge
an Truppen eines kontrollierten Gebietes in ein verbundenes Gebiet bewegt werden. Dabei darf aber nie ein Gebiet leer sein.
Gebiete sind verbunden, wenn es einen Pfad kontrollierter Gebiete zwischen den beiden gibt.

"""



class spiel:
    """Ein Spiel kann als Zustandsapparat verstanden werden.
        Der Initialzustand ist definiert durch:
    player[] spielerliste   : Eine Liste aus 3-5 Spielern
    spielfeld map           : Ein Spielfeldobjekt
    karte[] stapel          : Sammlung der Spielkarten
    int[] besatzung         : Liste über alle Gebiete mit Index des Spielers, der dieses kontrolliert
    int[] truppenZahl       : Anzahl der Truppen, die auf einem Gebiet stehen
    list of karte[] hand    : Handkarten der Spieler, zu Beginn leer
    int[] aktiveSpieler     : Liste der Spielerindizes, die noch im Spiel sind
    int spielerAmZug        : Erster Spieler
    int[[]] gebieteVon      : Liste pro Spieler mit seinen Gebieten
    bool log                : True wenn die Konsole das Spielgeschehen vollkommen ausgeben soll
    bool savegame           : True wenn die Historie des Spiels gespeichert werden soll
    Zusätzlich zum allgemeine Zustand der Daten soll das Spiel auch den Zustand 
    """
    def __init__(self, spielerliste: list[player], map: spielfeld, stapel: list[karte.karte], log=True, savegame=False) -> None:
        
        self.spielerliste = spielerliste
        self.map = map
        self.stapel = stapel
        self.log = log
        self.besatzung = [-1 for k in map.gebiete]
        self.truppenZahl = [3 for k in map.gebiete]
        self.hand = [[] for s in spielerliste]
        self.aktiveSpieler = [i for i in range(len(spielerliste))]
        self.gebieteVon = [[] for i in range(len(spielerliste))]
        # [[[1v1][1v2]] [[2v1][2v2]] [[3v1][3v2]]] [w(,l)]
        # Wo nur eine Zahl: drunter: gewonnen, drüber verloren#
        # wo zwei zahlen: unter erster zahl: gewonnen, über 1-zweite: verloren sonst: draw
        # Weitere Infos zu diesen Wahrscheinlichkeiten und ihrer Herleitung in der README verlinkt
        self.probs = [[[5/12],[55/216]],[[125/216],[295/1296,581/1296]],[[95/144],[1445/3888,2275/7776]]]
        self.kommandoHilfe = {"v": " v <Gebietsnummer> <Anzahl> [<Gebietsnummer> <Anzahl>]* \n Füge Gebiet <Gebietsnummer> <Anzahl> Truppen hinzu. Weitere Paare durch Leertaste trennen.",
                              "k": " k <KartenNr1> <KartenNr2> <KartenNr3> \n Tausche die angegebenen Karten für Truppen ein.",
                              "z": " z <Zielnummer> <Angreifernummer> [1/2/3]\n Beginnt den Angriff von <Angreifernummer> auf >Zielnummer> mit der angegebenen Anzahl an Truppen. Wird das letzte Argument weggelassen, benutzt maximal mögliche Anzahl.",
                              "a": " a [1/2/3]\n Greife das aktuelle Ziel weiter an. Optional kann gewählt werden, wie viele Truppen angreifen.",
                              "e": " e \n Beendet den aktuellen Zug",
                              "m": " m <Startnummer> <Zielnummer> <Anzahl> \n Führt ein Mannöver von <Anzahl> Truppen durch von Gebiet <Startnummer> nach Gebiet <Zielnummer> durch.",
                              "x": " x \n Höre auf zu spielen. Ein Bot springt ein und beendet das Spiel.",
                              "i": " i [Anzahl] \n Führt Invasion mit Anzahl Truppen durch. Wird das Argument weggelassen ziehen nur die im Gefecht beteiligten Truppen ein.",
                              "h": " h <Kommando> \n Zeigt die Beschreibung des Kommandos <Kommando> an.",
                              "s": " s [m/a] [a/m]\n Zeigt den Status des aktuellen Spielers an. Die Optionen m oder a zeigen jeweils, welche Mannöver möglich sind und welche Angriffe möglich sind"
                              }
        self.zustand = {"truppen": 0,
                        "kannKartenSetzen": 0,
                        "mussKartenSetzen": 0,
                        "angreifer": [],
                        "angriffsZiele": [],
                        "ziel": -1,
                        "trZiel": 0,
                        "wahlAng": -1,
                        "trAng": 0,
                        "erhKarte": False,
                        "man": False,
                        "validGeb": [],
                        "validKlassen": []}
        self.sg = savegame

        random.shuffle(stapel)
        self.spielerAmZug = random.randrange(0,len(spielerliste))
        self.konsolen_Log(f"Erster Spieler ist {self.spielerliste[self.spielerAmZug].name}\n")
        i = (self.spielerAmZug - 1 + len(spielerliste)) % len(spielerliste)
        for k in stapel:
            
            self.besatzung[k.id] = i
            self.gebieteVon[i].append(k.id)
            #print(f"Karte {k.id} geht an {self.spielerliste[i].name}")
            i = (i - 1 + len(spielerliste)) % len(spielerliste)
        
        random.shuffle(stapel)
        stopKartePos = random.randrange(len(stapel)//2,len(stapel)-1)
        
        stopKarte = karte.karte("Spielende", None)
        stapel.append(stapel[stopKartePos])
        stapel[stopKartePos] = stopKarte
        self.stapel.reverse()
        self.zeige_start(list(range(len(self.spielerliste))))
        self.runde = 0
        self.ende = False
    
    def set_zustand(self,**kwargs):
        """Interface für das Überschreiben von Einträgen im Attribut 'zustand'.
        Eine Liste von Schlüssel-Wert-Paaren überschreibt das Dictionary self.zustand. """
        for key,value in kwargs.items():
            self.zustand[key]=value
        
    def get_zustand(self,attr):
        """Interface für das Lesen eines Attributwertes des Dictionaries 'zustand'.
        str attr  -> Any|None"""
        try:
            return self.zustand[attr]
        except:
            self.konsolen_Log(f"{attr} ist nicht Teil des Zustands")

    def hilfe(self,spielerPos,*kommando):
        """Nimmt eine Liste von Kommando-Kürzeln und gibt eine Beschreibung
        auf dem STDOUT zurück."""
        try:
            if not kommando:
                self.konsolen_Log(self.kommandoHilfe['h'])
            for kom in kommando:
                self.konsolen_Log(self.kommandoHilfe[kom])
        except:
            self.konsolen_Log(self.kommandoHilfe['h']+"\n")
            self.konsolen_Log('\n'.join(["Kommandos:"]+['\t '+kommando for kommando in self.kommandoHilfe.keys()]))
        self.konsolen_Log("\n\n")
        return 0
    
    def zeige_status(self,spielerPos,*args):
        """Gibt alle (i,self.truppenZahl[i]) aus für die gilt: self.besatzung[i]=spielerPos .
        Informationen über mögliche Argumente für die Kommandos z arg1 arg2 und 
        m arg1 arg2 arg3 werden ausgegeben, wenn args a oder m enthält."""

        if self.get_zustand('truppen'):
            self.konsolen_Log(f"{self.get_zustand('truppen')} Truppen zu verteilen\n")
        else:
            if 'a' in list(args):
                self.konsolen_Log("Mögliche Angriffe")
                for i in range(len(self.get_zustand("angreifer"))):
                    self.konsolen_Log(f'{self.get_zustand("angreifer")[i]} kann {self.get_zustand("angriffsZiele")[i]} angreifen\n')
            if 'm' in list(args):
                self.konsolen_Log("Mögliche Mannöver\n")
                for i in range(len(self.get_zustand("validGeb"))):
                    self.konsolen_Log(f'{self.get_zustand("validGeb")[i]}--max {self.truppenZahl[self.get_zustand("validGeb")[i]]-1}-->{[y for y in self.get_zustand("validKlassen")[i] if y != self.get_zustand("validGeb")[i]]}\n')
        self.zeige_start([spielerPos])

        return 0
    
    def get_aktionen(self):
        """berechnet vom Zustand ausgehend, welche Aktionen der aktuelle Spieler durchführen kann"""

        aktionen = []
        kommandoStrings = []
        
        #verstärken
        #wenn Truppen>0
        truppen = self.get_zustand("truppen")
        n = 'n' if truppen>1 else ''
        if truppen:
            aktionen.append(self.verstärken)
            kommandoStrings.append("v (verstärken) "+'noch '+str(truppen)+' Truppe'+n)
        #karten setzen
        #bevor erster Angriff
        #oder wenn nach Auslöschung eines mitspielers zu viele Karten auf der Hand sind
        if (self.get_zustand("kannKartenSetzen") and self.get_zustand("wahlAng") == -1 and not(self.get_zustand("angreifer") or self.get_zustand("validKlassen"))) or self.get_zustand("mussKartenSetzen") and self.get_zustand("wahlAng") == -1 and not self.get_zustand("man"):
            aktionen.append(self.checke_boni)
            kommandoStrings.append("k (karten setzen)")
        #angreifen
        #es dürfen keine Truppen mehr auf reserve sein und kein kartenzwang
        #ausserdem muss es angreifbare Truppen geben
        #und ziel, falls gewählt, müssen positive zahl an Truppen haben
        bedA = not (self.get_zustand("truppen") or self.get_zustand("mussKartenSetzen")) and self.get_zustand("angriffsZiele") and not self.get_zustand("man")
        #angreifen 1/2 ziel wählen
        #entweder es wurde noch kein Ziel gewählt
        #oder das Ziel wird während eines Gefechts gewechselt
        if bedA and (self.get_zustand("ziel")==-1 or (self.get_zustand("trZiel")>0 and (len(self.get_zustand("angriffsZiele"))>1 or len(self.get_zustand("angreifer"))>1))):
            aktionen.append(self.spieler_gefecht)
            kommandoText = "z (ziel wählen)" if self.get_zustand("ziel")==-1 else "z (ziel wechseln)"
            kommandoStrings.append(kommandoText)
        #angreifen 2/2 weiter angreifen
        #falls bereits ein ziel gewählt wurde und alle angriffsbedingungen bedA erfüllt sind
        if bedA and self.get_zustand("ziel")!=-1 and self.get_zustand("trZiel")!=0 and self.get_zustand("trAng") > 1:
            aktionen.append(self.gefecht)
            kommandoStrings.append("a (weiter angreifen)")
        #mitziehen
        #wenn bedingungen für angriff erfüllt sind aber truppenzahl des gewählten feindes auf 0
        #gesunken ist
        #wird diese aktion nicht gewählt, dann ziehen nur die Truppen ein, die am Angriff beteiligt waren
        bedI = self.get_zustand("trZiel")==0 and self.get_zustand("ziel")!=-1
        if not self.get_zustand("truppen") and bedI:
            aktionen.append(self.spieler_mitziehen)
            kommandoStrings.append("i (invasion)")


        #manneuver
        #ein manneuver ist nach dem verstärken immer möglich, sofern es zusammenhängende Gebiete gibt die es erlauben
        #das manneuver beendet den Zug, wenn eines durchführbar ist
        if not (self.get_zustand("truppen") or self.get_zustand("mussKartenSetzen") or self.get_zustand("man") or bedI) and self.get_zustand("validGeb"):
            aktionen.append(self.manneuver)
            kommandoStrings.append("m (mannöver)")

        #Runde aufhören
        #nach verstärkung und karten setzen möglich
        if not (self.get_zustand("truppen") or self.get_zustand("mussKartenSetzen")):
            aktionen.append(self.zug_beenden)
            kommandoStrings.append("e (Zug beenden)")

        #spiel verlassen immer möglich
        aktionen.append(self.verlasse_spiel)
        kommandoStrings.append("x (verlasse Spiel)")

        aktionen.append(self.hilfe)
        kommandoStrings.append("h (Hilfe)")

        aktionen.append(self.zeige_status)
        kommandoStrings.append("s (status)")
        return aktionen, kommandoStrings
    
    
    
    def zug_starten(self):
        """der zustand wird neu berechnet für den Spieler, der am Zug ist."""
        self.set_zustand(truppen = 0,
                        kannKartenSetzen = 0,
                        mussKartenSetzen = 0,
                        angreifer = [],
                        angriffsZiele =  [],
                        ziel = -1,
                        trZiel = 0,
                        wahlAng = -1,
                        trAng = 0,
                        erhKarte = False,
                        man = False,
                        validGeb = [],
                        validKlassen = [])
        self.set_zustand(truppen = STANDARDBONUS(len(self.gebieteVon[self.spielerAmZug]))+self.berechne_regionsboni(self.spielerAmZug))
        self.pruefe_boni(self.spielerAmZug)
        self.setze_angreifer_und_manneuver(self.spielerAmZug)
        
        self.konsolen_Log(f"{self.spielerliste[self.spielerAmZug].name} ist am Zug.\n")
        # if self.spielerzug(self.spielerAmZug):
        #     self.spiel_ende()
        
        

    def zug_beenden(self,*args):
        """Ruft abhängig vom zustand die 'ziehe_karte'-Methode auf und
        inkrementiert die Attribute spielerAmZug und runde.
        Im Fall, dass die Endekarte gezogen wurde wird die spiel_ende-Methode aufgerufen."""
        if self.get_zustand("erhKarte"):
            self.konsolen_Log(f"{self.spielerliste[self.spielerAmZug].name} erhält eine Karte.\n")
            karte = self.ziehe_karte(self.spielerAmZug)
            self.set_zustand(erhKarte=False)
            if not karte.bonus:
                self.konsolen_Log(f"\n=============={karte.name} wurde gezogen==============\n")
                self.spiel_ende()
                return 1
        self.spielerAmZug = self.aktiveSpieler[(self.aktiveSpieler.index(self.spielerAmZug)+1)%len(self.aktiveSpieler)]
        self.runde += 1
        self.konsolen_Log(f"\n Zwischenstand nach Runde {self.runde}:\n")
        self.zeige_start(self.aktiveSpieler)
        return 1

    def setze_angreifer_und_manneuver(self,spielerPos):
        """Berechnet Attribute des zustands, die sich im Verlauf eines Zuges ändern können neu."""
        angreifer,zieleVonAngreifer = self.suche_ziele(spielerPos)
        self.set_zustand(angreifer=angreifer, angriffsZiele=zieleVonAngreifer)
        valideGebiete, valideZieleJeGebiet = self.suche_mannöver(spielerPos)
        self.set_zustand(validGeb=valideGebiete, validKlassen=valideZieleJeGebiet)

    

    
    def pruefe_boni(self, spielerPos):
        """Überschreibt zustands-Attribute, die das Nutzen von Karten betreffen.
            """
        bonusLvl = []
        LvlAnzahl = [0,0,0]
        hand = self.hand[spielerPos]
        if len(hand)>2:
            for karte in hand:
                #Für jeden Bonustypen auf der Hand lege Zähler an
                if karte.bonus not in bonusLvl:
                    bonusLvl.append(karte.bonus)
                LvlAnzahl[bonusLvl.index(karte.bonus)] += 1
            if LvlAnzahl[0]*LvlAnzahl[1]*LvlAnzahl[2] != 0 or max(LvlAnzahl) > 2:
                self.set_zustand(kannKartenSetzen=True)
            else:
                self.set_zustand(kannKartenSetzen=False)
            if len(hand)>= HANDKARTENMAX:
                self.set_zustand(mussKartenSetzen = True)
            else:
                self.set_zustand(mussKartenSetzen = False)
        else:
            self.set_zustand(kannKartenSetzen=False)
            self.set_zustand(mussKartenSetzen = False)

    def berechne_regionsboni(self,spielerPos):
        """Prüft die Gebiete des Spielers spielerPos darauf, ob sie volle Regionen
        enthalten. Im Spiel Risiko erhält ein Spieler in dem Fall zu Beginn seines Zuges Bonustruppen,
        deren Anzahl abhängig von der Region ist.
        
        Summe über die Anzahl der Regionen
        Vergleicht das skalarprodukt aus dem zugehörigkeitsvektor gebiet spieler
        und dem zugehörigkeitsvektor gebiet region mit der anzahl an der gebiete pro region."""
        bonus = 0
        spielerBesitzt = [int(spielerPos==self.besatzung[l]) for l in range(len(self.besatzung))]
        for k in range(len(self.map.regionBonus)):
            bon = self.map.regionBonus[k] * (np.dot(spielerBesitzt,[int(k==i) for i in self.map.gebZuReg]) == sum([int(k==i) for i in self.map.gebZuReg]) )
            if bon:
                self.konsolen_Log(f"Du besitzt alle Gebiete der Region {self.map.region[k]}. Erhalte {bon} weitere Truppe{'n' if bon>1 else ''}.\n")
            bonus+=bon
        return bonus
    

    def checke_boni(self, spielerPos, *karten):
        """Liest eine Liste von Indizes 'karten' und prüft, ob die Kartenobjekte
        [self.hand[spielerPos][k] for k in karten] eine gültige Kombination im Sinne
        des Spieles ergeben. Im positiven Fall wird der zustand verändert: Truppen werden
         hinzugefügt, Karten werden erneut auf Zwang oder Möglichkeit zum Eintauschen über-
        prüft. """
        
        spieler = self.spielerliste[spielerPos]
        try:
            karten = [self.hand[spielerPos][i] for i in karten]
        except IndexError:
            self.konsolen_Log("Die angegebenen Karten enthalten Nummern die zu keiner Handkarte gehören")
            return 0
        bonus = 0
        
        bonBon = len(set([karte.bonus for karte in karten] ))
        if len(karten)==3 and (bonBon == 1 or bonBon == 3 ) and karten[0].id != karten[1].id:
            self.konsolen_Log(f"{spieler.name} tauscht {[(karte.id,karte.bonus) for karte in karten]} ein.\n")
            bonus += KARTENBONUS + bonBon + max([karte.bonus for karte in karten]) - 1 * (bonBon-1)//2
            self.konsolen_Log(f"{spieler.name} hat weitere {bonus} Truppen durch eintauschen von Karten erhalten\n")
            self.set_zustand(truppen=self.get_zustand("truppen")+bonus)

            self.set_zustand
            while karten:
                idCheck = karten.pop()
                self.entferne_karte(spielerPos, idCheck)
                if idCheck.id in self.gebieteVon[spielerPos]:
                    self.mache_truppen(idCheck.id,2)
                    self.konsolen_Log(f"{self.map.gebiete[idCheck.id]} erhält wegen einem Kartenbonus 2 Zusatztruppen!\n")
        else:
            if karten:
                self.konsolen_Log(f"Die Kombination der Boni ist{[karte.bonus for karte in karten]} : keine gültige Wahl zum Tauschen gegen Truppen")
            
        self.pruefe_boni(spielerPos)
        return 0

    def suche_ziele(self,spielerPos):
        """Listet angriffsbereite Gebiete in einer Liste auf. Die zweite Liste besteht aus
        den Mengen der möglichen Ziele je angriffsbereitem Gebiet."""
        starkeGebiete = [y for y in self.gebieteVon[spielerPos] if self.truppenZahl[y]>1]
        zieleVon = []
        starkeGebieteMitGegnern = []
        for x in starkeGebiete:
            fremdeNachbarn = [y for y in self.map.gibNachbarn(x) if y not in self.gebieteVon[spielerPos] ]
            if fremdeNachbarn:
                zieleVon.append(fremdeNachbarn) 
                starkeGebieteMitGegnern.append(x)
        return starkeGebieteMitGegnern, zieleVon
    
    def suche_mannöver(self,spielerPos):
        """In dieser Funktion wird gesucht ob und welche Mannöver für den aktuellen Spieler
        möglich sind"""
        spielerGebiete = set(self.gebieteVon[spielerPos])
        if len(spielerGebiete)<2:
            #self.konsolen_Log(f"nicht genug Gebiete für Mannöver")
            return [],[]
        zusammenhangsklassen = []
        while spielerGebiete:
            letzteKlasse = self.map.ist_erreichbar(spielerGebiete.pop(),-1,self.gebieteVon[spielerPos],True)
            zusammenhangsklassen.append(letzteKlasse)
            spielerGebiete -= letzteKlasse
        
        
        validGebiete = []
        validKlassen = []
        for i in range(len(zusammenhangsklassen)):
            klasse = zusammenhangsklassen[i]
            if len(klasse)>1 and max([self.truppenZahl[gebiet] for gebiet in klasse])>1:
            #gültige Mannöver enthalten
                validGebiete+=list(klasse)
                #für jedes Gebiet aus Klasse lege die selbe Liste an mannövrierbare Gebieten in validKlassen an
                for geb in list(klasse):
                    validKlassen.append(list(klasse))
        return validGebiete, validKlassen

    def sende_zustand_karte(self,spielerPos):
        """Sende die Attribute Besatzung und TruppenZahl an den spielerPos.ten Spieler"""
        return {"besatzung":self.besatzung,"truppenZahl":self.truppenZahl}
    def logge_zustand_karte(self):
        try:
            with open(self.sg+"b"+".csv",'a') as file:
                writer = csv.writer(file,lineterminator="\n")
                writer.writerow(self.besatzung)
        except Exception as err:
            print(err)
            
        try:
            with open(self.sg+"t"+".csv",'a') as file:
                writer = csv.writer(file,lineterminator="\n")
                writer.writerow(self.truppenZahl)
        except Exception as err:
            print(err)
            
    def sende_kommandos(self):
        kommandos = self.get_aktionen()[1]
        return ".".join(kommandos)

    def lese_kommando(self,kommando):

        aktionen,kommandos = self.get_aktionen()
        try:
            self.konsolen_Log(f"Eingabe:\t{kommando}")
            wahlFunktion = aktionen[[k[0] for k in kommandos].index(kommando[0])]
        except:
            self.konsolen_Log(f"'{kommando}' ist kein gültiges Kommando. Benutze 'h all' um eine Liste aller Kommandos zu erhalten.")
            wahlFunktion = 0
        try:
            if kommando[0] in ['h','s']:
                argumente = [str(arg.strip()) for arg in kommando.strip().split()[1:]]
            else:
                argumente = [int(arg.strip()) for arg in kommando.strip().split()[1:]]
        except Exception as err:
            wahlFunktion = 0
            self.konsolen_Log(err)
        
        if wahlFunktion:
            wahlFunktion(self.spielerAmZug,*argumente)
        self.setze_angreifer_und_manneuver(self.spielerAmZug)

    def spielerzug(self,spielerPos):
        """
        spielerzug beinhaltet die Truppenverteilung, Gefechtsführung 
        und schließlich das Mannöver eines Spielers.

        Ziel ist es, dass die Spielinstanz mit dem Spieler kommuniziert, 
        indem sie ihm seine Spielsituation zeigt und alle möglichen Handlungen 
        vorschlägt. Der Spieler soll dann solange Handlungen durchführen,
        wie er kann oder will. 

        Der Spielerzug unterteilt sich in die 3 Phasen:
        Verstärkung
        Angriff
        Mannöver

        Der Spielerzug endet, sobald eine der folgenden Bedingungen eingetreten ist:
        a) Der Spieler beendet freiwillig die Angriffsphase und führt nur noch ein Mannöver aus
        b) Der Spieler kann keine Angriffe mehr ausführen, weil er nur noch eine Truppe pro Gebiet hat
        c) Falls er einen anderen Spieler ausgelöscht und dessen Karten erhalten hat und gezwungen ist,
        die Karten sofort einzutauschen, so darf er nochmal Truppen verteilen und dann ein Mannöver ausführen
        """
       
            

        #Liste die möglichen Aktionen auf
        aktionen,kommandos = self.get_aktionen()
        wahlFunktion = 0
        while wahlFunktion == 0:
            match self.spielerliste[spielerPos].type:
                case 'KI':
                    wahlKommando = self.spielerliste[spielerPos].wähle_aktion(kommandos,hand=self.hand[spielerPos],
                                                        gebiete=self.gebieteVon[spielerPos],
                                                        mussKartenSetzen = self.get_zustand("mussKartenSetzen"),
                                                        nachbarn=[self.map.gibNachbarn(geb) for geb in self.gebieteVon[spielerPos]],
                                                        truppenVerteilung=self.truppenZahl,
                                                        spielmap=self.map,
                                                        truppen=self.get_zustand("truppen"),
                                                        angreifer=self.get_zustand("angreifer"),
                                                        angriffsZiele=self.get_zustand("angriffsZiele"),
                                                        validKlassen=self.get_zustand("validKlassen"),
                                                        validGeb=self.get_zustand("validGeb"),
                                                        besatzung=self.besatzung,
                                                        wahlAng=self.get_zustand("wahlAng"),
                                                        ziel=self.get_zustand("ziel")
                                                        )
                case _:
                    wahlKommando = self.spielerliste[spielerPos].wähle_aktion(kommandos)
            try:
                self.konsolen_Log(f"Eingabe:\t{wahlKommando}")
                wahlFunktion = aktionen[[k[0] for k in kommandos].index(wahlKommando[0])]
            except:
                self.konsolen_Log(f"'{wahlKommando}' ist kein gültiges Kommando. Benutze 'h all' um eine Liste aller Kommandos zu erhalten.")
                wahlFunktion = 0
            try:
                if wahlKommando[0] in ['h','s']:
                    argumente = [str(arg.strip()) for arg in wahlKommando.strip().split()[1:]]
                else:
                    argumente = [int(arg.strip()) for arg in wahlKommando.strip().split()[1:]]
            except Exception as err:
                wahlFunktion = 0
                self.konsolen_Log(err)

        
        wahlFunktion(spielerPos,*argumente)
        if self.sg:
            self.logge_zustand_karte()
        self.setze_angreifer_und_manneuver(spielerPos)
                
        
    
    


    def manneuver(self,spielerPos, start, ziel, anzahl):
        anzahl = min(anzahl,self.truppenZahl[start]-1)
        if self.besatzung[start] == spielerPos and self.besatzung[ziel] == spielerPos and self.truppenZahl[start] > anzahl and anzahl>-1:
            if self.map.ist_erreichbar(start,ziel,self.gebieteVon[spielerPos]):
                self.konsolen_Log(f"{self.spielerliste[spielerPos].name} führt Mannöver durch:"
                                    f"{self.map.gebiete[start]}({start}) -- +{anzahl} --> {self.map.gebiete[ziel]}({ziel})")
                self.mache_truppen(ziel,anzahl)
                self.vernichte_truppen(start,anzahl)
                self.zug_beenden()

            else:
                self.konsolen_Log("Kein Pfad durch eigene Gebiete für dieses Mannöver")
        return 0
    
    
    def verstärken(self,spielerPos,*args):
        """
        
        args    : Liste von ort/anzahl-Paaren
        ort     : zu verstärkendes Gebiet
        anzahl  : verstärkung in truppenzahl

        logik für das richtige verstärken der Gebiete eines Spielers
        Annahme hier: der Spieler besitzt mindestens ein Gebiet
        Die Liste der übergebenen Paare wird so lange abgearbeitet wie möglich
        Falls eine anzahl > truppen die zu verteilen sind -> ignoriere
        """
        args = list(args)
        #ignoriere bei ungerader Argumentzahl das letzte positionale Argument
        if len(args)%2 != 0:
            args.pop()
        
        while args and self.get_zustand("truppen"):
            ort = args.pop(0)
            anzahl= args.pop(0)
            
            if self.besatzung[ort] != spielerPos:
                self.konsolen_Log("Kann nur eigene Gebiete verstärken")
                return 0
            zusatz = min(anzahl,self.get_zustand("truppen"))
            self.mache_truppen(ort,zusatz)
            self.set_zustand(truppen=self.get_zustand("truppen")-zusatz)
        return 0
    
    
    def spieler_mitziehen(self,spielerPos,*args):
        """nach einer Eroberung entscheidet ein Spieler, wie viele der nichtbeteiligten Truppen mit in das eroberte Gebiet einfallen.
        Die Funktion ignoriert bis auf das erste positionale Argument alles"""
        anzahl = self.get_zustand("anzahlAngreifer")
        if args:
            anzahl = max(anzahl,args[0])
        anzahl = min(self.truppenZahl[self.get_zustand("wahlAng")]-1,anzahl) 
        self.vernichte_truppen(self.get_zustand("wahlAng"),anzahl)
        self.mache_truppen(self.get_zustand("ziel"),anzahl)
        self.set_zustand(wahlAng = -1, ziel = -1)
        self.set_zustand(erhKarte=True)
        return 0
        
    def spieler_gefecht(self,spielerPos,*args):
        """Ändert aktuellen agreifer und ziel
        Falls args gegeben sind geht die Funktion von zwei Zahlen aus: Index des angreifenden und des verteidigenden Gebiets"""
        if len(args)==2:
            angreifer = args[0]
            verteidiger = args[1]
            
        else:
            angreifer = self.spielerliste[spielerPos].wähle_angreifer(self.get_zustand("angreifer"),[self.truppenZahl[j] for j in self.get_zustand("angreifer")],self.get_zustand("angriffsZiele"))
            verteidiger = self.spielerliste[spielerPos].wähle_verteidiger(self.get_zustand("angriffsZiele"),[self.truppenZahl[j] for j in self.get_zustand("angriffsZiele")])
        potentielleAngreifer = self.get_zustand("angreifer")
        #Prüfe ob das übergebene Angreifergebiet überhaupt Angreifen kann
        #und ob das übergebene verteidigergebiet in der entsprechenden Liste
        #von Zielen für den Angreifer liegt
        if angreifer in potentielleAngreifer:
            if verteidiger in self.get_zustand("angriffsZiele")[potentielleAngreifer.index(angreifer)]:
                self.konsolen_Log(f"{self.map.gebiete[angreifer]} ({self.truppenZahl[angreifer]} Truppen) vs {self.map.gebiete[verteidiger]} ({self.truppenZahl[verteidiger]} Truppen)")
                self.set_zustand(wahlAng=angreifer,ziel=verteidiger,trAng=self.truppenZahl[angreifer],trZiel=self.truppenZahl[verteidiger])
        else:
            self.konsolen_Log("Dieser Angriff funktioniert nicht")
        return 0
    
    def gefecht(self,spielerPos,*args):
        """Hier entscheiden die Spieler, wie viele Truppen sie
        ins Gefecht schicken und es wird ausgewürfelt, was rauskommt"""
        try:
            angreifer = args[0]
            verteidiger = args[1]
        except:
            angreifer = self.get_zustand("wahlAng")
            verteidiger = self.get_zustand("ziel")
        anzahlAngreifer = min(3, self.truppenZahl[angreifer]-1)
        anzahlVerteidiger = min(2,self.truppenZahl[verteidiger])
        probs = self.probs[anzahlAngreifer-1][anzahlVerteidiger-1]
        #für mitziehen
        self.set_zustand(anzahlAngreifer=anzahlAngreifer)
        r = random.random()
        if len(probs)==1:
            if r<probs[0]:
                self.konsolen_Log(f"Angreifer besiegt eine Truppe")
                self.set_zustand(trZiel=self.get_zustand("trZiel")-1)
                self.vernichte_truppen(verteidiger,1)
            else:
                self.konsolen_Log(f"Angreifer verliert eine Truppe")
                self.set_zustand(trAng=self.get_zustand("trAng")-1)
                self.vernichte_truppen(angreifer,1)
        else:
            if r<probs[0]:
                self.konsolen_Log(f"Angreifer besiegt zwei Truppen")
                self.set_zustand(trZiel=self.get_zustand("trZiel")-2)
                self.vernichte_truppen(verteidiger,2)
            elif r>1-probs[1]:
                self.konsolen_Log(f"Angreifer verliert zwei Truppe")
                self.set_zustand(trAng=self.get_zustand("trAng")-2)
                self.vernichte_truppen(angreifer,2) 
            else:
                self.konsolen_Log(f"Angreifer und Verteidiger verlieren je eine Truppe")
                self.set_zustand(trAng=self.get_zustand("trAng")-1)
                self.vernichte_truppen(angreifer,1)
                self.set_zustand(trZiel=self.get_zustand("trZiel")-1)
                self.vernichte_truppen(verteidiger,1)

        if self.get_zustand("trZiel") == 0:
           
            
            self.gebieteVon[self.besatzung[verteidiger]].remove(verteidiger)
            
            if not self.gebieteVon[self.besatzung[verteidiger]]:
                        self.entferne_spieler(self.besatzung[verteidiger])
                        self.hand[spielerPos] += self.hand[self.besatzung[verteidiger]]
                        self.hand[self.besatzung[verteidiger]] = []
                        if len(self.hand[spielerPos])>2:
                            self.pruefe_boni(spielerPos)

            self.besatzung[verteidiger] = spielerPos
            self.gebieteVon[spielerPos].append(verteidiger)

        #Angriff wird beendet, da Angreifer alle Truppen verloren hat
        elif self.get_zustand("trAng")==1:
            self.set_zustand(wahlAng=-1,ziel=-1,trZiel=0,trAng=0)
            self.setze_angreifer_und_manneuver(self.spielerAmZug)
            return 0

        
    def verlasse_spiel(self,spielerPos):
        """Spieler wird durch KI ersetzt, die für ihn zu Ende spielt"""
        self.konsolen_Log(f"{self.spielerliste[spielerPos].name} wird vom Computer übernommen...\n")
        self.spielerliste[spielerPos] = KIplayer(self.spielerliste[spielerPos].name+"BOT", "KI",0)
        return 0
        
    def entferne_spieler(self,spielerPos):
        self.aktiveSpieler.remove(spielerPos)
        spieler = self.spielerliste[spielerPos]
        self.konsolen_Log(f"Spieler {spieler.name} wurde ausradiert")
        spieler.entlassen()
        self.spielerliste[spielerPos] = None
        if len(self.aktiveSpieler)<2:
            self.konsolen_Log(f"{self.spielerliste[self.spielerAmZug]} siegt als Alleinherrscher!")
            self.spiel_ende()
        

    def ziehe_karte(self, spielerPos)->karte.karte:
        """Poppe eine Karte vom Stapel und füge sie dem aktiven Spieler hinzu"""
        karte = self.stapel.pop()
        self.hand[spielerPos].append(karte)
        return karte

    def entferne_karte(self, spielerPos, karte):
        self.hand[spielerPos].remove(karte)

    def verteile_truppen(self,truppen,spielerPos):
        akteur = self.spielerliste[spielerPos]
        for i in range(truppen):
                k = akteur.verteile_truppe(self.gebieteVon[spielerPos],[self.truppenZahl[j] for j in self.gebieteVon[spielerPos]])
                if k == -1:
                    self.spielerliste[spielerPos] = KIplayer(akteur.name, "KI",0)
                    akteur = self.spielerliste[spielerPos] 
                    k = akteur.verteile_truppe(self.gebieteVon[spielerPos],[self.truppenZahl[j] for j in self.gebieteVon[spielerPos]])
                self.mache_truppen(k,1)
                self.konsolen_Log(f"{akteur.name} verstärkt Gebiet {k}")

    def mache_truppen(self,ort,zahl):
        """Fügt 'zahl' Truppen dem Gebiet 'ort' hinzu"""
        self.truppenZahl[ort] += zahl
        #self.konsolen_Log(f"Erhöhe Truppenzahl in {self.map.gebiete[ort]} von {self.truppenZahl[ort]-1} auf {self.truppenZahl[ort]}")

    def vernichte_truppen(self,ort,zahl):
        """Entfernt 'zahl' Truppen aus dem Gebiet 'ort'"""
        self.truppenZahl[ort] -= zahl

    

    def zeige_start(self,spielerMenge):
        """Loggt den Zwischenstand jedes Spielers in der spielerMenge"""
        anzahl = len(spielerMenge)
        gebieteSpieler = ["" for i in range(anzahl)]
        
        for k in range(anzahl):
            for i in self.gebieteVon[spielerMenge[k]]:
                gebieteSpieler[k] += f" {i}({self.map.gebiete[i]}, {self.truppenZahl[i]}),\n"
            if self.spielerliste[spielerMenge[k]] != None:
                self.konsolen_Log(f"{self.spielerliste[spielerMenge[k]].name}:\n"+gebieteSpieler[k])
                self.konsolen_Log(f"{self.spielerliste[spielerMenge[k]].name}s Hand:{[(karte.id,karte.bonus) for karte in self.hand[spielerMenge[k]]]}\n")
            

    def spiel_ende(self):
        """Gibt Endpunktestand aus wenn logging aktiviert und gibt den Gewinner zurück"""
        self.konsolen_Log("Punkteübersicht der Spieler:\n")
        punkte = [0 for s in self.spielerliste]
        for n in range(len(self.spielerliste)):
            if self.spielerliste[n]:
                punkte[n] += sum([1 for id in self.besatzung if id == n])
                self.konsolen_Log(f"{self.spielerliste[n].name}: {punkte[n]} Punkte")
            gewinner = [i for i in range(len(punkte)) if punkte[i] == max(punkte)]
        time.sleep(1)
        self.ende = True
        self.spielerAmZug = -1    
        return gewinner
            
    def erzwinge_ende(self):
        
        self.spiel_ende()

    def konsolen_Log(self,string,logAktiv=False):
        if logAktiv or self.log:
            print(string)
    
    def main(self):
        if self.sg:
            filename = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            path = "data\\"
            for border in self.map.grenzen:
                path += str(border[0]+border[1]).replace('(',"").replace(')',"").replace(', ',"")
            print(f"PATH: {path}")
            path = path[0:min(len(path),16)]+"l"+str(len(path))

            try:
                os.makedirs(path)
            except FileExistsError:
                pass
            except Exception as err:
                print(err)
                time.sleep(4)

            self.sg = path+"/"+filename
            try:
                with open(path+"/"+"borders.csv",'x') as file:
                    writer = csv.writer(file, lineterminator="\n")
                    writer.writerows(self.map.grenzen)
            except FileExistsError:
                self.konsolen_Log("file exists")
            except Exception as err:
                print(err)
                time.sleep(3)
            try:
                with open(self.sg+"b"+".csv",'x') as file:
                    writer = csv.writer(file,lineterminator="\n")
                    writer.writerow(self.besatzung)
            except FileExistsError:
                self.konsolen_Log("file exists")
            except Exception as err:
                print(err)
                time.sleep(3)
            try:
                with open(self.sg+"t"+".csv",'x') as file:
                    writer = csv.writer(file,lineterminator="\n")
                    writer.writerow(self.truppenZahl)
            except FileExistsError:
                self.konsolen_Log("file exists")
            except Exception as err:
                print(err)
                time.sleep(3)
       
        while not self.ende:
            self.zug_starten()
            spielerPos = self.spielerAmZug
            while spielerPos == self.spielerAmZug:
                self.spielerzug(spielerPos)
                


##########################################################################################################################################
if __name__ == "__main__":
    from itertools import combinations as combo
    import sys
    import pickle

    karte.karte("","").karten_reset()
    yourName = 'KI'
    try:
        yourName = sys.argv[1]
        with open(sys.argv[2],'br') as file:
            feld = pickle.load(file)
        anzahlKarten = len(feld.gebiete)
    except Exception as err:
        print(err)
        if type(err) == 'IndexError':
            print("Starte eine Runde mit\n >py spiel.py <deinName> [<Pfad/serialisiertes_Spielfeld>]")
        print("Starte Standardkarte...")
        
        feld = spielfeld([(0,1),(0,2),(0,3),(1,3),(1,4),(2,3),(3,4),(3,5),(3,6),(3,8),(3,9),(4,6),(4,10),(5,7),(5,8),
                        (6,9),(6,10),(7,8),(7,11),(7,12),(8,9),(8,12),(8,13),(9,10),(9,13),(10,13),(12,13)],
                        ["Schleswig-Holstein","Mecklenburg-Vorpommern","Hamburg",
                        "Niedersachsen","Brandenburg","Nordrhein-Westfalen","Sachsen-Anhalt",
                        "Rheinland-Pfalz","Hessen","Thüringen","Sachsen",
                        "Saarland","Baden-Württemberg","Bayern"],
                        ["Britische Zone","Amerikanische Zone",
                        "Französische Zone","Sowjetische Zone"],
                        [2,1,1,3],
                        [0,3,0,0,3,0,3,2,1,3,3,2,1,1],[],[])
        karten = [karte.karte("",i%3 + 1) for i in range(14)] 
    else:
        karten = [karte.karte(feld.gebiete[i],i%3 + 1) for i in range(anzahlKarten)] 

    
    
    
    comsN = 3 if yourName=='KI' else 2  
    spielerN = ["Alice","Bob","Martin","Peter","Clara","Jasmin"]
    typen = ["KI"]
    zufallGegenspieler = random.choice(list(combo(spielerN,comsN)))
    spieler = [KIplayer(zufallGegenspieler[i],typen[i%len(typen)],0) for i in range(len(zufallGegenspieler))]
    if yourName != 'KI':
        spieler.append(HumanPlayer(yourName,"Mensch"))

 
    rundeEins = spiel(spieler,feld,karten,True,True)
    rundeEins.main() 

        
