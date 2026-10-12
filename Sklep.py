import sqlite3

polaczenie = sqlite3.connect("sklep.db")
kursor = polaczenie.cursor()

# Tworzenie tabeli
kursor.execute("""
    CREATE TABLE IF NOT EXISTS produkty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazwa TEXT NOT NULL,
        kategoria TEXT NOT NULL,
        cena REAL NOT NULL,
        ilosc INTEGER NOT NULL
    )
""")

# Dane startowe (tylko jeśli tabela jest pusta)
kursor.execute("SELECT COUNT(*) FROM produkty")
if kursor.fetchone()[0] == 0:
    kursor.executemany(
        "INSERT INTO produkty (nazwa, kategoria, cena, ilosc) VALUES (?, ?, ?, ?)",
        [
            ("mleko", "nabiał", 3.50, 10),
            ("chleb", "pieczywo", 4.20, 5),
            ("ser", "nabiał", 12.99, 0),
            ("jabłko", "owoce", 2.10, 20),
            ("masło", "nabiał", 7.80, 0),
        ],
    )
    polaczenie.commit()


def pobierz_wszystkie():
    kursor.execute("SELECT nazwa, kategoria, cena, ilosc FROM produkty")
    return kursor.fetchall()


def wyswietl_produkt(p):
    nazwa, kategoria, cena, ilosc = p
    print(f"{nazwa} | {kategoria} | {cena:.2f} zł | {ilosc} szt.")


def wszystkie_produkty():
    print("\n--- Wszystkie produkty ---")
    for p in pobierz_wszystkie():
        wyswietl_produkt(p)


def dostepne_produkty():
    print("\n--- Dostępne produkty ---")
    for p in pobierz_wszystkie():
        if p[3] == 0:
            continue
        wyswietl_produkt(p)


def wyszukaj_produkt():
    szukana = input("Podaj produkt: ").lower()
    znaleziono = False
    for p in pobierz_wszystkie():
        if p[0].lower() == szukana:
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
    for p in pobierz_wszystkie():
        if p[2] <= max_cena:
            wyswietl_produkt(p)
            znaleziono = True
    if not znaleziono:
        print("Brak produktów spełniających warunek")


def kup_produkt():
    nazwa = input("Podaj produkt: ").lower()
    znaleziono = False
    kursor.execute("SELECT id, nazwa, ilosc FROM produkty")
    for id_produktu, nazwa_bazy, ilosc in kursor.fetchall():
        if nazwa_bazy.lower() == nazwa:
            znaleziono = True
            if ilosc == 0:
                print("Produkt niedostępny")
            else:
                kursor.execute(
                    "UPDATE produkty SET ilosc = ilosc - 1 WHERE id = ?",
                    (id_produktu,),
                )
                polaczenie.commit()
                print(f"Kupiono {nazwa_bazy}")
                print(f"Pozostało sztuk: {ilosc - 1}")
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

polaczenie.close()