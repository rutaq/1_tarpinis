import sqlite3
conn = sqlite3.connect('src/lists/lib_books.db')
cursor = conn.cursor()

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
        return f'{self.isbn_or_id}. {self.author} "{self.name}", {self.year} ({self.genre}) - {self.n} vnt.\n'
    
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

        # book = Book(author,name,pub_year,genre,isbn,lib_id,quantity)
        # self.booklist.append(book)

        with conn:
            cursor.execute("""CREATE TABLE IF NOT EXISTS Books(
               ISBN_or_ID integer,
               Author text,
               Name text,
               Year integer,
               Genre text,
               Quantity integer)""")
        with conn:
            cursor.execute("""INSERT INTO Books(ISBN_or_ID,Author,Name,Year,Genre,Quantity) VALUES
                           (?,?,?,?,?,?)""", (isbn if isbn else lib_id, author, name, pub_year, genre, quantity))
        print("Knyga sėkmingai pridėta į biblioteką.")

    # def save_books(self, filename="src/lists/lib_books.db"):
        # kadangi filename = "lists/lib_books.pickle" kelias neveikia nei taip, nei ../, nei r"..." būdais, nei perėjus iš Poetry virtualios aplinkos į standartinę virtualią aplinką, ir tam sugaišau daugiau nei dvi valandas, toliau panaudotas ChatGPT pasiūlytas veikiantis sprendimas."
        # Nustatome absoliutų kelią pagal dabartinę failo vietą
        # project_root = Path(__file__).resolve().parent.parent  # Nustatome projekto šaknį
        # filepath = project_root / "lists" / filename  # Sukuriame absoliutų kelią
        # with open(filepath, "wb") as f:
        #     pickle.dump(self.booklist, f)


    # def load_books(self, filename="src/lists/lib_books.pickle"):
    #     try:
    #         with open(filename, "rb") as f:
    #             self.booklist = pickle.load(f)
    #     except (FileNotFoundError, EOFError):
    #         print("Failas nerastas arba tuščias.")

# Turėtų būti galima pašalinti senas/nebenaudojamas knygas (konkretų kiekį), galima daryti pagal išleidimo metus, jeigu senesnis nei x išmetam.
    def remove_book(self):
        isbn_id = input("Įveskite knygos ISBN arba bibliotekos numerį: ")
        # remove_n = int(input(f"Įveskite kiekį, kurį norite pašalinti (maksimalus: {book.n}): "))
        with conn:
            cursor.execute("DELETE from Books WHERE ISBN_or_ID = ?", (isbn_id,))
        print("Knyga sėkmingai ištrinta iš bibliotekos.")

        # for book in self.booklist:
        #     if book.isbn == id or book.lib_id == id:
        #         print(f'Knyga rasta: "{book.name}". Esamų egzempliorių kiekis: {book.n}')
        #         while True:
        #             try:
        #                 remove_n = int(input(f"Įveskite kiekį, kurį norite pašalinti (maksimalus: {book.n}): "))
        #                 if remove_n > book.n:
        #                     print(f"Klaida: negalima pašalinti daugiau egzemplių nei yra ({book.n}).")
        #                 else:
        #                     break
        #             except ValueError:
        #                 print("Neteisinga įvestis. Prašome įvesti sveikąjį skaičių.")
                
        #         book.n -= remove_n
        #         print(f'Pašalinta {remove_n} vnt. knygos "{book.name}". Liko: {book.n} vnt.')
                
        #         if book.n == 0:
        #         # Būsimas funkcionalumas: patikrinti, ar nėra išduotų egzempliorių
        #         # issued_copies = check_if_issued(book)

        #         # Patvirtinimas iš vartotojo
        #             confirm = input(f"Knyga '{book.name}' nebeturi egzempliorių. Ar norite visiškai ištrinti knygą iš bibliotekos knygų sąrašo? (taip/ne): ")
        #             if confirm.lower() == "taip":
        #                 self.booklist.remove(book)
        #                 print(f"Knyga '{book.name}' visiškai pašalinta.")
        #             else:
        #                 print(f"Knyga '{book.name}' nebuvo pašalinta.")
        #     return
        #     # Jei return nebūtų, ciklas pereitų prie kitos knygos, net jei buvo rasta ir apdorota knyga.
        # else:
        #     print(f"Knyga su nurodytu ISBN arba unikaliu bibliotekos numeriu '{id}' nerasta.")

    # Turi būti galima peržiūrėti visas bibliotekos knygas
    def show_books(self):
        # if not self.booklist:
        #     print("Bibliotekoje šiuo metu nėra knygų.")
        # else:
        print("BIBLIOTEKOJE ESANČIŲ KNYGŲ SĄRAŠAS")
        with conn:
            cursor.execute("SELECT * from Books")
            list = cursor.fetchall()
            for x in list:
                print(x)
    
    # Turėtų būti galimybė ieškoti knygų bibliotekoje, pagal knygos pavadinimą arba autorių.
    def search_books(self, keyword):
        keyword = '%' + keyword + '%'  # Paruošiame raktažodį LIKE užklausai
        with conn:
            cursor.execute("SELECT * FROM Books WHERE Author LIKE ? OR Name LIKE ?", (keyword, keyword))
            print(cursor.fetchall())


        # results = []
        # for book in self.booklist:
        #     if keyword.lower() in book.name.lower() or keyword.lower() in book.author.lower():
        #         results.append(book)
        # if results:
        #     print(f"Rasta(-os) knyga(-os) su '{keyword}':")
        #     for book in results:
        #         print(book)
        #     return results
        # else:
        #     print(f"Nerasta knygų su '{keyword}'.\n")
        #     return None