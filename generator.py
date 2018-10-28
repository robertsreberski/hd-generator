from utils import *
from classes import *
from mimesis import Person
from mimesis import Address
from mimesis import Business
from random import randint
from collections import OrderedDict
import os.path
import time
import random
import datetime
import uuid
import json

person = Person()
address = Address()
business = Business()


hotele = {}
goscie_hotelowi = {}
uslugi = {}
opcje_pobytu = {}
cenniki_uslug = {}
karty_hotelowe = {}
pobyty = {}
zamowienia_uslugi = {}
ankiety = {}

def generujHotele(ilosc):
    for x in range(0, ilosc):
        hotel_id = uuid.uuid4()
        hotele[hotel_id] = Hotel(
            ID=hotel_id,
            Nazwa=business.company(),
            Adres=address.address()
        )


def generujOpcjePobytu(zdefiniowane):
    for typ in zdefiniowane:
        opcje_pobytu[typ] = OpcjaPobytu(
            Typ=typ
        )


def generujGoscieHotelowi(ilosc, date_max):
    for x in range(0, ilosc):
        PESEL = uuid.uuid4()
        goscie_hotelowi[PESEL] = GoscHotelowy(
            PESEL=PESEL,
            Imie=person.name(),
            Nazwisko=person.surname(),
            KrajPochodzenia=person.nationality(),
            DataUrodzenia=get_random_date(
                min=datetime.date(1950, 1, 1),
                max=date_max
            ),
            _Pobyty=[]
        )


def generujUslugi(ilosc, hotel_id, typy_uslug):
    for x in range(0, ilosc):
        usluga_id = uuid.uuid4()
        uslugi[usluga_id] = Usluga(
            ID=usluga_id,
            Typ=random.choice(typy_uslug),
            Nazwa=business.company(),
            HotelID=hotel_id
        )


def get_random_cena():
    return round(random.uniform(0, 1000), 2)


def generujCennikiUslug(min_date, max_date, usluga_id):
    for opcja_pobytu_id in list(opcje_pobytu.keys()):
        start = min_date
        end = get_random_date(start+datetime.timedelta(days=1), max_date)
        while (start != end):
            cennik_id = uuid.uuid4()
            cenniki_uslug[cennik_id] = CennikUslugi(
                ID=cennik_id,
                Cena=get_random_cena(),
                DataRozpoczecia=start,
                DataZakonczenia=end,
                OpcjaPobytuID=opcja_pobytu_id,
                UslugaID=usluga_id
            )
            start = end
            diff = max_date - start
            if (diff.days == 0):
                break
            elif diff.days < 60:
                end = max_date
            else:
                end = get_random_date(start+datetime.timedelta(days=1), max_date)


def generujKartyHotelowe(min_date, max_date, ilosc):
    for x in range(0, ilosc):
        date = get_random_date(min_date, max_date)
        karta_id = uuid.uuid4()
        karty_hotelowe[karta_id] = KartaHotelowa(
            ID=karta_id,
            DataWydania=date,
            DataZwrotu=date + datetime.timedelta(days=random.randint(1, 14)),
            OpcjaPobytuID=random.choice(list(opcje_pobytu.keys())),
            HotelID=random.choice(list(hotele.keys()))
        )


def getGoscForPobyt(karta_hotelowa_id):
    gosc = random.choice(list(goscie_hotelowi.values()))

    if len(gosc._Pobyty) == 0:
        return gosc.PESEL

    czyLosowacNowegoGoscia = False
    goscNiepoprawny = True




    while goscNiepoprawny:
        for pobyt_id in gosc._Pobyty:
            karta_hotelowa_stary_pobyt = karty_hotelowe.get(pobyty[pobyt_id].KartaHotelowa)
            karta_hotelowa_nowy_pobyt = karty_hotelowe.get(karta_hotelowa_id)
            if karta_hotelowa_stary_pobyt.HotelID == karta_hotelowa_nowy_pobyt.HotelID:
                if not (
                        karta_hotelowa_nowy_pobyt.DataZwrotu <= karta_hotelowa_stary_pobyt.DataWydania or karta_hotelowa_nowy_pobyt.DataWydania >= karta_hotelowa_nowy_pobyt.DataZwrotu):
                    czyLosowacNowegoGoscia = True
                    break
        if czyLosowacNowegoGoscia:
            gosc = random.choice(list(goscie_hotelowi.values()))
            czyLosowacNowegoGoscia = False
        else:
            goscNiepoprawny = False



    return gosc.PESEL


def generujPobyty(ilosc, karta_hotelowa_id):
    for x in range(0, ilosc):
        pobyt_id = uuid.uuid4()
        gosc_id = getGoscForPobyt(karta_hotelowa_id)

        gosc = goscie_hotelowi[gosc_id]
        gosc._Pobyty.append(pobyt_id)

        pobyty[pobyt_id] = Pobyt(
            _ID=pobyt_id,
            KartaHotelowaID=karta_hotelowa_id,
            GoscHotelowyID=gosc_id
        )


def get_cennik_for_zamowienie(date, opcja_pobytu):
    _cenniki = list(filter(
        lambda temp: temp.DataRozpoczecia <= date <= temp.DataZakonczenia and temp.OpcjaPobytu == opcja_pobytu,
        list(cenniki_uslug.values())
    ))

    return random.choice(_cenniki).ID


