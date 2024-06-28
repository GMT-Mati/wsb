import socket
import json
import threading

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
                self.clients = json.load(file)
        except FileNotFoundError:
            self.clients = []

    def save_clients_data(self):
        with open(self.clients_data_file, 'w') as file:
            json.dump(self.clients, file, indent=4)

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                request = json.loads(data)
                response = self.process_request(request)
                client_socket.send(json.dumps(response).encode('utf-8'))
            except:
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
        return {"status": "error", "message": "Nieznana operacja"}

    def check_balance(self, request):
        # Implementacja sprawdzania stanu konta
        pass

    def deposit(self, request):
        # Implementacja wpłaty środków
        pass

    def withdraw(self, request):
        # Implementacja wypłaty środków
        pass

    def transfer(self, request):
        # Implementacja przelewu środków
        pass

    def add_client(self, request):
        # Implementacja dodawania nowego klienta
        pass

    def edit_client(self, request):
        # Implementacja edycji danych klienta
        pass

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print("Połączono z", addr)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = BankServer()
    server.run()
