from classes.book import Book,Library # nereikia priekyje taško, nes eisim į gylį (iš main perspektyvos)

library = Library()

library.load_books()

while True:
    action = input("Pasirinkite veiksmą: 1 - Pridėti knygą, 2 - Pašalinti knygą, 3 - Rodyti knygas, 0 - Išeiti:\n")
    if action == "1":
        library.add_book()
        library.save_books()
    elif action == "2":
        ...
    elif action == "0":
        break
    else:
        print("Netinkamas pasirinkimas!")