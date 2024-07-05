import socket
import json

class ClientTerminal:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        print(f"Wysyłanie żądania: {request}")  # Debugowanie
        self.client_socket.send(json.dumps(request).encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        print(f"Otrzymano odpowiedź: {response}")  # Debugowanie
        return json.loads(response)

    def check_balance(self, nr_konta):
        request = {
            "operation": "check_balance",
            "nr_konta": nr_konta
        }
        response = self.send_request(request)
        print("Saldo konta:", response.get("saldo"))

    def deposit(self, nr_konta, amount):
        request = {
            "operation": "deposit",
            "nr_konta": nr_konta,
            "amount": amount
        }
        response = self.send_request(request)
        print(response.get("message"))

    def withdraw(self, nr_konta, amount):
        request = {
            "operation": "withdraw",
            "nr_konta": nr_konta,
            "amount": amount
        }
        response = self.send_request(request)
        print(response.get("message"))

    def transfer(self, from_account, to_account, amount):
        request = {
            "operation": "transfer",
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount
        }
        response = self.send_request(request)
        print(response.get("message"))

if __name__ == "__main__":
    client = ClientTerminal()
    # Przykłady wywołania funkcji terminala klienta
    client.check_balance("00000001")
    client.deposit("00000001", 200)
    client.withdraw("00000001", 50)
    client.transfer("00000001", "00000002", 100)
