import datetime
from classes.book import Library
from classes.client import Readers

class Service:
    def __init__(self, library, readers):
        self.library = library
        self.readers = readers

    def borrow_book(self, client_keyword, book_keyword, days_borrowed=30):
        client = self.readers.search_client(client_keyword)
        if not client:
            while True:
                add_client = input("Ar norite jį užregistruoti? (taip/ne): ").lower()
                if add_client == 'taip':
                    client = self.readers.add_client()
                    if not client:
                        print("Nepavyko pridėti skaitytojo.")
                        return
                    break
                elif add_client == 'ne':
                    print("Knyga neišduota, nes nėra skaitytojo.")
                    return
                else:
                    print("Nesupratau jūsų atsakymo. Prašome įvesti 'taip' arba 'ne'.")
        # Turi būti neleidžiama pasiimti knygos, jeigu skaitytojas turi vėluojančią knygą ir jis turi būti įspėtas, kad knyga vėluoja
        if client.has_overdue_books():
            print(f"Skaitytojas {client.name} {client.surname} turi vėluojančių knygų ir negali pasiimti naujų knygų.")
            return
        found_books = self.library.search_books(book_keyword)
        if found_books:
            for wanted_book in found_books:
                if wanted_book.n > 0:
                    wanted_book.n -= 1
                    due_date = datetime.datetime.now() + datetime.timedelta(days=days_borrowed)
                    client.borrowed_books.append({'book': wanted_book, 'due_date': due_date})
                    print(f"Knyga '{wanted_book.name}' išduota skaitytojui {client.name} {client.surname}. Grąžinimo data: {due_date.date()}")
                    self.library.save_books() 
                    self.readers.save_client()
                    return
                
            else:
                print(f"Knygos '{wanted_book.name}' šiuo metu nėra.")
                return
        else:
            print(f"Knyga su raktažodžiu '{book_keyword}' nerasta bibliotekoje.")
            return
        
    def return_book(self, client_keyword, book_keyword):
        client = self.readers.search_client(client_keyword)
        if not client:
            print(f"Skaitytojas su duomenimis '{client_keyword}' nerastas.")
            return

        for borrowed in client.borrowed_books:
            book = borrowed['book']
            if (book_keyword.lower() in book.name.lower() or
                book_keyword.lower() in book.author.lower()):
                client.borrowed_books.remove(borrowed)
                book.n += 1  # Padidiname knygos kiekį bibliotekoje
                self.library.save_books()
                self.readers.save_client()
                print(f"Knyga '{book.name}' grąžinta į biblioteką.")
                return
        print(f"Skaitytojas neturi knygos su pavadinimu arba autoriumi '{book_keyword}'.")