# Tietokantasovellus (tsoha) -kurssin harjoitustyö

Projekti on tehty tietojenkäsittelytieteen harjoitustyökurssia varten, jossa aiheena tietokantaa käyttävä web-sovellus.

Sovellus Herokussa: https://tsoha-cook-it.herokuapp.com/

Peruskäyttäjä:
kt: testi@mailinator.com
ss: 1234567890

Jos haluat testata lokaalisti, varmista ensin, että ympäristössä Python3, Flask ja Postgres asennettuina.
1. Alusta tietokantataulut: psql < schema.sql
2. Käynnistä sovellus: flask run
3. Luo itsellesi käyttäjätunnus http://127.0.0.1:5000/signup 
3. Aja kantaan testisisältöä: psql < data.sql

## COOK IT -reseptihaku

Cook it on sovellus, johon voi tallettaa reseptejä sekä hakea ja kommentoida niitä.

### Käyttötapaukset

- :white_check_mark: Palveluun voi kirjautua
- :white_check_mark: Palveluun voi luoda uusia tunnuksia
- :white_check_mark: Palvelusta voi kirjautua ulos
- :white_check_mark: Kirjautunut käyttäjä voi lisätä reseptejä
- :white_check_mark: Reseptille voi lisätä nimen, tyypin, kuvauksen, ainekset ja tekovaiheet
- :white_check_mark: Reseptejä voi selata tuoreusjärjestyksessä
- :white_check_mark: Jokaiselle reseptille on oma sivunsa
- :white_check_mark: Käyttäjä voi poistaa lisäämänsä reseptit
- :white_check_mark: Resepteistä voi tykätä jos on kirjautunut
- :white_check_mark: Käyttäjällä on oma profiilisivu

- :white_large_square: Resepteistä voi selata suosituimmuus-järjestyksessä
- :white_large_square: Reseptejä voi kommentoida
- :white_large_square: Käyttäjä voi poistaa lisäämänsä kommentit
- :white_large_square: Palveluun voi luoda admin-tunnuksia
- :white_large_square: Admin-käyttäjä voi poistaa kenen tahansa reseptit ja kommentit
- :white_large_square: Reseptejä voi hakea nimen perusteella
- :white_large_square: Reseptejä voi hakea julkaisuajan perusteella
- :white_large_square: Reseptejä voi hakea tyypin perusteella
- :white_large_square: Reseptejä voi hakea suosion perusteella
- :white_large_square: Reseptejä voi hakea lisääjän perusteella
- :white_large_square: Reseptiin voi lisätä kuvan
- :white_large_square: Admin-käyttäjä voi valita Featured-reseptejä etusivulle

### Tekniset vaatimukset
