
# Risiko Brettspiel-Simulator

Der Brettspiel-Klassiker "Risiko" und seine zahlreichen Versionen erfreuen sich großer Beliebtheit. Aufregende Schlachten, der Wunsch nach Weltherrschaft, Bündnisse und Betrug sind Teil einer üblichen Risiko-Runde. Reize, die meine Freunde und mich regelmäßig zu einer Partie verführen.


## Spielphasen

Um einen Kontext für die folgenden Abschnitte zu erhalten wird hier kurz zusammengefasst, welche üblichen Phasen während eines Spiels vorkommen. Ist der Leser mit dem Spiel vertraut,
möge er direkt zur [Einleitung](#einführung) springen.


### Start

Folgende Teile des Zubehörs werden ausgepackt:
- Ein Spielbrett
- 5 Würfel
- ein Satz Truppenfiguren pro Spieler, verschiedene Farben
- ein Kartenstapel passend zum Spielbrett mit einer Spezialkarte, die das Spielende ausruft

Der Kartenstapel wird gemischt und die Spezialkarte wird irgendwo in die untere Hälfte des Stapels gesteckt.
Das Spielbrett zeigt je nach Version einen Kartenausschnitt der Erde oder einer fiktiven Welt. Die einzelnen Gebiete oder Länder werden zufällig
unter den Spielern aufgeteilt. 
Zum Schluss dieser Phase sollten alle Spieler jeweils drei ihrer Truppenfiguren auf die zugeteilten Gebiete gestellt haben. Es wird ausgewürfelt,
welcher Spieler den ersten Zug machen darf. 
Sind Gebiete übriggeblieben, weil die Zahl an Gebieten nicht restlos durch die Anzahl Spieler teilbar ist so erhalten fairerweise die Spieler je ein
übriges Gebiet, welche am längsten auf ihren Zug warten müssen. 

### Spielerzug

Der Zug eines Spielers besteht aus drei Phasen:
- Verstärkung
- Angriff
- Mannöver

#### Verstärkung

Abhängig von der Anzahl an besetzten Gebieten und weiteren Faktoren, die im Abschnitt [Bonustruppen](#bonustruppen) erklärt werden, darf 
der Spieler Truppenfiguren aus seiner Reserve verteilen. Die Figuren dürfen frei unter den durch den Spieler besetzten Gebieten aufgeteilt werden

##### Bonustruppen

Die Gebiete der Spielbretts erkennbar an ihrer Farbe in Regionen eingeteilt. Besitzt ein Spieler alle Gebiete einer Region, erhält er einen regionsabhängigen Bonus auf die zu verteilenden
Truppenfiguren. 
Hat der Spieler 3 Karten mit passenden aufgedruckten Symbolen, darf er diese eintauschen um noch mehr Figuren verteilen zu dürfen. Haben die Karten paarweise unterschiedliche Symbole, ist der Bonus noch größer. 

#### Angriff

Diese Phase ist optional. Der Spieler darf in dieser Phase solange Gefechte führen, wie es ihm möglich ist. Ein Gefecht zwischen angrenzenden Gebieten A und B ist möglich, wenn auf A mindestens
zwei Truppenfiguren des Spielers stehen und B von einem Gegenspieler besetzt ist.

Will der Spieler ein Gefecht zwischen Gebieten A und B ausführen, würfelt er mit einem bis drei Würfeln. Der Spieler, dem das Gebiet B gehört, würfelt mit einem oder zwei Würfeln. 
Ist die größte gewürfelte Zahl des Spielers größer als die größte Würfelzahl des Gegners, muss der Gegner eine Figur von seinem Gebiet entfernen. Ansonsten muss der Spieler eine Figur vom eigenen Gebiet entfernen. Falls beide Spieler mehr als einen Würfel benutzt haben, wird die zweitgrößte Würfelzahl verglichen und erneut im entsprechenden Gebiet eine Figur entfernt. Entfernte Figuren kommen wieder in die Truppenreserve des entsprechenden Spielers.
Die maximale Anzahl an genutzten Würfeln richtet sich nach der Anzahl an Figuren auf einem Gebiet. Der Gegner darf zwei Würfel benutzen, wenn zwei oder mehr Figuren auf dem Gebiet B stehen.
Der Spieler darf n <= k = 1,2,3 Würfel benutzen, wenn k+1 Figuren auf Gebiet A stehen.

Ein Gefecht hat somit folgende Ausgänge:
- Der Spieler oder der Gegner muss eine oder zwei Figur(en) zurück in die Reserve legen
- Beide Spieler müssen je eine Figur zurück in die entsprechende Reserve legen

Eroberung: Hat Gebiet B nach einem Gefecht keine Figuren mehr, so bewegt der Spieler mindestens so viele seiner Figuren in das Gebiet B, wie er Würfel benutzt hat. Eine Figur muss jedoch auf Gebiet A bleiben.

#### Mannöver

Diese Phase ist optional. Der Spieler kann Truppenfiguren zwischen zwei seiner Gebieten verschieben. Das ist allerdings nur möglich, wenn die Gebiete benachbart oder durch eine Kette von benachbarten Gebieten des Spielers verbunden sind.
Nach einem Mannöver darf der Spieler keine Aktionen mehr für diesen Zug ausführen. Fand in der Angriffsphase eine Eroberung statt, zieht der Spieler eine Karte vom Stapel. Ist die gezogene Karte die Spezialkarte, endet das Spiel.

### Spielende

Wurde die Spezialkarte gezogen oder hat ein Spieler alle Gebiete erobert, endet das Spiel. Jeder Spieler zählt seine Gebiete. Der Spieler mit den meisten Gebieten hat gewonnen.


## Einführung

Um einen Kontext für die besprochenen Begriffe zu erhalten möge der Leser bitte diese [Erklärung](#spielphasen) lesen.

Ursprünglich ist dieses Projekt entstanden, um für eine beliebige (Start-)Konfiguration des Spiels mithilfe der Analyse von Markovketten eine ideale Strategie zu finden. Das Spielbrett wird zu einem bidirektionalen Graphen abstrahiert. Jedes Gebiet des Spielfelds entspricht einem Knoten in diesem Graphen. Zudem sind jedem Knoten eine natürliche Zahl größer als 0 und eine Farbe zugeordnet, die jeweils der Anzahl an Truppenfiguren und einem Spieler entsprechen. Die Menge der Truppenzahl-Farb-Tupel für alle Knoten bilden eine Konfiguration. Der Raum aller Konfigurationen ist somit abhängig vom gewählten Spielbrett, der Anzahl an Farben(Spielern) und der Anzahl an Truppenfiguren, über die ein Spieler maximal verfügen kann. 
Ein Spiel ist ein diskreter stochastischer Prozess auf einem solchen Konfigurationsraum. Ein Spielerzug entspricht einem Zeitschritt dieses Prozesses. Macht man die starke und i.A. unpassende Annahme, dass die Spieler ihre Handlungen während eines Zuges unabhängig vom vorherigen Spielverlauf wählen, so lässt sich dieser Prozess als Markovkette modellieren. 


Nach der ersten Implementation eines in der Kommandozeile spielbaren Simulators hat sich jedoch der Fokus auf Erweiterbarkeit und lokale Mehrspielermöglichkeit verschoben, weswegen ein zweites Projekt entstanden ist. 




## Pythonimplementierung

Der Spielsimulator wurde in Python geschrieben Die wichtigsten Klassen werden im folgenden kurz vorgestellt:

### Spiel

 Bildet den Zustand eines Spiels ab. Dazu gehört die Liste der Spieler,
eine Karte, auf der gespielt wird und ein Stapel Spielkarten. Weiterhin liegen hier die Funktionen, die Handlungen wie Verstärkung der Truppen, Mannöver und Angriffe nach Prüfung der Gültigkeit auf den Zustand des Spiels abbilden. Die Funktion start startet ein Spiel und hört erst auf, wenn ein [Endzustand](#spielende) erreicht ist.

### Spielfeld

Instanzen dieser Klasse modellieren den Ausschnitt einer Weltkarte, auf dem ein Spiel stattfindet. Attribute sind Gebietsnamen, Regionsnamen und Listen, die Gebieten Regionen, Nachbarn, Burgen und Häfen zuordnen. Neben Methoden, die ein Attribut zurückgeben ist eine angepasste Dijkstra-Methode vorhanden, die zu einer gegebenen Teilmenge an Gebieten ihre Zusammenhangskomponenten findet.

### Player

Die Stammklasse für HumanPlayer und KIplayer. 
- KIplayer: Diese Klasse wird mit einem Namen instanziiert und enthält Methoden für jede vom Spieler zu treffende Entscheidung. Der KIplayer entscheidet, welche Gebiete er verstärken möchte, wen und wie lange er angreift, wie viele Truppen er nach einer Eroberung mitziehen möchte, ob und welche Karten er setzt und wie er mannövrieren will.
- HumanPlayer: Bildet eine Schnittstelle zwischen Spiel und Eingabemedium. 

### Tests

Für die ersten drei Klassen wurden bereits ein paar Unittests geschrieben. Sie befinden sich im Unterordner tests.

### Karte

Diese Klasse ist hauptsächlich dafür verantwortlich, Gebiete und Kartenboni zu verbinden. Vor einem Spiel wird eine Liste an Karten instanziiert, die während eines Spiels durch list.pop entfernt werden. Da der interne Zähler der Klasse zur ID-Verteilung an die Karten genutzt wird, muss dieser nach einem Spiel durch die Karte.reset()-Methode zurückgesetzt werden.

## Anleitung

### Requirements

Die externen Bibliotheken sind in der Datei req.txt gelistet.

Bisher wurde das Projekt nur unter Python 3.11 und Windows 10 getestet.

Am besten führt man das Skript aus einer virtuellen Umgebung aus, in der Python 3.11 und die benötigten Bibliotheken installiert sind. Hier findet sich eine kurze Anleitung zum Anlegen
einer virtuellen Umgebung mit [venv](https://docs.python.org/3/library/venv.html)*.


### Ein Spiel starten

`py spiel.py name [Pfad/zu/einer/gepickleten/spielfeldinstanz]`



Möchte man nur eine Simulation zwischen Computern laufen lassen, kann man als erstes Kommandozeilenargument 'KI' ohne Anführungszeichen eingeben oder das Kommando ohne Argumente ausführen.

Beide Argumente sind jedoch optional. Wird das zweite Argument weggelassen, beginnt die Simulation auf einer fiktiven Standardkarte, in der alle Referenzen auf echte Orte
rein zufällig sind.

Führt man eine Simulation zwischen Computern durch, kann man den gesamten Spielverlauf in der Konsole nachlesen. Möchte man spielen, so dient eine textuelle Benutzerschnittstelle mit Hinweisen zu den möglichen Kommandos der Eingabe.


## Ziele 

### Konzepte

- HumanPlayer und Spiel: eine einheitliche Kommunikation und Logikprüfung soll zwischen Spielern und dem Spiel stattfinden. Die Idee ist, dass für jede Spielhandlung eine einheitliche Syntax existieren soll. Das Spiel prüft dann im ersten Schritt die Syntax des Spielerinputs und wiederholt gegebenfalls den Aufruf nach Input, aber kommuniziert in jedem Fall den Syntaxfehler an den Spieler. Erst wenn eine syntaktisch korrekte Eingabe im Spiel bearbeitet wird, prüft das Spiel diese hinsichtlich logischer Durchführbarkeit.

- Spielverlauf speichern: Ein Dateiformat muss ausgearbeitet werden, dass jede Handlung des Spiels auf möglichst sparsame Weise codiert. Es soll dann möglich sein, sich ein Replay des Spiels anzuschauen.

- Spiel.start und Spiel.Spielerzug: Ein wohldefinierter Zustandsapparat soll zu Beginn jedes Zugs berechnen, welche Handlungen durchgeführt werden können. Dieser soll die strikte Reihenfolge in der aktuellen spiel.start()-Methode aufbrechen und für eine dynamischere Spielabfolge sorgen.

- Grafische Oberfläche: Das Spiel soll den aktuellen Zustand in einem grafischen Fenster darstellen. Dazu muss für eine geladene Karte eine Abbildung zwischen Koordinaten und den zugehörigen Gebieten der Spiel-Instanz implementiert werden.

- Mapeditor: Der Nutzer soll ein Tool erhalten, mit dem er eigene Karten designen kann. Es soll ihm ermöglichen, mit einem Pinsel auf ein leeres Kanvas zu zeichnen, mit einer ausgewählten Farbe einen abgeschlossenen Bereich zu färben und den Gebieten Namen zu geben und Burgen/ Häfen einzufügen. Er soll Regionen definieren können und auch ihren Truppenbonus bestimmen. Das ganze soll dann exportiert werden in einem Format, das vom Hauptprogramm in eine Spielfeldinstanz übersetzt werden kann. Zudem soll ein Kartensatz zur Map generiert werden, wobei jede Karte einem Gebiet zugeordnet wird. Die Bonussymbole sollen 

- Zufallsmap: Es soll die Möglichkeit geben, eine zufällige Karte zu erstellen.

- HumanPlayer, Kommunikation: Für die Online-Variante des Spiels muss man sich noch ausdenken, auf welchem Port das Spiel Eingaben empfängt und wie die Architektur zum Schluss ist. Bisher war die Idee, dass ein Spieler der Host ist, auf dem die spiel-Instanz läuft. Die Eingabe selber ist aber wie bei allen anderen Spielern ein Client. 



### Entwicklungszyklus

- Tests sollen automatisiert werden. Ebenfalls sollte ein Weg gefunden werden, wie man die Tests auf anderen Systemen und Plattformen simuliert. 




