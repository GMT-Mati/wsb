import pandas as pd


def compare_data(file_path_old, file_path_new):
    # Wczytaj dane z obu plików Excel
    df_old = pd.read_excel(file_path_old)
    df_new = pd.read_excel(file_path_new)

    # Jeśli kolumna 'ID' nie istnieje, użyj pierwszej kolumny jako indeks
    if 'ID' not in df_old.columns:
        df_old.set_index(df_old.columns[0], inplace=True)
    if 'ID' not in df_new.columns:
        df_new.set_index(df_new.columns[0], inplace=True)

    # Znajdź nowe rekordy (w nowym pliku, ale nie w starym)
    new_records = df_new.index.difference(df_old.index)

    # Znajdź usunięte rekordy (w starym pliku, ale nie w nowym)
    deleted_records = df_old.index.difference(df_new.index)

    # Znajdź zmienione rekordy (obecne w obu plikach)
    changed_records = df_old.index.intersection(df_new.index)

    # Stwórz raport
    report = []

    # Dodaj nowe rekordy do raportu
    for index in new_records:
        record = {'ID': index, 'Status': 'Nowy', 'Zmiany': 'Brak zmian'}
        report.append(record)

    # Dodaj usunięte rekordy do raportu
    for index in deleted_records:
        record = {'ID': index, 'Status': 'Usunięty', 'Zmiany': 'Brak zmian'}
        report.append(record)

    # Porównaj zmienione rekordy i dodaj informacje o zmianach do raportu
    for index in changed_records:
        changes = []
        for column in df_old.columns:
            if df_old.loc[index, column] != df_new.loc[index, column]:
                change = f"{column}: '{df_old.loc[index, column]}' -> '{df_new.loc[index, column]}'"
                changes.append(change)
        if changes:
            record = {'ID': index, 'Status': 'Zmieniony', 'Zmiany': ', '.join(changes)}
            report.append(record)

    # Zwróć raport jako DataFrame
    report_df = pd.DataFrame(report)

    return report_df


def main():
    # Ścieżki do plików .xlsx
    file_path_old = "download/katalog_2023.xlsx"
    file_path_new = "download/katalog_2024.xlsx"

    # Porównaj dane
    report = compare_data(file_path_old, file_path_new)

    # Zapisz raport do pliku CSV
    report.to_csv("comparison_report.csv", index=False)

    print("Porównanie zakończone. Raport został zapisany do pliku comparison_report.csv")


if __name__ == "__main__":
    main()
