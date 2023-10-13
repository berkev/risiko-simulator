import random
from itertools import combinations as combo
import math
import spielfeld
import time

PROBATTACKE = 0.85
"""
Spielerklasse:

Im Spiel Risiko kann man unterschiedliche Strategien und Taktiken nutzen, 
um einen Vorteil im Spielgeschehen zu erlangen. 

Spieler werden durch eine Spielinstanz instanziiert.

Vorerst bleibe ich bei der Objektorientierung um zusammengehörende Daten zu koppeln
aber lasse mir offen, auf die Klasse zu verzichten.

"""
class player:








    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type
        
    def verteile_truppe(self,gebiete,truppen,anzahl):
        schwacheGebiete = [gebiete[j] for j in range(len(gebiete)) if truppen[j]<2]
        if schwacheGebiete:
            return random.choice(schwacheGebiete)
        return random.choice(gebiete)
        
    def wähle_angreifer(self,gebiete,truppen,fremdeNachbarn):
        #len(gebiete) == len(truppen) == len(fremdeNachbarn)
        #gebiet[i] hat truppen[i] Truppen und kann fremdeNachbarn[i] angreifen
        if not len(gebiete) == len(truppen):
            print(f"{len(gebiete)} Gebiete aber {len(truppen)} Truppenstärken erhalten")
        if not len(gebiete) == len(fremdeNachbarn):
            print(f"{len(gebiete)} Gebiete aber {len(fremdeNachbarn)} Angriffszielmengen erhalten")

        zufall = random.random()
        if zufall<0.7:
            return gebiete[truppen.index(max([truppen[k] for k in range(len(gebiete)-1) if fremdeNachbarn[k]]))]
        if zufall>0.75:
            return random.choice( [gebiete[j] for j in range(len(gebiete)-1) if truppen[j]>1 and fremdeNachbarn[j]])
        else:
            return -1
    def wähle_ziel(self,gebiete,truppen):
        if not len(gebiete) == len(truppen) or not len(gebiete):
            print(f"{len(gebiete)} Gebiete aber {len(truppen)} Truppenstärken erhalten")
        zufall = random.random()
        if zufall<0.7:
            return gebiete[truppen.index(min(truppen))]
        if zufall>0.75:
            return random.choice(gebiete)
        else:
            return -1
    def entlassen(self):
        pass
    def angriff(self,truppenSelbst,truppenGegner):
        pass
    def mitziehen(self,a,v,truppenVerteilung,revier,aNachbarn,vNachbarn):
        pass
    def wähle_karten(self, hand, gebiete, zwang = False):
        pass
    def berechne_risiko(self,ort,spielerOrte,NachbarOrte,truppenVerteilung,spielmap):
        #risiko ist summe der truppen minus eigene Truppen plus 2 für jeden Nachbarort mit mehr Gebieten als 'ort' (Um ein aufstocken ) pro spieler
        #
        #Diese Funktion könnte auch bei truppen verteilen helfen
        #
        #risiko abspeichern und nur neu berechnen, wenn sich etwas verändert hat
        #
        #
        #Interessanter Gedanke: Das Risiko für ein Gebiet abhnängig vom Risiko jedes anderen machen -> DGL
        #

            risiko = round(10*sum([(truppenVerteilung[n]-truppenVerteilung[ort])/len(spielmap.gibNachbarn(n)) for n in set(NachbarOrte[spielerOrte.index(ort)])-set(spielerOrte)]+[0]))  
            
            risiko += 2*len(set([truppenVerteilung[ort] for ort in set(NachbarOrte[spielerOrte.index(ort)])-set(spielerOrte)]))
            return risiko

        
    
    def wähle_manneuver(self,spielerOrteErreichbarKlassen,spielerOrte,NachbarOrte,truppenVerteilung,spielmap):
        """SpielerOrte ist Liste der vom Spieler besetzten Gebiete,
            pro Eintrag ist in NachbarOrte eine Liste, truppenVerteilung
            ist der gesamte Vektor
            Rechnet für jedes Gebiet eines Spielers, dass mit mindestens einem
            anderen verbunden ist, einen Risikowert aus.
            Der Risikowert kommt zustande aus der Anzahl an gegnerischen Truppen in
            Nachbarländern.
            -1 als Standardwert für nicht erreichbare Orte.
            Gebiete sollen dann als Mannöverziel priorisiert werden, wenn:
             -viele Nachbarländer mit wenig Truppen pro Land
                -wenige Nachbarn mit viel Truppen pro Land
                  """
        potentialKlasse = [-1 for k in spielerOrteErreichbarKlassen]
        risiko = [0 for i in spielerOrte]
        for i in range(len(spielerOrteErreichbarKlassen)):
            klasse=spielerOrteErreichbarKlassen[i]
            if len(klasse) > 1:
                for ort in klasse:
                    risiko[spielerOrte.index(ort)] = self.berechne_risiko(ort,spielerOrte,NachbarOrte,truppenVerteilung,spielmap)
                potentialKlasse[i] = max([risiko[spielerOrte.index(ort)] for ort in klasse]) - min([risiko[spielerOrte.index(ort)] for ort in klasse if truppenVerteilung[ort]>1])
        KlMaxPot = spielerOrteErreichbarKlassen[potentialKlasse.index(max(potentialKlasse))]
        start = spielerOrte[risiko.index(min([risiko[spielerOrte.index(ort)] for ort in KlMaxPot if truppenVerteilung[ort]>1]))]
        ziel = spielerOrte[risiko.index(max([risiko[spielerOrte.index(ort)] for ort in KlMaxPot]))]
        if risiko[spielerOrte.index(start)]<0 and not set(NachbarOrte[spielerOrte.index(ort)])-set(spielerOrte):
            anzahl = truppenVerteilung[start]-1
        else:
            anzahl = min(truppenVerteilung[start]-1, risiko[spielerOrte.index(ziel)] - risiko[spielerOrte.index(start)] )
        return ' '.join([str(start),str(ziel),str(anzahl)])


        


