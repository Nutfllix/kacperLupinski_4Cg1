import json
import os

PLIK = "sklep.json"

DANE_STARTOWE = [
    {"nazwa": "mleko", "kategoria": "nabiał", "cena": 3.50, "ilosc": 10},
    {"nazwa": "chleb", "kategoria": "pieczywo", "cena": 4.20, "ilosc": 5},
    {"nazwa": "ser", "kategoria": "nabiał", "cena": 12.99, "ilosc": 0},
    {"nazwa": "jabłko", "kategoria": "owoce", "cena": 2.10, "ilosc": 20},
    {"nazwa": "masło", "kategoria": "nabiał", "cena": 7.80, "ilosc": 0},
]


def zapisz_dane(produkty):
    with open(PLIK, "w", encoding="utf-8") as f:
        json.dump(produkty, f, ensure_ascii=False, indent=4)


def wczytaj_dane():
    # Jeśli pliku nie ma, tworzymy go z danymi startowymi
    if not os.path.exists(PLIK):
        zapisz_dane(DANE_STARTOWE)
        return list(DANE_STARTOWE)
    try:
        with open(PLIK, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Błąd odczytu pliku - przywracam dane startowe")
        zapisz_dane(DANE_STARTOWE)
        return list(DANE_STARTOWE)


produkty = wczytaj_dane()


def wyswietl_produkt(p):
    print(f"{p['nazwa']} | {p['kategoria']} | {p['cena']:.2f} zł | {p['ilosc']} szt.")


def wszystkie_produkty():
    print("\n--- Wszystkie produkty ---")
    for p in produkty:
        wyswietl_produkt(p)


def dostepne_produkty():
    print("\n--- Dostępne produkty ---")
    for p in produkty:
        if p["ilosc"] == 0:
            continue
        wyswietl_produkt(p)


def wyszukaj_produkt():
    szukana = input("Podaj produkt: ").lower()
    znaleziono = False
    for p in produkty:
        if p["nazwa"].lower() == szukana:
            wyswietl_produkt(p)
            znaleziono = True
            break
    if not znaleziono:
        print("Nie znaleziono produktu")


def produkty_do_ceny():
    try:
        max_cena = float(input("Podaj maksymalną cenę: "))
    except ValueError:
        print("Błędna cena - podaj liczbę")
        return
    znaleziono = False
    print(f"\n--- Produkty do {max_cena:.2f} zł ---")
    for p in produkty:
        if p["cena"] <= max_cena:
            wyswietl_produkt(p)
            znaleziono = True
    if not znaleziono:
        print("Brak produktów spełniających warunek")


def kup_produkt():
    nazwa = input("Podaj produkt: ").lower()
    znaleziono = False
    for p in produkty:
        if p["nazwa"].lower() == nazwa:
            znaleziono = True
            if p["ilosc"] == 0:
                print("Produkt niedostępny")
            else:
                p["ilosc"] -= 1
                zapisz_dane(produkty)
                print(f"Kupiono {p['nazwa']}")
                print(f"Pozostało sztuk: {p['ilosc']}")
            break
    if not znaleziono:
        print("Nie znaleziono produktu")


# ----- Menu główne -----
while True:
    print("\n===== MENU =====")
    print("1 - Wszystkie produkty")
    print("2 - Dostępne produkty")
    print("3 - Wyszukaj produkt")
    print("4 - Produkty do podanej ceny")
    print("5 - Kup produkt")
    print("0 - Zakończ program")

    try:
        wybor = int(input("Wybierz opcję: "))
    except ValueError:
        print("Wybrano złą opcję")
        continue

    if wybor == 1:
        wszystkie_produkty()
    elif wybor == 2:
        dostepne_produkty()
    elif wybor == 3:
        wyszukaj_produkt()
    elif wybor == 4:
        produkty_do_ceny()
    elif wybor == 5:
        kup_produkt()
    elif wybor == 0:
        print("Koniec programu")
        break
    else:
        print("Wybrano złą opcję")