import socket
import json
import threading
import random

class BankServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.clients_data_file = 'clients.json'
        self.load_clients_data()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Serwer SB uruchomiony na porcie", self.port)

    def load_clients_data(self):
        try:
            with open(self.clients_data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"clients": []}

    def save_clients_data(self):
        with open(self.clients_data_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Otrzymano dane: {data}")  # Debugowanie
                request = json.loads(data)
                response = self.process_request(request)
                print(f"Wyślij odpowiedź: {response}")  # Debugowanie
                client_socket.send(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"Błąd: {e}")  # Debugowanie
                break
        client_socket.close()

    def process_request(self, request):
        operation = request.get("operation")
        if operation == "check_balance":
            return self.check_balance(request)
        elif operation == "deposit":
            return self.deposit(request)
        elif operation == "withdraw":
            return self.withdraw(request)
        elif operation == "transfer":
            return self.transfer(request)
        elif operation == "add_client":
            return self.add_client(request)
        elif operation == "edit_client":
            return self.edit_client(request)
        elif operation == "delete_client":
            return self.delete_client(request)
        return {"status": "error", "message": "Nieznana operacja"}

    def check_balance(self, request):
        nr_konta = request.get("nr_konta")
        client = self.find_client(nr_konta)
        if client:
            return {"status": "success", "saldo": client["saldo"]}
        return {"status": "error", "message": "Nie znaleziono klienta"}

    def deposit(self, request):
        nr_konta = request.get("nr_konta")
        amount = float(request.get("amount"))
        client = self.find_client(nr_konta)
        if client:
            client["saldo"] += amount
            self.save_clients_data()
            return {"status": "success", "message": f"Wpłacono {amount} PLN"}
        return {"status": "error", "message": "Nie znaleziono klienta"}

    def withdraw(self, request):
        nr_konta = request.get("nr_konta")
        amount = float(request.get("amount"))
        client = self.find_client(nr_konta)
        if client:
            if client["saldo"] >= amount:
                client["saldo"] -= amount
                self.save_clients_data()
                return {"status": "success", "message": f"Wypłacono {amount} PLN"}
            return {"status": "error", "message": "Niewystarczające środki na koncie"}
        return {"status": "error", "message": "Nie znaleziono klienta"}

    def transfer(self, request):
        from_account = request.get("from_account")
        to_account = request.get("to_account")
        amount = float(request.get("amount"))

        sender = self.find_client(from_account)
        receiver = self.find_client(to_account)

        if sender and receiver:
            if sender["saldo"] >= amount:
                sender["saldo"] -= amount
                receiver["saldo"] += amount
                self.save_clients_data()
                return {"status": "success", "message": f"Przelew wykonany: {amount} PLN"}
            return {"status": "error", "message": "Niewystarczające środki na koncie"}
        return {"status": "error", "message": "Nie znaleziono jednego z kont"}

    def add_client(self, request):
        imie = request.get("imie")
        nazwisko = request.get("nazwisko")
        pesel = request.get("pesel")

        if not self.check_if_client_exists(pesel):
            nr_konta = self.generate_account_number()
            new_client = {
                "imie": imie,
                "nazwisko": nazwisko,
                "pesel": pesel,
                "nr_konta": nr_konta,
                "saldo": 0.0
            }
            self.data["clients"].append(new_client)
            self.save_clients_data()
            return {"status": "success", "message": f"Nowy klient dodany, nr konta: {nr_konta}"}
        return {"status": "error", "message": "Klient o podanym PESEL już istnieje"}

    def edit_client(self, request):
        nr_konta = request.get("nr_konta")
        imie = request.get("imie")
        nazwisko = request.get("nazwisko")
        pesel = request.get("pesel")

        client = self.find_client(nr_konta)
        if client:
            client["imie"] = imie if imie else client["imie"]
            client["nazwisko"] = nazwisko if nazwisko else client["nazwisko"]
            client["pesel"] = pesel if pesel else client["pesel"]
            self.save_clients_data()
            return {"status": "success", "message": "Dane klienta zaktualizowane"}
        return {"status": "error", "message": "Nie znaleziono klienta"}

    def delete_client(self, request):
        nr_konta = request.get("nr_konta")
        for client in self.data["clients"]:
            if client["nr_konta"] == nr_konta:
                self.data["clients"].remove(client)
                self.save_clients_data()
                return {"status": "success", "message": "Klient usunięty"}
        return {"status": "error", "message": "Nie znaleziono klienta"}

    def generate_account_number(self):
        max_attempts = 1000  # Prevent infinite loop
        for _ in range(max_attempts):
            nr_konta = str(random.randint(1, 99999999)).zfill(8)
            if not self.find_client(nr_konta):
                return nr_konta
        raise Exception("Nie udało się wygenerować unikalnego numeru konta")

    def find_client(self, nr_konta):
        for client in self.data["clients"]:
            if client["nr_konta"] == nr_konta:
                return client
        return None

    def check_if_client_exists(self, pesel):
        for client in self.data["clients"]:
            if client["pesel"] == pesel:
                return True
        return False

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print("Połączono z", addr)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = BankServer()
    server.run()
