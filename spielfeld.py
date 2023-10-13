import numpy as np
"""Diese Klasse dient einzig der Definition von der Kartentopologie.
Die zugehörigen Strukturen implizieren eine Sortierung der Gebiete.
Die Gebiete werden links nach rechts und oben nach unten sortiert.
Wenn Gebiet i Nachbarn j hat, dann hat auch Gebiet j Nachbarn i. Außerdem ist kein Gebiet sein 
eigener Nachbar. Deshalb reicht zum abspeichern der Inzidenzmatrix eine Liste von Tupeln
(i,j) mit 0<i<j<n für n Gebiete.

"""

class spielfeld:
    """Das Spielfeld besteht aus folgenden Datenstrukturen:
    (int,int)[] Grenzen : Inzidenzmatrix für nebeneinander liegende Gebiete
    str[] gebiete       : Namen der Gebiete
    int[] Region        : Namen der Regionen
    int[] regionBonus   : Liste der Boni pro Region
    int[] gebZuReg      : der i-te Eintrag ist die Nummer der Region des i-ten Gebiets
    boolean[] burg      : Hat Gebiet eine Burg
    int[] hafen         : Liste der Gebiete mit Hafen
    
    """

    def __init__(self, grenzen: list[(int,int)],gebiete: list[str],region: list[str],regionBonus: list[int],gebZuReg: list[int],burg: list[bool],hafen: list[int]) :
        self.grenzen    = grenzen
        self.gebiete    = gebiete
        self.region     = region
        self.regionBonus= regionBonus
        self.gebZuReg   = gebZuReg
        self.burg       = burg
        self.hafen      = hafen

    def gibNachbarn(self,gebietNr):
        return [j for (i,j) in self.grenzen if gebietNr == i]+[i for (i,j) in self.grenzen if gebietNr == j]

    def gib_name_gebiet(self,Nr):
        return self.gebiete[Nr]
    def gib_name_region(self,Nr):
        return self.region[Nr]
    def gib_region_von(self,gebiet):
        return self.gebZuReg[gebiet]
    def gib_anzahl_gebiete_in(self,region):
        return len([id for id in self.gebZuReg if id == region])
    
    def ist_erreichbar(self,ort1,ort2,erlaubteWege,gibErreichbar = False):
        """berechnet ob ort2 in der Hülle von ort1 vorkommt, wobei 
        die Hülle hier die Zusammehangskomponente zu ort1 im Teilgraphen 'erlaubteWege' ist"""
        erreichbar = {ort1}
        q = erreichbar
        while q:
            k = q.pop()
            if k == ort2 and (not gibErreichbar):
                return 1
            erreichbar = erreichbar | {k}
            q = q | set(self.gibNachbarn(k)) & set(erlaubteWege) - erreichbar
        if gibErreichbar:
            return erreichbar
        return 0
        
    

class Gebiet:
    """Graphische Repräsentation eines Gebietes.
    (fl,fl)             pos     : Koordinaten des Mittelpunkts eines Gebiets
    <Array (fl,fl)>     ecken   : Punkte eines Polygonzugs relativ zur Position des Mittelpunkts
    int                 region  : Id der Region
    """
    
    def __init__(self,mitte,ecken,region):
        self.pos = mitte
        self.ecken = ecken
        self.region = region

    def gib_pos(self):
        return self.pos
    def gib_ecken(self):
        return self.ecken
    
    def verschiebe(self,delta):
        """Gibt die Position um delta = (x,y) verschoben zurück"""
        return self.pos + delta
    def gib_polygon(self,faktor,neuePos):
        """gibt die Eckpunkte des Polygons relativ zur neuen Position zurück"""
        return [(ecke-neuePos)*faktor+neuePos for ecke in self.ecken]

class SpielfeldGrafik(spielfeld):
    """Eine Klasse zur Verknüpfung logischer und graphischer Elemente.
    Zusätzlich zu den Attributen der Elternklasse spielfeld nimmt der Konstruktor
    eine Liste von Instanzen der Klasse Gebiet. Annahme für die richtige Zuordnung 
    ist gebiete[k] ist Name von gebieteGrafik[k]"""
    def __init__(self, grenzen: list[(int,int)],gebiete: list[str],region: list[str],regionBonus: list[int],gebZuReg: list[int],burg: list[bool],hafen: list[int],gebieteGrafik: list[Gebiet]):
        super().__init__(grenzen,gebiete,region,regionBonus,gebZuReg,burg,hafen)
        self.gebieteGrafik = gebieteGrafik

    def verschiebe(self,delta):
        """Gibt die Positionen aller gebieteKGrafiken um delta = (x,y) verschoben zurück"""
        liste = []
        for geb in self.gebieteGrafik:
            liste.append(geb.verschiebe(delta))
        return liste

    def zoom(self,faktor,fixpunkt):
        """Gibt die um Faktor gestauchte Positionen der Gebiete um einem Fixpunkt zurück.
        """
        liste = []
        for geb in self.gebieteGrafik:
            liste.append((geb.verschiebe(-1*fixpunkt))*faktor+fixpunkt)
        return liste

    def gib_spielfeld(self,delta,faktor,fixpunkt):
        """Berechnet die Mittelpunkte und die Polygonecken relativ zur verschiebung um delta und
        streckung um faktor mit fixpunkt. Delta wird nach der Streckung angewandt."""
        mitten = self.zoom(faktor,fixpunkt)

if __name__ == "__main__":

    testfeld = spielfeld([(0,1),(0,2),(0,4),(0,7),(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,5),(5,6),(6,7),(7,8)] ,[],[],[]
                          )
    for k in range(9):
        print(testfeld.gibNachbarn(k))

    