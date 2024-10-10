# knyga privalo turėti bent autorių, pavadinimą, išleidimo metus ir žanrą
class Book:
    def __init__(self, author: str, name: str, pub_year: int, genre: str):
        self.author = author
        self.name = name
        self.year = pub_year
        self.genre = genre
    
    # Turėtų būti galima pridėti naują į knygą į biblioteką
    def add_book(books: list):
        author = input("Autorius: ")
        name = input("Knygos pavadinimas: ")
        pub_year = input("Leidimo metai: ")
        genre = input("Žanras: ")
        book = Book(author,name,pub_year,genre)
        book.append(book)