def generujZamowieniaUslug(ilosc, karta_hotelowa_id, max_date):
    karta_hotelowa = karty_hotelowe.get(karta_hotelowa_id)
    min_date = karta_hotelowa.DataWydania

    if karta_hotelowa.DataZwrotu <= max_date:
        max_date = karta_hotelowa.DataZwrotu

    for x in range(0, ilosc):
        start = get_random_date(min_date, max_date)
        zamowienie_id = uuid.uuid4()
        zamowienia_uslugi[zamowienie_id] = ZamowienieUslugi(
            _ID=zamowienie_id,
            KartaHotelowaID=karta_hotelowa_id,
            CennikUslugiID=get_cennik_for_zamowienie(start, karta_hotelowa.OpcjaPobytu),
            DataRozpoczecia=start,
            DataZakonczenia=get_random_date(start, max_date),
            Oplacone=random.randint(0, 1)
        )


def generujAnkiete(karta_hotelowa_id, data, opcje_uslug):
    if randint(0, 100) <= 66:
        return
    plec = ['M', 'F']
    jakosc_uslug = list(map(lambda x: randint(0, 10), opcje_uslug))

    ankieta = {
        'data': data.strftime('%Y-%m-%d'),
        'plec': random.choice(plec),
        'wiek': randint(18,100),
        'sugestie': 'lorem ipsum',
        'oceny': {
            'zadowolenieZPobytu': randint(0, 10),
            'czystoscPokoju': randint(0,10),
            'wyposazeniePokoju': randint(0, 10),
            'czystoscLazienki': randint(0, 10),
            'jakosc': dict(zip(opcje_uslug, jakosc_uslug))
        }
    }
    ankiety[str(karta_hotelowa_id)] = ankieta



def single(title, body):
    print("{title}...".format(title=title), end=' ', flush=True)
    start_time = time.time()
    count = body()
    elapsed_time = time.time() - start_time
    print("Zakończone; czas: {czas}s; ilość: {ilosc}".format(czas=elapsed_time, ilosc=count))



def generuj(N, t1, t2, opcje_uslug):
    print("Rozpoczynanie generowania; daty: poczatek={t1}, koniec={t2}".format(t1=t1, t2=t2))

    def stage1():
        ilosc = N*3
        generujGoscieHotelowi(ilosc=ilosc, date_max=(t1 - datetime.timedelta(days=365 * 10)))
        return ilosc

    def stage2():
        opcje = ['ALL-INCLUSIVE', 'BRONZE', 'SILVER', 'GOLD']
        generujOpcjePobytu(opcje)
        return len(opcje)

    def stage3():
        ilosc = random.randint(1, 50)
        generujHotele(ilosc)
        return ilosc

    def stage4():
        sum = 0
        for id in hotele:
            ilosc = random.randint(5, 25)
            sum += ilosc
            generujUslugi(
                ilosc=ilosc,
                hotel_id=id,
                typy_uslug=opcje_uslug
            )
        return sum

    def stage5():
        for id in uslugi:
            generujCennikiUslug(
                min_date=t1,
                max_date=t2,
                usluga_id=id
            )
        return len(uslugi) * 4

    def stage6():
        generujKartyHotelowe(min_date=t1, max_date=t2, ilosc=N)
        return N

    def stage7():
        sum = 0
        for id in karty_hotelowe:
            ilosc = random.randint(1, 5)
            sum += ilosc
            generujPobyty(
                ilosc=ilosc,
                karta_hotelowa_id=id
            )
        return sum

    def stage8():
        sum = 0
        for id in karty_hotelowe:
            ilosc = random.randint(1, 10)
            sum += ilosc
            generujZamowieniaUslug(
                ilosc=ilosc,
                karta_hotelowa_id=id,
                max_date=t2
            )
        return sum

    def stage9():
        for karta in karty_hotelowe.values():
            generujAnkiete(karta.ID, karta.DataZwrotu, opcje_uslug)

        prev_data = {}
        if os.path.exists("ankiety.json"):
            with open("ankiety.json") as json_file:
                prev_data = json.load(json_file)

        if len(prev_data) > 0:
            ankiety.update(prev_data)

        with open("ankiety.json", "w") as write_file:
            json.dump(ankiety, write_file, indent=4, sort_keys=True)
        return N

    mapping_tuples = [
        ("Generowanie Gości Hotelowych", stage1),
        ("Generowanie Opcji Pobytu", stage2),
        ("Generowanie Hoteli", stage3),
        ("Generowanie Usług", stage4),
        ("Generowanie Cenników Usług", stage5),
        ("Generowanie Kart Hotelowych", stage6),
        ("Generowanie Zamówień Usług", stage8),
        ("Generowanie Pobytów", stage7),
        ("Generowanie Ankiet", stage9),
    ]
    mapping = OrderedDict(mapping_tuples)
    for title, body in mapping.items():
        single(
            title=title,
            body=body
        )

    return {
        "GoscHotelowy": goscie_hotelowi,
        "OpcjaPobytu": opcje_pobytu,
        "Hotel": hotele,
        "Usluga": uslugi,
        "CennikUslugi": cenniki_uslug,
        "KartaHotelowa": karty_hotelowe,
        "ZamowienieUslugi": zamowienia_uslugi,
        "Pobyt": pobyty
    }

