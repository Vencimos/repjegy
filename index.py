from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# Enum osztály létrehozása
class JaratTipusok(Enum):
    BELFOLDI = "Belföldi"
    NEMZETKOZI = "Nemzetközi"
    
setJaratszamok = set()
listLegitarsasagok = []

# Alapvető absztrakt osztály
class Jarat(ABC):
    def __init__(self, legitarsasag_kod, jaratszam, celallomas, jegyar, tipus = JaratTipusok.BELFOLDI):
        self.tipus = tipus
        self.legitarsasag_kod = legitarsasag_kod
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        
        setJaratszamok.add(self.legitarsasag_kod+self.jaratszam)

    @abstractmethod
    def getJaratTipus(self):
        pass

    def teljes_azonosito(self):
        return f"{self.legitarsasag_kod}{self.jaratszam}"
    
class BelfoldiJarat(Jarat):
    def getJaratTipus(self):
        return self.tipus.value

class NemzetkoziJarat(Jarat):
    def getJaratTipus(self):
        return self.tipus.value

class LegiTarsasag:
    def __init__(self, nev, kod):
        self.nev = kod
        self.nev = nev
        self.jaratok = []

    def addJarat(self, jarat):
        self.jaratok.append(jarat)

    def getJaratok(self):
        return self.jaratok

class JegyFoglalas:
    def __init__(self, jarat, utas_nev, datum):
        self.jarat = jarat
        self.utas_nev = utas_nev
        self.datum = datum

    def __str__(self):
        return f"Foglalás: {self.utas_nev} - {self.jarat.legitarsasag_kod}{self.jarat.jaratszam} ({self.jarat.celallomas}) - {self.datum} - {self.jarat.getJaratTipus()} - {self.jarat.jegyar} Ft"

class FoglalasiRendszer:
    def __init__(self):
        self.foglalasok = []

    def jegy_foglalas(self, jaratszam, utas_nev, datum):
        if jaratszam not in setJaratszamok:
            print("Hiba: A megadott járat nem található.")
            return None
        jarat = next((k for j in listLegitarsasagok for k in j.getJaratok() if k.legitarsasag_kod + k.jaratszam == jaratszam), None)
        if not jarat:
            print("Hiba: A megadott járat nem található.")
            return None
        foglalas = JegyFoglalas(jarat, utas_nev, datum)
        self.foglalasok.append(foglalas)
        print(f"Sikeres foglalás! Ár: {jarat.jegyar} Ft")
        return foglalas

    def foglalas_lemondasa(self, utas_nev, jaratszam):
        for foglalas in self.foglalasok:
            if foglalas.utas_nev == utas_nev and foglalas.jarat.legitarsasag_kod + foglalas.jarat.jaratszam == jaratszam:
                self.foglalasok.remove(foglalas)
                print("Sikeresen lemondta a foglalást.")
                return True
        print("Hiba: Nem található foglalás ezzel a névvel és járatszámmal.")
        return False

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            print("Nincs elérhető foglalás.")
        for foglalas in self.foglalasok:
            print(foglalas)

# Rendszer inicializálása
listLegitarsasagok.append(LegiTarsasag("MA", "123"))
listLegitarsasagok.append(LegiTarsasag("BA", "456"))

jarat1 = BelfoldiJarat("HA" , "123", "Budapest", 5000)
jarat2 = BelfoldiJarat("HA" , "234", "Debrecen", 4500)
jarat3 = NemzetkoziJarat("WZ", "900", "London", 35000, JaratTipusok.NEMZETKOZI)
jarat4 = NemzetkoziJarat("WZ", "945", "New York", 350000, JaratTipusok.NEMZETKOZI)

listLegitarsasagok[0].addJarat(jarat1)
listLegitarsasagok[0].addJarat(jarat2)
listLegitarsasagok[0].addJarat(jarat3)
listLegitarsasagok[1].addJarat(jarat4)

rendszer = FoglalasiRendszer()

# Előre betöltött foglalások
rendszer.jegy_foglalas("HA123", "Kovács Péter", "2024-11-22")
rendszer.jegy_foglalas("HA234", "Nagy Anna", "2024-11-23")
rendszer.jegy_foglalas("WZ900", "Tóth Balázs", "2024-11-24")
rendszer.jegy_foglalas("WZ945", "Szabó Eszter", "2024-11-24")
rendszer.jegy_foglalas("HA123", "Molnár Dániel", "2024-11-25")
rendszer.jegy_foglalas("HA234", "Varga Katalin", "2024-11-26")

# Felhasználói interfész
while True:
    print("\n--- Légitársaság Foglalási Rendszer ---")
    print("1. Jegy foglalása")
    print("2. Foglalás lemondása")
    print("3. Foglalások listázása")
    print("4. Kilépés")
    valasztas = input("Válasszon egy lehetőséget: ")

    if valasztas == "1":
        jaratszam = input("Adja meg a járatszámot: ")
        utas_nev = input("Adja meg az utas nevét: ")
        datum = input("Adja meg a dátumot (YYYY-MM-DD): ")
        try:
            datetime.strptime(datum, "%Y-%m-%d")  # Érvényesség ellenőrzése
            rendszer.jegy_foglalas(jaratszam, utas_nev, datum)
        except ValueError:
            print("Hiba: Érvénytelen dátumformátum.")

    elif valasztas == "2":
        utas_nev = input("Adja meg az utas nevét: ")
        jaratszam = input("Adja meg a járatszámot: ")
        rendszer.foglalas_lemondasa(utas_nev, jaratszam)

    elif valasztas == "3":
        rendszer.foglalasok_listazasa()

    elif valasztas == "4":
        print("Kilépés a rendszerből. Viszontlátásra!")
        break

    else:
        print("Hiba: Érvénytelen választás.")
