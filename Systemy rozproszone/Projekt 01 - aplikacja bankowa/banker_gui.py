import tkinter as tk
from tkinter import messagebox
import socket
import json

class BankerTerminal:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        self.client_socket.send(json.dumps(request).encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        return json.loads(response)

    def add_client(self, imie, nazwisko, pesel):
        request = {
            "operation": "add_client",
            "imie": imie,
            "nazwisko": nazwisko,
            "pesel": pesel
        }
        return self.send_request(request)

    def edit_client(self, nr_konta, imie=None, nazwisko=None, pesel=None):
        request = {
            "operation": "edit_client",
            "nr_konta": nr_konta,
            "imie": imie,
            "nazwisko": nazwisko,
            "pesel": pesel
        }
        return self.send_request(request)

    def delete_client(self, nr_konta):
        request = {
            "operation": "delete_client",
            "nr_konta": nr_konta
        }
        return self.send_request(request)

class BankerGUI:
    def __init__(self, root, banker_terminal):
        self.banker_terminal = banker_terminal
        self.root = root
        self.root.title("Terminal Bankiera")
        self.create_widgets()

    def create_widgets(self):
        self.imie_label = tk.Label(self.root, text="Imię")
        self.imie_label.pack()
        self.imie_entry = tk.Entry(self.root)
        self.imie_entry.pack()

        self.nazwisko_label = tk.Label(self.root, text="Nazwisko")
        self.nazwisko_label.pack()
        self.nazwisko_entry = tk.Entry(self.root)
        self.nazwisko_entry.pack()

        self.pesel_label = tk.Label(self.root, text="PESEL")
        self.pesel_label.pack()
        self.pesel_entry = tk.Entry(self.root)
        self.pesel_entry.pack()

        self.add_client_button = tk.Button(self.root, text="Dodaj Klienta", command=self.add_client)
        self.add_client_button.pack()

        self.nr_konta_label = tk.Label(self.root, text="Numer Konta")
        self.nr_konta_label.pack()
        self.nr_konta_entry = tk.Entry(self.root)
        self.nr_konta_entry.pack()

        self.edit_client_button = tk.Button(self.root, text="Edytuj Klienta", command=self.edit_client)
        self.edit_client_button.pack()

        self.delete_client_button = tk.Button(self.root, text="Usuń Klienta", command=self.delete_client)
        self.delete_client_button.pack()

        self.amount_label = tk.Label(self.root, text="Kwota")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.deposit_button = tk.Button(self.root, text="Wpłata", command=self.deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(self.root, text="Wypłata", command=self.withdraw)
        self.withdraw_button.pack()

        self.check_balance_button = tk.Button(self.root, text="Sprawdź Saldo", command=self.check_balance)
        self.check_balance_button.pack()

    def add_client(self):
        imie = self.imie_entry.get()
        nazwisko = self.nazwisko_entry.get()
        pesel = self.pesel_entry.get()
        response = self.banker_terminal.add_client(imie, nazwisko, pesel)
        if response["status"] == "success":
            messagebox.showinfo("Dodano Klienta", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

    def edit_client(self):
        nr_konta = self.nr_konta_entry.get()
        imie = self.imie_entry.get()
        nazwisko = self.nazwisko_entry.get()
        pesel = self.pesel_entry.get()
        response = self.banker_terminal.edit_client(nr_konta, imie, nazwisko, pesel)
        if response["status"] == "success":
            messagebox.showinfo("Edytowano Klienta", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

    def delete_client(self):
        nr_konta = self.nr_konta_entry.get()
        response = self.banker_terminal.delete_client(nr_konta)
        if response["status"] == "success":
            messagebox.showinfo("Usunięto Klienta", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

    def deposit(self):
        nr_konta = self.nr_konta_entry.get()
        amount = float(self.amount_entry.get())
        response = self.banker_terminal.deposit(nr_konta, amount)
        if response["status"] == "success":
            messagebox.showinfo("Wpłata", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

    def withdraw(self):
        nr_konta = self.nr_konta_entry.get()
        amount = float(self.amount_entry.get())
        response = self.banker_terminal.withdraw(nr_konta, amount)
        if response["status"] == "success":
            messagebox.showinfo("Wypłata", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

    def check_balance(self):
        nr_konta = self.nr_konta_entry.get()
        response = self.banker_terminal.check_balance(nr_konta)
        if response["status"] == "success":
            messagebox.showinfo("Saldo", f"Saldo: {response['saldo']} PLN")
        else:
            messagebox.showerror("Błąd", response["message"])

if __name__ == "__main__":
    root = tk.Tk()
    banker_terminal = BankerTerminal()
    app = BankerGUI(root, banker_terminal)
    root.mainloop()
