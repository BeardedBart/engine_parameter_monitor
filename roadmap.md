# Web GUI na stan 
- <span style="color:lime"> kilka stron
- <span style="color:lime"> jedna z nich to DB, 
- <span style="color:lime"> strona startowa,
- <span style="color:lime"> implementacja funkcji "wgraj plik"
- dodatkowe algorytmy

# CORE
- pandas + numpy,
- csv + sql (23.05.2025)
- github - kontrola wersji
- aby zwiększyć uniwersalność, dodać kolumnę z parametrami "dodatkowymi"

Opcjonalnie
- to użytkownik wybiera, co trzeba zawrzeć w analizie 

# TO DO & Work In Progress
- **[WIP]** <span style="color:cyan"> umozliwienie odpalania starego prgoramu przez GUI - modyfikacja *main.py* </span>
  
  - przypisanie jednostek SI vs Imperial w części bazy danych

- implementacja algorytmu odnośnie gradientu z urządzenia z inżynierki
  
- <span style="color:red"> GIT siedzi lokalnie 
- w opisie w magisterce, dodać schemat ścieżek do poszczególnych miejsc w aplikacji (ala schemat z NanoVNA co masz)

## OPTIONAL
- Dodanie funkcji zapisu liczby przekroczeń dopuszczalnych wartości poszczególnych parametrów w celu przewidywań potencjalnych problemów. 

# ✅<span style="color:#94fe0c"> DONE ✅:
- baza danych o parametrach pracy poszczególnych silników:
  - EGT;
  - CHT;
  - TemOil;
  - Nazwa silnika;
  - Typ;
  - *to be cont.?*
- **Wszystkie funkcjonalności bazy danych działają!**
- strona startowa
- program ma kontrolę wersji GIT
- modyfikacja tworzenia wykresów w **chartgen.py, logic.py oraz processingcore.py** <span style="color:#94fe0c"> **wszystkie** wykresy się tworzą!!!
- Informacja zwrotna dla użytkownika - w postaci <span style="color:#94fe0c">"flashed messages"
- tworzenie raport <span style="color:#94fe0c"> PDF </span>
  - pobrać raportgen open source
  - zastanowić się jak ogarnąć funkcję pobierania z przeglądarki w html/flask