def process_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    # Symulacja przetwarzania danych: liczenie liczby linii
    return len(lines)
