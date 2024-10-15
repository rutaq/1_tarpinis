import pickle
# from pathlib import Path
# knyga privalo turėti bent autorių, pavadinimą, išleidimo metus ir žanrą
class Book:
    def __init__(self, author: str, name: str, pub_year: int, genre: str, isbn: int, lib_id, quantity: int = 1):
        self.author = author
        self.name = name
        self.year = pub_year
        self.genre = genre
        self.n = quantity if quantity is not None else 0
        self.isbn = isbn
        self.lib_id = lib_id  # Unikalus bibliotekos numeris, jei nėra ISBN
        self.isbn_or_id = self.isbn if self.isbn else (self.lib_id if self.lib_id else "Neturi ID")
    
    def __str__(self):
        return f'{self.isbn_or_id}. {self.author} "{self.name}", {self.year} ({self.genre}) - {self.n} vnt.'
class Library:
    def __init__(self):
        self.booklist = []

    # Turėtų būti galima pridėti naują į knygą į biblioteką
    def add_book(self):
        author = input("Autorius: ")
        name = input("Knygos pavadinimas: ")
        pub_year = input("Leidimo metai: ")
        genre = input("Žanras: ")
        isbn = input("ISBN (jeigu nėra, spauskite 'Enter'): ")
        lib_id = None
        if isbn == "":
            lib_id = input("Unikalus bibliotekos numeris: ")
        while True:
            quantity = input("Kiekis (jeigu paspausite 'Enter', automatiškai bus priskirtas kiekis '1'): ")
            if quantity == "":
                quantity = None
                break
            elif quantity.isdecimal():
                quantity = int(quantity)
                break
            else:
                print("Įvesta neteisinga kiekio reikšmė. Prašome įvesti sveikąjį skaičių.")

        book = Book(author,name,pub_year,genre,isbn,lib_id,quantity)
        self.booklist.append(book)
        print("Knyga sėkmingai pridėta į biblioteką.")

    def save_books(self, filename="1_tarpinis/lists/lib_books.pickle"):
        # kadangi filename = "lists/lib_books.pickle" kelias neveikia nei taip, nei ../, nei r"..." būdais, nei perėjus iš Poetry virtualios aplinkos į standartinę virtualią aplinką, ir tam sugaišau daugiau nei dvi valandas, toliau panaudotas ChatGPT pasiūlytas veikiantis sprendimas."
        # Nustatome absoliutų kelią pagal dabartinę failo vietą
        # project_root = Path(__file__).resolve().parent.parent  # Nustatome projekto šaknį
        # filepath = project_root / "lists" / filename  # Sukuriame absoliutų kelią
        # with open(filepath, "wb") as f:
        #     pickle.dump(self.booklist, f)
        with open(filename, "wb") as f:
            pickle.dump(self.booklist, f)

    def load_books(self, filename="1_tarpinis/lists/lib_books.pickle"):
        # Nustatome absoliutų kelią pagal dabartinę failo vietą
        # project_root = Path(__file__).resolve().parent.parent  # Nustatome projekto šaknį
        # filepath = project_root / "lists" / filename  # Sukuriame absoliutų kelią
        try:
            # with open(filepath, "rb") as f:
            #     self.booklist = pickle.load(f)
            with open(filename, "rb") as f:
                self.booklist = pickle.load(f)
            print("Bibliotekos knygų sąrašas pakrautas iš failo.")
        except (FileNotFoundError, EOFError):
            print("Failas nerastas arba tuščias.")

# Turėtų būti galima pašalinti senas/nebenaudojamas knygas (konkretų kiekį), galima daryti pagal išleidimo metus, jeigu senesnis nei x išmetam.
    def remove_book(self):
        id = input("Įveskite knygos ISBN arba bibliotekos numerį: ")
        for book in self.booklist:
            if book.isbn == id or book.lib_id == id:
                print(f'Knyga rasta: "{book.name}". Esamų egzempliorių kiekis: {book.n}')
                while True:
                    try:
                        remove_n = int(input(f"Įveskite kiekį, kurį norite pašalinti (maksimalus: {book.n}): "))
                        if remove_n > book.n:
                            print(f"Klaida: negalima pašalinti daugiau egzemplių nei yra ({book.n}).")
                        else:
                            break
                    except ValueError:
                        print("Neteisinga įvestis. Prašome įvesti sveikąjį skaičių.")
                
                book.n -= remove_n
                print(f'Pašalinta {remove_n} vnt. knygos "{book.name}". Liko: {book.n} vnt.')
                
                if book.n == 0:
                # Būsimas funkcionalumas: patikrinti, ar nėra išduotų egzempliorių
                # issued_copies = check_if_issued(book)

                # Patvirtinimas iš vartotojo
                    confirm = input(f"Knyga '{book.name}' nebeturi egzempliorių. Ar norite visiškai ištrinti knygą iš bibliotekos knygų sąrašo? (taip/ne): ")
                    if confirm.lower() == "taip":
                        self.booklist.remove(book)
                        print(f"Knyga '{book.name}' visiškai pašalinta.")
                    else:
                        print(f"Knyga '{book.name}' nebuvo pašalinta.")
            return
            # Jei return nebūtų, ciklas pereitų prie kitos knygos, net jei buvo rasta ir apdorota knyga.
        else:
            print(f"Knyga su nurodytu ISBN arba unikaliu bibliotekos numeriu '{id}' nerasta.")

    # Turi būti galima peržiūrėti visas bibliotekos knygas
    def show_books(self):
        if not self.booklist:
            print("Bibliotekoje šiuo metu nėra knygų.")
        else:
            # table_len = 108
            # col_width = table_len/6
            # formatavimas = f"|{{st1:^{col_width}}}|{{st2:^{col_width}}}|{{st3:^{col_width}}}|{{st4:^{col_width}}}|{{st5:^{col_width}}}|{{st6:^{col_width}}}|"
            # st1, st2,st3,st4,st5,st6 = "Autorius","Pavadinimas","Leidimo metai","Žanras", "ISBN/Bibliotekos nr.","Kiekis"
            # print("-" * table_len)
            # print(formatavimas.format(st1=st1, st2=st2,st3=st3,st4=st4,st5=st5,st6=st6))
            # print("-" * table_len)
            # for book in self.booklist:
            #     st1, st2, st3, st4, st5, st6 = (str(book.author), str(book.name), str(book.year), str(book.genre), str(book.isbn), str(book.n))
            # print(formatavimas.format(st1=st1, st2=st2, st3=st3, st4=st4, st5=st5, st6=st6))
            # print("-" * table_len)
            print("BIBLIOTEKOJE ESANČIŲ KNYGŲ SĄRAŠAS")
            for book in self.booklist:
                print(book)
    
    # Turėtų būti galimybė ieškoti knygų bibliotekoje, pagal knygos pavadinimą arba autorių.
    def search_books(self, keyword):
        results = []
        for book in self.booklist:
            if keyword.lower() in book.name.lower() or keyword.lower() in book.author.lower():
                results.append(book)
        if results:
            print(f"Rasta(-os) knyga(-os) su '{keyword}':")
            for book in results:
                print(book)
        else:
            print(f"Nerasta knygų su '{keyword}'.\n")