# Niniejszy dokument stanowi <span style="color:#94fe0C">instrukcję użytkowania </span> aplikacji
## Informacje o pliku CSV
### Składnia
Nazwa kolumny - dowolna, lecz aby automatyka działała poprawnie, muszą znaleźć się kolumny "egt", "cht" czy choćby "Lcl Time"

## Informacja o bazie danych
Baza danych jest bazą relacyjną, napisaną za pomocą języka *SQL* (nazwa samej tabeli roboczej - "engpdb"; wykorzystana jest biblioteka zaimplementowana domyślnie wraz z językiem *Python*), zawierająca 7 kolumn parametrów maksyalnych (chyba że wskazano inaczej):

- kolumna: 'eng_name' - zawiera nazwy robocze silników, typ danych: char(32)
- kolumna: 'typ' - informacja o typie (benzynowy czy z zapłonem samoczynnym) typ danych: char(32)
- kolumna: 'TOil' - temperatura oleju, typ danych: REAL
- kolumna: 'egt' - temperatura głowicy cylindra typ danych: REAL
- kolumna: 'cht' - temperatura gazów wylotowych, typ danych: REAL
- kolumna: 'oil_press_l' - **minimalne** ciśnienie oleju, typ danych: REAL
- kolumna: 'oil_press_h' - maksymalne ciśnienie oleju, typ danych: REAL.
  
Typ danych "REAL"
## Wersje języka i użytych bibliotek 
Informacje na dzień 10.08.2025
...

## Uruchomienie aplikacji
Aby uruchomić aplikację, należy uruchomić plik wykonawczy <span style="color:#fe940c">run.py </span>, następnie aplikacja samoistnie otworzy odpowiednie okno w przeglądarce. 

