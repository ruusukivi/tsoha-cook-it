# Tietokantasovellus (tsoha) -kurssin harjoitustyö

Projekti on tehty tietojenkäsittelytieteen harjoitustyökurssia varten, jossa aiheena tietokantaa käyttävä web-sovellus.

Sovellus Herokussa: https://tsoha-cook-it.herokuapp.com/

Admin-käyttäjä:
kt: testi
ss: 1234567890

Jos haluat testata lokaalisti, varmista ensin, että ympäristössä Python3, Flask ja Postgres asennettuina.
1. Alusta tietokantataulut: psql < /sql/schema.sql
2. Aja kantaan testisisältöä: psql < /sql/data.sql
3. Käynnistä sovellus: flask run

## COOK IT -reseptihaku

Cook It on sovellus, johon voi tallettaa reseptejä sekä hakea ja kommentoida niitä.

### Käyttötapaukset

- :white_check_mark: Palveluun voi kirjautua
- :white_check_mark: Palveluun voi luoda uusia tunnuksia
- :white_check_mark: Palvelusta voi kirjautua ulos
- :white_check_mark: Kirjautunut käyttäjä voi lisätä reseptejä
- :white_check_mark: Reseptille voi lisätä nimen, tyypin, kuvauksen, ainekset ja tekovaiheet
- :white_check_mark: Reseptejä voi selata aikajärjestyksessä
- :white_check_mark: Jokaiselle reseptille on oma sivunsa
- :white_check_mark: Käyttäjä voi poistaa lisäämänsä reseptit
- :white_check_mark: Resepteistä voi tykätä jos on kirjautunut
- :white_check_mark: Käyttäjällä on oma profiilisivu, jossa on hänen lisäämänsä reseptit
- :white_check_mark: Reseptejä voi selata suosituimmuus-järjestyksessä (eniten tykkäyksiä)
- :white_check_mark: Kirjautunut käyttäjä voi kommentoida reseptejä
- :white_check_mark: Reseptejä voi selata kommenttien määrän perusteella
- :white_check_mark: Profiilisivulla voi selata käyttäjän tykkäämiä viestejä
- :white_check_mark: Profiilisivulla voi selata käyttäjän kommentoimia viestejä
- :white_check_mark: Käyttäjä voi poistaa lisäämänsä kommentit
- :white_check_mark: Käyttäjälle voi lisätä admin-oikeudet profiilisivulta jos on admin
- :white_check_mark: Admin-käyttäjä voi poistaa kenen tahansa reseptit ja kommentit
- :white_check_mark: Reseptejä voi hakea nimen perusteella
- :white_check_mark: Reseptejä voi hakea kuvauksen perusteella
- :white_check_mark: Reseptejä voi hakea tyypin perusteella
- :white_check_mark: Reseptejä voi päivittää
- :white_check_mark: Reseptiin voi lisätä kuva
- :white_check_mark: Reseptin lisätty kuva poistetaan kun resepti poistetaan
- :white_check_mark: Reseptissä olevaa kuvaa voi päivittää

- :white_large_square: Admin-käyttäjä voi valita Featured-reseptejä etusivulle


