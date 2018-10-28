class GoscHotelowy:
    def __init__(self, PESEL, Imie, Nazwisko, KrajPochodzenia, DataUrodzenia, _Pobyty):
        self.PESEL = PESEL
        self.Imie = Imie
        self.Nazwisko = Nazwisko
        self.KrajPochodzenia = KrajPochodzenia
        self.DataUrodzenia = DataUrodzenia
        self._Pobyty = _Pobyty

    def bulk(self):
        return '{PESEL}|"{Imie}"|"{Nazwisko}"|"{KrajPochodzenia}"|"{DataUrodzenia}"'.format(
            PESEL=self.PESEL,
            Imie=self.Imie,
            Nazwisko=self.Nazwisko,
            KrajPochodzenia=self.KrajPochodzenia,
            DataUrodzenia=self.DataUrodzenia
        )


class Hotel:
    def __init__(self, ID, Adres, Nazwa):
        self.ID = ID
        self.Adres = Adres
        self.Nazwa = Nazwa

    def bulk(self):
        return "{ID}|{Adres}|{Nazwa}".format(
            ID=self.ID,
            Adres=self.Adres,
            Nazwa=self.Nazwa
        )


class OpcjaPobytu:
    def __init__(self, Typ):
        self.Typ = Typ

    def bulk(self):
        return "{Typ}".format(
            Typ=self.Typ
        )


class Usluga:
    def __init__(self, ID, Typ, Nazwa, HotelID):
        self.ID = ID
        self.Typ = Typ
        self.Nazwa = Nazwa
        self.Hotel = HotelID

    def bulk(self):
        return "{ID}|{Typ}|{Nazwa}|{Hotel}".format(
            ID=self.ID,
            Typ=self.Typ,
            Nazwa=self.Nazwa,
            Hotel=self.Hotel
        )


class CennikUslugi:
    def __init__(self, ID, Cena, DataRozpoczecia, DataZakonczenia, OpcjaPobytuID, UslugaID):
        self.ID = ID
        self.Cena = Cena
        self.DataRozpoczecia = DataRozpoczecia
        self.DataZakonczenia = DataZakonczenia
        self.OpcjaPobytu = OpcjaPobytuID
        self.Usluga = UslugaID

    def bulk(self):
        return "{ID}|{Cena}|{DataRozpoczecia}|{DataZakonczenia}|{OpcjaPobytu}|{Usluga}".format(
            ID=self.ID,
            Cena=self.Cena,
            DataRozpoczecia=self.DataRozpoczecia,
            DataZakonczenia=self.DataZakonczenia,
            OpcjaPobytu=self.OpcjaPobytu,
            Usluga=self.Usluga
        )


class KartaHotelowa:
    def __init__(self, ID, DataWydania, DataZwrotu, OpcjaPobytuID, HotelID):
        self.ID = ID
        self.HotelID = HotelID
        self.DataWydania = DataWydania
        self.DataZwrotu = DataZwrotu
        self.OpcjaPobytu = OpcjaPobytuID

    def bulk(self):
        return "{ID}|{Hotel}|{DataWydania}|{DataZwrotu}|{OpcjaPobytu}".format(
            ID=self.ID,
            Hotel=self.HotelID,
            DataWydania=self.DataWydania,
            DataZwrotu=self.DataZwrotu,
            OpcjaPobytu=self.OpcjaPobytu
        )


class Pobyt:
    def __init__(self, _ID, GoscHotelowyID, KartaHotelowaID):
        self._ID = _ID
        self.GoscHotelowy = GoscHotelowyID
        self.KartaHotelowa = KartaHotelowaID

    def bulk(self):
        return "{GoscHotelowy}|{KartaHotelowa}".format(
            GoscHotelowy=self.GoscHotelowy,
            KartaHotelowa=self.KartaHotelowa
        )


class ZamowienieUslugi:
    def __init__(self, _ID, KartaHotelowaID, CennikUslugiID, DataRozpoczecia, DataZakonczenia, Oplacone):
        self._ID = _ID
        self.KartaHotelowa = KartaHotelowaID
        self.CennikUslugi = CennikUslugiID
        self.DataRozpoczecia = DataRozpoczecia
        self.DataZakonczenia = DataZakonczenia
        self.Oplacone = Oplacone

    def bulk(self):
        return "{KartaHotelowa}|{CennikUslugi}|{DataRozpoczecia}|{DataZakonczenia}|{Oplacone}".format(
            KartaHotelowa=self.KartaHotelowa,
            CennikUslugi=self.CennikUslugi,
            DataRozpoczecia=self.DataRozpoczecia,
            DataZakonczenia=self.DataZakonczenia,
            Oplacone=self.Oplacone
        )