import pickle

# knyga privalo turėti bent autorių, pavadinimą, išleidimo metus ir žanrą
class Book:
    def __init__(self, author: str, name: str, pub_year: int, genre: str):
        self.author = author
        self.name = name
        self.year = pub_year
        self.genre = genre
    
    def __str__(self):
        return f'{self.author} "{self.name}", {self.year} ({self.genre})'
class Library:
    def __init__(self):
        self.booklist = []

    # Turėtų būti galima pridėti naują į knygą į biblioteką
    def add_book(self, books: list):
        author = input("Autorius: ")
        name = input("Knygos pavadinimas: ")
        pub_year = input("Leidimo metai: ")
        genre = input("Žanras: ")

        book = Book(author,name,pub_year,genre)
        self.booklist.append(book)
        print("Knyga sėkmingai pridėta į biblioteką.\n")

    def load_books(self, filename="lib_books.pickle"):
        try:
            with open(filename, "rb") as f:
                self.booklist = pickle.load(f)
            print("Bibliotekos knygų sąrašas pakrautas iš failo.")
        except (FileNotFoundError, EOFError):
            print("Failas nerastas arba tuščias.")