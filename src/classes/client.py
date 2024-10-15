import pickle
from datetime import datetime
class Client:

    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email
        self.card_id = None
        self.borrowed_books = []

# Knygos išduodamos tik tam tikram laikui, jeigu knygos negrąžinamos iki išduotos datos, jos skaitomos vėluojančiomis (angl. Overdue).
    def has_overdue_books(self):
        now = datetime.now()
        for borrowed in self.borrowed_books:
            due_date = borrowed['due_date']
            is_overdue = due_date < now
            if is_overdue:
                return True
        return False

    def __str__(self):
        return f"Kortelės ID: {self.card_id}. Skaitytojas: {self.name} {self.surname}, el. paštas: {self.email}\n"

class Readers:
    def __init__(self):
        self.readerlist = []
        self.current_card_id = 1

    def save_client(self, filename="src/lists/lib_clients.pickle"):
        with open(filename, "wb") as f:
            pickle.dump((self.readerlist, self.current_card_id), f)
        # print("Klientų sąrašas išsaugotas.")

    def load_clients(self, filename="src/lists/lib_clients.pickle"):
        try:
            with open(filename, "rb") as f:
                self.readerlist, self.current_card_id = pickle.load(f)
            # print("Klientų sąrašas įkeltas.")
        except (FileNotFoundError, EOFError):
            print("Klientų failas nerastas arba tuščias, todėl inicijuotas jo sukūrimas.")

# Knygas galima pasiimti tik su skaitytoje kortele, skaitytojo korteles reikia galėti užregistruoti ir priskirti naudotojui.
    def add_client(self):
        name = input("Įveskite vardą: ")
        surname = input("Įveskite pavardę: ")
        email = input("Įveskite el. paštą: ")
        new_client = Client(name, surname, email)
        new_client.card_id = f"{self.current_card_id:07d}"
        self.current_card_id += 1
        self.readerlist.append(new_client)
        self.save_client()
        print(f"Skaitytojas užregistruotas: {new_client}")
        return new_client

    def show_clients(self):
        if not self.readerlist:
            print("Bibliotekoje nėra registruotų skaitytojų.")
        else:
            for client in self.readerlist:
                print(client)

    def search_client(self, keyword):
        for client in self.readerlist:
            if (keyword.lower() in client.surname.lower() or
                keyword.lower() in client.email.lower() or
                keyword in client.card_id):
                print(f"Rastas skaitytojas su '{keyword}':\n{client}")
                return client
        print(f"Nerasta skaitytojo su '{keyword}'.\n")
        return None

# Turi būti galima peržiūrėti visas vėluojančias knygas   
    def show_all_overdue_books(self):
        now = datetime.now()
        has_overdues = False
        for client in self.readerlist:
            overdue_books = []
            for borrowed in client.borrowed_books:
                if borrowed['due_date'] < now:
                    overdue_books.append(borrowed)
            if overdue_books:
                has_overdues = True
                print(f"Skaitytojas: {client.name} {client.surname}, Kortelės ID: {client.card_id}")
                for borrowed in overdue_books:
                    book = borrowed['book']
                    due_date = borrowed['due_date']
                    print(f"  - Knyga: {book.name}, Grąžinimo data: {due_date.date()}")
        if not has_overdues:
            print("Šiuo metu nėra vėluojančių knygų.")