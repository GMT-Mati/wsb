import requests
import os
from urllib.parse import unquote


def download_file(url, folder):
    # Pobierz zawartość pliku
    response = requests.get(url)

    # Pobierz nazwę pliku z nagłówka content-disposition
    if "content-disposition" in response.headers:
        file_name = unquote(response.headers["content-disposition"].split("filename=")[1])
    else:
        # Jeśli nie ma nagłówka content-disposition, pobierz nazwę pliku z URL
        file_name = url.split("/")[-1]

    # Usuń ewentualne otaczające cudzysłowy z nazwy pliku
    file_name = file_name.strip('"')

    # Połącz ścieżkę folderu z nazwą pliku
    file_path = os.path.join(folder, file_name)

    # Zapisz zawartość pliku
    with open(file_path, "wb") as file:
        file.write(response.content)

    print(f"Pobrano plik: {file_name}")


def main():
    # URL do plików .xlsx
    urls = [
        "https://drive.google.com/uc?export=download&id=1wKpSpTx89dbU3SrKt-3-DqQ62kHOFHSX",
        "https://drive.google.com/uc?export=download&id=1oYKyW7flL53smo56W9srpFdoUuz6_42x"
    ]
    # Ścieżka do folderu download
    folder = "download"

    # Sprawdź czy folder istnieje, jeśli nie - utwórz
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Pobierz każdy plik z listy URL
    for url in urls:
        download_file(url, folder)


if __name__ == "__main__":
    main()
