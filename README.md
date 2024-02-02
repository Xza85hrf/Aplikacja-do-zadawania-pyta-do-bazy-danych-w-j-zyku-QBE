# Aplikacja do zadawania pytań do bazy danych w języku QBE
Intuicyjna aplikacja QBE do zarządzania bazą danych szkolnej w Pythonie, z funkcją zaawansowanego wyszukiwania i eksportu danych.

# School Database Management - QBE Application

## Opis

Aplikacja "School Database Management" to przykładowe narzędzie do zarządzania bazą danych szkolnej z wykorzystaniem języka Query by Example (QBE). Została stworzona w języku Python i umożliwia intuicyjne tworzenie zapytań do bazy danych bez konieczności znajomości SQL i QBE.

## Funkcje

- Tworzenie zapytań QBE
- Zaawansowane wyszukiwanie z wykorzystaniem wielu kryteriów
- Eksport wyników zapytań do formatu PDF
- Interfejs użytkownika dostosowany do osób nieposiadających specjalistycznej wiedzy informatycznej

## Instalacja

Wymagania Systemowe
Python 3.6 lub nowszy.
Serwer MySQL.
Zainstalowane niezbędne biblioteki Pythona.
Krok po Kroku

1. Konfiguracja Środowiska
   Upewnij się, że masz zainstalowany Python oraz menedżer pakietów pip. Możesz to zrobić, odwiedzając stronę Python.org i postępując zgodnie z instrukcjami instalacji dla Twojego systemu operacyjnego.

2. Instalacja MySQL
   Zainstaluj MySQL Server, jeśli jeszcze tego nie zrobiłeś. Możesz pobrać instalator ze strony MySQL. Podczas instalacji zapisz nazwę użytkownika i hasło, które będziesz potrzebować do konfiguracji połączenia z bazą         danych.

3. Przygotowanie Bazy Danych
   Utwórz bazę danych school i tabele zgodnie ze skryptem SQL dostarczonym w projekcie. Możesz to zrobić za pomocą narzędzia wiersza poleceń MySQL lub interfejsu graficznego, takiego jak MySQL Workbench.

4. Klonowanie Repozytorium
   Sklonuj repozytorium lokalnie za pomocą polecenia:
   git clone [URL_DO_REPOZYTORIUM]
   Jeśli masz projekt lokalnie, upewnij się, że masz wszystkie potrzebne pliki projektu.

6. Instalacja Zależności
   Przejdź do katalogu projektu i zainstaluj wymagane zależności:
   pip install -r requirements.txt

7. Konfiguracja Połączenia z Bazą Danych
    Upewnij się, że plik QBESchool.py  zawiera poprawne dane dostępowe do serwera MySQL.

8. Uruchomienie Aplikacji
   Po skonfigurowaniu połączenia z bazą danych uruchom aplikację poleceniem:
   python QBESchool.py
   Aplikacja powinna uruchomić się i być gotowa do użytku.

Upewnij się, że wszystkie kroki zostały wykonane zgodnie z instrukcjami i że Twoje środowisko pracy jest odpowiednio przygotowane do uruchomienia projektu.