class KIplayer(player):
    """
    Die KIplayer Klasse ist eine Kopplung von einem probabilistischen Automaten und ihrer Kommunikation mit dem Spiel.
    Zukünftig wäre es interessant diese Kopplung komplett zu lösen und eine künstliche Intelligenz an die Stelle eines
    Computers zu setzen. Diese muss dann erst trainiert werden und könnte beispielweise gegen den Automaten getestet werden.
    bool willErobern    :Falls die KI sich entschieden hat, auf eine 5. Karte zu warten wird diese auf 1 gesetzt
    int verzweiflung    :während willErobern aktiv ist, steigt diese mit jedem Verlust und wird danach zurückgesetzt
    int maxVerzweiflung :Grenze für das Level der Verzwiflung eines Spielers
    """

    def __init__(self, name: str, type: str, maxVerzweiflung: int) -> None:
        super().__init__(name,type)
        self.willErobern = 0
        self.verzweiflung = 0
        self.maxVerzweiflung = maxVerzweiflung
        self.erinnerungLetzteAktionen = ""


    
    def wähle_aktion(self,kommandos,**kwargs):
        x = random.random()
        kommandoBuchstabenKI = [kommando[0] for kommando in kommandos if kommando[0] not in ['s','h','x']]
        print("Kommandos:")
        print(kommandoBuchstabenKI)
        if 'i' in kommandoBuchstabenKI:
            eingabe = self.mitziehen(kwargs["wahlAng"],kwargs["ziel"],kwargs["truppenVerteilung"],kwargs["gebiete"],kwargs["spielmap"])
            self.erinnerungLetzteAktionen +='i'
            self.willErobern = 0
            self.verzweiflung = 0
            return 'i '+eingabe
        #Begrenzung der Züge für den Computer, der sonst immer so lange zieht, wie es möglich wäre
        if len(self.erinnerungLetzteAktionen)>12:
            self.erinnerungLetzteAktionen = ""
            print("Zu viele Aktionen")
            return 'e'
        
        
        if 'k' in kommandoBuchstabenKI:
            eingabe = self.wähle_karten(kwargs["hand"],kwargs["gebiete"],kwargs["mussKartenSetzen"])
            self.erinnerungLetzteAktionen += 'k'
            return 'k '+ eingabe
        if 'v' in kommandoBuchstabenKI:
            eingabe = self.verteile_truppe(kwargs["gebiete"],kwargs["nachbarn"],kwargs["truppenVerteilung"],kwargs["spielmap"],kwargs["truppen"])
            #self.erinnerungLetzteAktionen += 'v'
            return 'v '+ eingabe
        
        
        bedVerzweifeln = self.erinnerungLetzteAktionen and self.erinnerungLetzteAktionen[-1] == 'a' and 'a' not in kommandoBuchstabenKI
        if bedVerzweifeln:
            self.verzweiflung += 1
        if self.erinnerungLetzteAktionen and self.erinnerungLetzteAktionen[-1] == 'i' and x<0.8:
            if 'm' in kommandoBuchstabenKI:
                eingabe = 'm '+self.wähle_manneuver(kwargs["validKlassen"],kwargs["validGeb"],kwargs["nachbarn"],kwargs["truppenVerteilung"],kwargs["spielmap"])
            else:
                print("Ende wegen Invasion")
                eingabe = 'e'
            self.erinnerungLetzteAktionen = ""
            return eingabe

        if  'z' in kommandoBuchstabenKI and ('z' not in self.erinnerungLetzteAktionen  or self.verzweiflung and self.erinnerungLetzteAktionen and 'z' != self.erinnerungLetzteAktionen[-1]):
            
            eingabe = self.wähle_angreifer_und_ziel(kwargs["angreifer"],kwargs["truppenVerteilung"],kwargs["angriffsZiele"])
            self.erinnerungLetzteAktionen +='z'
            return 'z '+eingabe
        
        elif self.erinnerungLetzteAktionen and 'z' in self.erinnerungLetzteAktionen and 'a' in kommandoBuchstabenKI:
            #Falls keine weiteren Gebiete/Ziele existieren, greife immer an
            if x<max(1-('z' in kommandoBuchstabenKI),PROBATTACKE) or self.willErobern:
                self.erinnerungLetzteAktionen += 'a'
                return 'a'
            else:
                eingabe = self.wähle_angreifer_und_ziel(kwargs["angreifer"],kwargs["truppenVerteilung"],kwargs["angriffsZiele"])
                self.erinnerungLetzteAktionen +='z'
                return 'z '+eingabe
        print("Alle Optionen scheitern\n")
        self.erinnerungLetzteAktionen = ""
        self.willErobern = 1
        return 'e'
     
    def verteile_truppe(self,spielerOrte,NachbarOrte,truppenVerteilung,spielmap,anzahl):
        #todo schwache Gebiete, die aber isoliert vom feind sind, müssen nicht zwangsweise verstärkt werden
        #schlaues Verstärken mit Hinblick auf Angriffsziele und bedrohliche Gegener
        risiken = []
        auswahl = []
        for geb in spielerOrte:
            risiken.append(super().berechne_risiko(geb,spielerOrte,NachbarOrte,truppenVerteilung,spielmap))
        while anzahl>0:
            maxRisikoGeb = spielerOrte[risiken.index(max(risiken))]
            auswahl.append(maxRisikoGeb)
            auswahl.append(1)
            anzahl -=1
            risiken[spielerOrte.index(maxRisikoGeb)] -= sum([1/len(spielmap.gibNachbarn(k)) for k in set(NachbarOrte[spielerOrte.index(maxRisikoGeb)])-set(spielerOrte)])
        return ' '.join(str(nr) for nr in auswahl)
    
    def wähle_angreifer_und_ziel(self,gebiete,truppenVerteilung,fremdeNachbarn):
        #len(gebiete) == len(truppen) == len(fremdeNachbarn)
        #gebiet[i] hat truppen[i] Truppen und kann fremdeNachbarn[i] angreifen
        truppen = [truppenVerteilung[geb] for geb in gebiete]
        
        if not len(gebiete) == len(truppen):
            print(f"{len(gebiete)} Gebiete aber {len(truppen)} Truppenstärken erhalten")
        if not len(gebiete) == len(fremdeNachbarn):
            print(f"{len(gebiete)} Gebiete aber {len(fremdeNachbarn)} Angriffszielmengen erhalten")

        zufall = random.random()
        if zufall<0.9:
            wahlAng = gebiete[truppen.index(max([truppen[k] for k in range(len(gebiete)) if fremdeNachbarn[k]]))]
            truppenZiele = [truppenVerteilung[nb] for nb in fremdeNachbarn[gebiete.index(wahlAng)]]
            wahlZiel = fremdeNachbarn[gebiete.index(wahlAng)][truppenZiele.index(min(truppenZiele))]
            
        else:
            wahlAng = random.choice( [gebiete[j] for j in range(len(gebiete)) if truppen[j]>1 and fremdeNachbarn[j]])
            wahlZiel = random.choice(fremdeNachbarn[gebiete.index(wahlAng)])
        return str(wahlAng)+" "+str(wahlZiel)
        



    def wähle_manneuver(self,spielerOrteErreichbarKlassen,spielerOrte,NachbarOrte,truppenVerteilung,spielmap):
        return super().wähle_manneuver(spielerOrteErreichbarKlassen,spielerOrte,NachbarOrte,truppenVerteilung,spielmap)
        

    def angreifen(self,truppenSelbst,truppenGegner):
        x = random.random()
        if x<(truppenGegner/truppenSelbst)**2:
            return 0
        return 1
    
        
    def entlassen(self):
        return 0

    def mitziehen(self,a,v,truppenVerteilung,revier,spielmap):
        """Die KI wählt die Anzahl der mitgezogenen Truppen nach einer Eroberung anhand der folgenden Informationen:
        int a                       :Angreifendes Gebiet
        int v                       :Besiegtes Gebiet
        int[] truppenVerteilung     :Anzahl der Truppen[...] je Gebiet
        int[] revier                :Liste der kontrollierten Gebiete
        Spielfeld spielmap          :Referenz auf die Karte """
        #die KI macht es so:
        #erste Prio ist die Absicherung gegen Angriffe
        #die Truppen werden je nach Gefahr durch das Umland aufgeteilt
        #Gefahr ist der Anteil der Gesamtgefahr auf v
        aNachbarn = spielmap.gibNachbarn(a)
        vNachbarn = spielmap.gibNachbarn(v)
        gefahrA = sum([truppenVerteilung[k] for k in aNachbarn if k not in revier])
        gefahrV = sum([truppenVerteilung[k] for k in vNachbarn if k not in revier])
        #falls der spieler gezwungen war zu erobern, ist er es jetzt nicht mehr
        
        return str(round(truppenVerteilung[a]*(gefahrV)/max(gefahrV+gefahrA,1)))
    
    def wähle_karten(self, hand, gebiete, zwang = False):
        #Nehme an, dass es drei unterschiedliche, mit Ordnung versehene Typen von Bonussymbol gibt 
        bonusLvl = []
        LvlAnzahl = [0,0,0]
        #kandidaten = []
       
        #besterKandidatPos = 0
        besterKandidatWahl = []
        besterKandidat = 0
      
        for karte in hand:
            #Für jeden Bonustypen auf der Hand lege Zähler an
            if karte.bonus not in bonusLvl:
                bonusLvl.append(karte.bonus)
            LvlAnzahl[bonusLvl.index(karte.bonus)] += 1
        #Falls keine Omnikombo vorhanden, suche alle möglichen Trippel   
        if LvlAnzahl[0]*LvlAnzahl[1]*LvlAnzahl[2] == 0: 
            for i in [j for j in range(3) if LvlAnzahl[j] > 2]:
                kartenGleichBonus = [karte for karte in hand if karte.bonus == bonusLvl[i]]
                for combi in combo(kartenGleichBonus,3):
                    #kandidaten.append(list(combi))
                    
                    #hier werden die extraTruppen mit Gewicht 1 berücksichtigt ( vielleicht abschwächen ? )
                    aktuellerBonus = bonusLvl[i] + 2*len([karte for karte in list(combi) if karte.id in gebiete])
                    #Ersetze aktuellen kandidaten falls neuer besser ist
                    besterKandidat = aktuellerBonus if aktuellerBonus > besterKandidat else besterKandidat
                    
                    #besterKandidatPos = len(kandidaten)-1  if aktuellerBonus > besterKandidat else besterKandidatPos
                    besterKandidatWahl = list(combi)  if aktuellerBonus == besterKandidat else besterKandidatWahl
                    
        else:
            
            for i in range(3):
                #falls für omnibonus mehrere karten zur auswahl sind, präferiere diese, welche einen truppenbonus geben
                kartenGleichBonus = [karte for karte in hand if karte.bonus == bonusLvl[i]]
                if LvlAnzahl[i] > 1:
                    
                    truppenBonus = [karte for karte in kartenGleichBonus if karte.id in gebiete]
                    if truppenBonus:
                        besterKandidatWahl.append(truppenBonus[0])
                    else:
                        besterKandidatWahl.append(kartenGleichBonus[0])
                else:
                    besterKandidatWahl.append(kartenGleichBonus[0])
            

        #Falls der Spieler nicht gezwungen ist die Karten abzugeben und schon 2 verschiedene Symbole hat,
        #besteht die Wahrscheinlichkeit von 1/3 auf die nächste Karte zu warten
        # in dem Fall sollte der Spieler aber auch erobern wollen  
        
        
        return ' '.join(str(hand.index(nr)) for nr in besterKandidatWahl)



