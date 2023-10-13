"""Eine (Spiel-)Karte dient der Zuordnung des Namens, Bonussymbols, der Region, sowie der Häfen und Burgen
zu einem Gebiet. """

class karte:

    id_counter = 0
    """Eine Karte besteht aus den folgenden Informationen:

    int id          : id zugehöriger region
    string name     : name der region
    int bonus       : 1 Reiter, 2 Katapult, 3 Turm
    """
    def __init__(self, name: str, bonus: int) -> None:

        self.id       = self.id_counter
        self.name     = name
        self.bonus    = bonus

        type(self).id_counter += 1

    def karten_reset(self):
        type(self).id_counter = 0