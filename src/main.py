from classes.book import Book,Library # nereikia priekyje taško, nes eisim į gylį (iš main perspektyvos)
from classes.client import Client, Readers

library = Library()
library.load_books()
client = Readers()
client.load_clients

while True:
    action = input("Pasirinkite veiksmą: 1 - Pridėti knygą, 2 - Pašalinti knygą, 3 - Rodyti knygas, 4 - ieškoti knygų, 5 - Išduoti knygą, 6 - Grąžinti knygą, 0 - Išeiti:\n")
    if action == "1":
        library.add_book()
        library.save_books()
    elif action == "2":
        library.remove_book()
        library.save_books()
    elif action == "3":
        library.show_books()
    elif action == "4":
        keyword = input("Įveskite paieškos frazę (autorių arba knygos pavadinimą): ")
        library.search_books(keyword)
    elif action == "5":
        book_name = input("Įveskite knygos pavadinimą: ")
        Client.borrow_book(book_name, library)
    elif action == "0":
        break
    else:
        print("Netinkamas pasirinkimas!")