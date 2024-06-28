# Prosty CMS w Pythonie z użyciem Flask, SQLite i Flask-Bootstrap

Projekt CMS (System Zarządzania Treścią) stworzony w Pythonie z wykorzystaniem frameworka Flask oraz bazy danych SQLite. Projekt umożliwia tworzenie, wyświetlanie, edytowanie i usuwanie artykułów przez zalogowanych użytkowników. Interfejs użytkownika jest zbudowany przy użyciu Flask-Bootstrap.

Projekt jest idealny dla początkujących, którzy chcą nauczyć się podstaw tworzenia aplikacji webowych w Pythonie przy użyciu Flask oraz pracy z bazą danych SQLite.

## Funkcje

### 1. Rejestracja i logowanie użytkowników
- Użytkownicy mogą zarejestrować się podając nazwę użytkownika i hasło.
- Zalogowani użytkownicy mają dostęp do tworzenia, edytowania i usuwania artykułów.

### 2. Zarządzanie artykułami
- Użytkownicy mogą dodawać nowe artykuły, podając tytuł i treść.
- Istnieje możliwość przeglądania wszystkich artykułów oraz wyświetlania pojedynczych artykułów po ID.
- Zalogowani użytkownicy mogą edytować istniejące artykuły oraz usuwać artykuły.

## Struktura projektu

1. **`app.py`**: Główny plik aplikacji Flask, zawierający routingi i logikę aplikacji.
2. **`database.py`**: Moduł odpowiedzialny za zarządzanie bazą danych SQLite, w tym tworzenie tabel i połączenie z bazą danych.
3. **`models.py`**: Moduł zawierający modele danych aplikacji, w tym modele użytkownika (`User`) i artykułu (`Article`).
4. **`templates/`**: Katalog zawierający szablony HTML aplikacji Flask, w tym formularze rejestracji, logowania, tworzenia i edycji artykułów.
5. **`static/`**: Katalog zawierający pliki statyczne takie jak arkusze stylów CSS i skrypty JavaScript.

## Jak uruchomić projekt

1. Upewnij się, że masz zainstalowanego Pythona oraz bibliotekę Flask (`pip install flask`).
2. Zainstaluj Flask-Bootstrap (`pip install flask-bootstrap`).
3. Sklonuj ten projekt z repozytorium GitHub.
4. Utwórz i zaaktywuj wirtualne środowisko Pythona (opcjonalne, ale zalecane).
5. Uruchom plik `app.py` komendą:

```sh
python app.py