class HumanPlayer(player):
    """Klasse für die Kommunikation mit einem festgelegten Spieler
        bisher geht alles durch den Standard IO
        in Zukunft soll das auch verteilt funktionieren
        """

    def __init__(self, name: str, adresse: str) -> None:
        super().__init__(name,"Mensch")
        self.adresse = adresse

    def wähle_aktion(self,kommandos,**kwargs):
        print(" ",end="")
        print('\n '.join(kommandos))
        # while not self.adresse:
        #     time.sleep(2)

        # msg = self.adresse
        # self.adresse = ""
        # return msg
        return input("\n")
    
    def verteile_truppe(self,spielerOrte,NachbarOrte,truppenVerteilung,besatzung,anzahl):
        gebiete = None
        truppen = None
        wahl = input(f"\n {anzahl} Truppen verfügbar. Wähle die Gebiete (nr) und wieviele Truppen darauf kommen?\n")
        wahl = wahl.strip()
        try:
            eingabe = [int(z) for z in wahl.split(" ")] 
        except:
            return []
        return eingabe  
     

    def wähle_angreifer(self,gebiete,truppen,fremdeNachbarn):
        truppen = None
        wahl = -8
        print(gebiete)
        while wahl not in gebiete and wahl != -1:
            try:
                wahl = int(input("\nMit welchem Gebiet angreifen(-1 beendet den Zug)?\n"))
            except Exception:
                print("What?!?")
                wahl = -8
            finally:
                continue
        return wahl  
        

    def wähle_ziel(self,gebiete,truppen):
        truppen = None
        wahl = -8
        print(gebiete)
        while wahl not in gebiete and wahl != -1:
            try:
                wahl = int(input("\nWelches Gebiet angreifen(-1 beendet den Zug)?\n"))
            except Exception:
                print("What?!?")
                wahl = -8
            finally:
                continue
        return wahl 
    
    def entlassen(self):
        return input("Aufhören?")

    def angriff(self,truppenSelbst,truppenGegner):
        if not(truppenGegner and truppenSelbst-1):
            return 0
        eingabe = input(f"\n{truppenSelbst-1} vs {truppenGegner}?\n")
        return not eingabe
    
    def mitziehen(self,a,v,truppenVerteilung,revier,aNachbarn,vNachbarn):
        """Entscheide, wie viele Truppen nach einem Angriff mitgenommen werden"""
        anzahl = -8
        while anzahl not in range(truppenVerteilung[a]):
            try:
                return int(input(f"Wieviele der {truppenVerteilung[a]-1} mobilen Truppen mitnehmen?\n"))
            except:
                return 0
            finally:
                pass

    def wähle_karten(self, hand, gebiete, zwang = False):

        
        wahl = []
        optionalText = "(oder leere Eingabe um noch keine Karten zu legen)" if not zwang else ""
        print("Wähle 3 Karten durch Wahl ihrer Nummer mit Leertaste getrennt"+optionalText+".\n")
        while len(wahl)<3:
            eingabe = input(f"{str([(i,hand[i].id,hand[i].bonus) for i in range(len(hand))])}\n")
            if not bool(eingabe):
                return []
            wahl += [hand[int(zahl)] for zahl in eingabe.split(" ")]
        return wahl
            
    def wähle_manneuver(self,spielerOrteErreichbarKlassen,spielerOrte,NachbarOrte,truppenVerteilung,besatzung):
        empf = super().wähle_manneuver(spielerOrteErreichbarKlassen,spielerOrte,NachbarOrte,truppenVerteilung,besatzung)
        pufferN = 3
        
        eingabe = "."
        while eingabe:
            eingabe = input(f"Empfohlenes Mannöver: {empf[0]} -- +{empf[2]} --> {empf[1]}, \n'start ziel anzahl' oder leer lassen für kein Mannöver\n")
            
            try:
                start,ziel,anzahl = [int(k) for k in [j.strip() for j in eingabe.strip().split(" ") if j ][0:pufferN]]
                return start,ziel,anzahl
            except:
                return 0
            
        return 0


        