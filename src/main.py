from classes.book import Library # nereikia priekyje taško, nes eisim į gylį (iš main perspektyvos)
from classes.client import Readers
from classes.service import Service

library = Library()
library.load_books()
readers = Readers()
readers.load_clients()
service = Service(library, readers)

while True:
    action = input("Pasirinkite veiksmą: 1 - Pridėti knygą, 2 - Pašalinti knygą, 3 - Rodyti knygas, 4 - ieškoti knygų, 5 - Išduoti knygą, 6 - Grąžinti knygą, 7 - Peržiūrėti vėluojamas atiduoti knygas, 0 - Išeiti:\n")
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
        client_keyword = input("Įveskite skaitytojo kortelės ID, pavardę arba el. paštą: ")
        book_keyword = input("Įveskite knygos pavadinimą arba autorių: ")
        service.borrow_book(client_keyword, book_keyword)
    elif action == "6":
        client_keyword = input("Įveskite skaitytojo kortelės ID, pavardę arba el. paštą: ")
        book_keyword = input("Įveskite grąžinamos knygos pavadinimą arba autorių: ")
        service.return_book(client_keyword, book_keyword)
    elif action == "7":
        readers.show_all_overdue_books()
    elif action == "0":
        break
    else:
        print("Netinkamas pasirinkimas!")