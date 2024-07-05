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
        response = self.send_request(request)
        print(response.get("message"))

    def edit_client(self, nr_konta, imie=None, nazwisko=None, pesel=None):
        request = {
            "operation": "edit_client",
            "nr_konta": nr_konta,
            "imie": imie,
            "nazwisko": nazwisko,
            "pesel": pesel
        }
        response = self.send_request(request)
        print(response.get("message"))

if __name__ == "__main__":
    banker = BankerTerminal()
    # Przykłady użycia
    banker.add_client("Anna", "Nowak", "98765432101")
    banker.edit_client("00000001", imie="Janusz")
