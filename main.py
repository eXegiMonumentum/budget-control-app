#Aplikacja do zarządzania budżetem
# Opis projektu:
# Aplikacja do zarządzania budżetem osobistym to narzędzie, które umożliwia użytkownikowi monitorowanie swoich finansów poprzez dodawanie transakcji, przypisywanie ich do odpowiednich kategorii, a także generowanie szczegółowych raportów. Celem aplikacji jest pomoc w analizie wydatków i zarządzaniu finansami, co pozwala na lepsze planowanie budżetu.
#
# Technologie:
# Backend: Python
# Baza danych: PostgreSQL
# Interfejs użytkownika: Konsola (możliwość rozszerzenia na interfejs webowy w przyszłości)
# Biblioteki: psycopg2 do połączenia z PostgreSQL, tabulate do wyświetlania tabel w konsoli, matplotlib do prostych wizualizacji danych


# Funkcje aplikacji:

# 1. Rejestracja i logowanie użytkowników:
#
#  --- Możliwość zakładania konta z hasłem.
#  --- Logowanie do istniejącego konta.
#  --- Ochrona hasła przy użyciu szyfrowania (np. bcrypt).
# 2. Dodawanie transakcji:
#
#  --- Możliwość dodawania przychodów i wydatków.
#  --- Pola: kwota, data, kategoria (np. jedzenie, transport, rozrywka), opcjonalny opis.
#  --- Każda transakcja jest powiązana z kontem użytkownika, który ją dodał.
# 3. Zarządzanie kategoriami:
#
#  --- Dodawanie, edytowanie i usuwanie kategorii.
#  --- Przykładowe kategorie: Jedzenie, Transport, Rozrywka, Rachunki, Inne.
#  --- Możliwość dodawania własnych kategorii przez użytkownika.
# 4. Generowanie raportów:
#
#  --- Raport miesięczny: Wyświetlanie sumy przychodów, sumy wydatków i bilansu netto za dany miesiąc.
#  --- Raport kategorii: Sumaryczne wydatki w podziale na kategorie (np. ile wydano na jedzenie, transport itp.).
#  --- Raport trendów: Wizualizacja trendów wydatków/przychodów na przestrzeni miesięcy.
# 5. Analiza wydatków:
#
#  --- Średnie wydatki na kategorię.
#  --- Wykresy przedstawiające wydatki w poszczególnych kategoriach.
#  --- Ostrzeżenia przy przekroczeniu ustalonych budżetów dla kategorii.
# 6. Zarządzanie budżetem:
#
#  --- Możliwość ustawienia miesięcznego budżetu dla poszczególnych kategorii.
#  --- Powiadomienia (np. w konsoli) o zbliżaniu się do limitu wydatków w danej kategorii.
# 7. Eksport danych:
#
#  --- Eksport transakcji do pliku CSV lub PDF.
#  --- Możliwość wygenerowania raportu w formie tekstowej lub wykresu.
# 8. Import danych:
#
#  --- Możliwość importu danych z pliku CSV (np. wcześniejsze wydatki z innej aplikacji).
# 9. Historia transakcji:
#
#  --- Przeglądanie historii transakcji, z możliwością filtrowania po dacie, kategorii lub kwocie.
# 10. Backup danych:
#
#  --- Automatyczne tworzenie kopii zapasowej bazy danych w regularnych odstępach czasu.




# Kroki realizacji projektu:
# Projekt bazy danych:
#
# Stwórz schemat bazy danych z tabelami: users, transactions, categories.
# Zadbaj o relacje między tabelami, np. każda transakcja powinna być powiązana z użytkownikiem i kategorią.
# Backend w Pythonie:
#
# Zaimplementuj podstawowe funkcje do interakcji z bazą danych (dodawanie transakcji, zarządzanie kategoriami).
# Utwórz funkcje do generowania raportów.
# Interfejs użytkownika:
#
# Zbuduj interaktywny interfejs w konsoli, umożliwiający łatwą nawigację po funkcjach aplikacji.
# Zaimplementuj logikę logowania, rejestracji, dodawania transakcji i generowania raportów.
# Testowanie:
#
# Testuj każdą funkcję oddzielnie, a następnie przeprowadzaj testy integracyjne, aby upewnić się, że wszystkie elementy działają razem.
# Dokumentacja:
#
# Sporządź dokumentację, opisującą jak zainstalować i używać aplikacji.
# Dodaj przykłady użycia oraz wyjaśnienie struktury bazy danych.
# Możliwości rozbudowy:
# Przeniesienie interfejsu z konsoli do prostego interfejsu webowego (np. z Flask).
# Implementacja systemu powiadomień e-mailowych lub SMS.
# Wersja mobilna aplikacji (np. z wykorzystaniem frameworka Kivy).
# Taki projekt pokaże Twoje umiejętności w zakresie programowania w Pythonie, zarządzania bazami danych, a także tworzenia aplikacji, które rozwiązują rzeczywiste problemy.

from credentials import SignUp
print("sign up simulation")

while True:
    email = input("Please enter your e-mail: ")
    SignUp.print_password_requirements()
    password = input("Please enter your password: ")
    repeated_password = input("Please repeat password: ")

    try:
        user = SignUp(email, password, repeated_password)
        hashed_password_str = SignUp.hashing_password(password)
        SignUp.save_credentials_to_file(email, hashed_password_str)
        print("Sign up successful.")
        break
    except ValueError as e:
        print(f"Sign up failed: {e}")

# username, ill add it tomorrow.



