import tkinter as tk
from tkinter import messagebox
import socket
import json

class ClientTerminal:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        self.client_socket.send(json.dumps(request).encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        return json.loads(response)

    def check_balance(self, nr_konta):
        request = {
            "operation": "check_balance",
            "nr_konta": nr_konta
        }
        return self.send_request(request)

    def deposit(self, nr_konta, amount):
        request = {
            "operation": "deposit",
            "nr_konta": nr_konta,
            "amount": amount
        }
        return self.send_request(request)

    def withdraw(self, nr_konta, amount):
        request = {
            "operation": "withdraw",
            "nr_konta": nr_konta,
            "amount": amount
        }
        return self.send_request(request)

    def transfer(self, from_account, to_account, amount):
        request = {
            "operation": "transfer",
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount
        }
        return self.send_request(request)

class ClientGUI:
    def __init__(self, root, client_terminal):
        self.client_terminal = client_terminal
        self.root = root
        self.root.title("Klient Bankowy")
        self.create_widgets()

    def create_widgets(self):
        self.nr_konta_label = tk.Label(self.root, text="Numer Konta")
        self.nr_konta_label.pack()
        self.nr_konta_entry = tk.Entry(self.root)
        self.nr_konta_entry.pack()

        self.check_balance_button = tk.Button(self.root, text="Sprawdź Saldo", command=self.check_balance)
        self.check_balance_button.pack()

        self.amount_label = tk.Label(self.root, text="Kwota")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.deposit_button = tk.Button(self.root, text="Wpłata", command=self.deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(self.root, text="Wypłata", command=self.withdraw)
        self.withdraw_button.pack()

        self.to_account_label = tk.Label(self.root, text="Na Numer Konta (do przelewu)")
        self.to_account_label.pack()
        self.to_account_entry = tk.Entry(self.root)
        self.to_account_entry.pack()

        self.transfer_button = tk.Button(self.root, text="Przelew", command=self.transfer)
        self.transfer_button.pack()

    def check_balance(self):
        nr_konta = self.nr_konta_entry.get()
        response = self.client_terminal.check_balance(nr_konta)
        if response["status"] == "success":
            messagebox.showinfo("Saldo", f"Saldo: {response['saldo']} PLN")
        else:
            messagebox.showerror("Błąd", response["message"])

    def deposit(self):
        nr_konta = self.nr_konta_entry.get()
        amount = float(self.amount_entry.get())
        response = self.client_terminal.deposit(nr_konta, amount)
        if response["status"] == "success":
            messagebox.showinfo("Wpłata", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

    def withdraw(self):
        nr_konta = self.nr_konta_entry.get()
        amount = float(self.amount_entry.get())
        response = self.client_terminal.withdraw(nr_konta, amount)
        if response["status"] == "success":
            messagebox.showinfo("Wypłata", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

    def transfer(self):
        from_account = self.nr_konta_entry.get()
        to_account = self.to_account_entry.get()
        amount = float(self.amount_entry.get())
        response = self.client_terminal.transfer(from_account, to_account, amount)
        if response["status"] == "success":
            messagebox.showinfo("Przelew", response["message"])
        else:
            messagebox.showerror("Błąd", response["message"])

if __name__ == "__main__":
    root = tk.Tk()
    client_terminal = ClientTerminal()
    app = ClientGUI(root, client_terminal)
    root.mainloop()
