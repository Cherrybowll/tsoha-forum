# Keskustelusovellus

### Nykytila ja tämänhetkiset käyttöhjeet (toinen välipalautus 7.4)

Sovelluksen saat käyttöösi seuraavasti:
Ensiksi kloonaa tämän Github-repositorio omalle laitteellesi ja luo sen juurihakemistoon `.env`-niminen tiedosto, jonka tulee sisältää seuraavat rivit:
```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
Seuraavaksi aktivoi virtuaaliympäristö (yhä repositorion juurihakemistossa) ja asenna riippuvuudet komennoilla:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt
```
Määritä tietokannan skeema ja luo ylläpitäjä-käyttäjä 'admin' salasanalla 'admin' komennolla:
```
psql < schema.sql
```
Nyt voit käynnistää sovelluksen komennolla:
```
flask run
```
Sovelluksen nykytilasta mainittakoon, että en ole saanut sovellusta siihen vaiheeseen, missä olisin sen toivonut tässä vaiheessa olevan (johtuen pitkälti ylenpalttisesta ajankäytöstä tutkiessani ylimääräisten ja itselleni turhan haastavien ominaisuuksien toteuttamismahdollisuuksia), mutta tärkeimmät ja ajallisesti vaativimmat ominaisuudet pitäisi olla koodissa pitkälti toteutettuna (ei tosin välttämättä käytettävissä :D).

Tällä hetkellä sovelluksessa on toteutettuna käyttäjätunnusten rekisteröinti sekä sisään- ja uloskirjautuminen, keskustelusovelluksen tavallinen hierarkinen rakenne (aihesivut>ketjut>viestit), aiheiden, ketjujen ja viestien luominen ja poistaminen. Koodista löytyy kaikki valmistelut käyttäjien oikeuksien rajoittamiseen, mutta en ehtinyt deadlineen mennessä käytännössä toteuttaa näistä kuin aiheiden luonnin rajoittamisen ylläpidolle.

### Sovelluksen suunnitelma (ensimmäinen välipalautus 12.3)

Tarkoituksenani on toteuttaa keskustelusovellus juuri sellaisena kuin on esitetty [kurssin aihe-ehdotuksissa](https://hy-tsoha.github.io/materiaali/aiheen_valinta/). Kyseessä on siis perinteinen keskustelupalstaratkaisu, jossa käyttäjä voi luoda aloitusviestillä keskustelun, joka vastauksineen muodostaa erillisen kokonaisuuden (muista keskusteluista). Keskustelut on lisäksi kategorisoitu joidenkin aihepiirien mukaisesti.
Sovellus kattaa siis varmasti seuraavat toiminnot:
- Käyttäjätunnuksen luominen / sisään- ja uloskirjautuminen
- Etusivulla aihealueet, jokaisesta aihealueesta keskustelujen ja viestien kokonaismäärä sekä viimeisimmän viestin ajankohta
- Ketjujen luominen (vaatii käyttäjän sekä otsikon ja viestin sisällön keskustelunaloitukseen)
- Viestien lisääminen ketjuihin
- Oman ketjun otsikon muokkaaminen / ketjun poistaminen
- Oman viestin muokkaaminen / poistaminen
- Viestien haku (pitää täsmätä täydellisesti hakusanaan) koko sovelluksesta
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita
- Ylläpitäjä voi luoda alueita, joille pääsy on rajoitettu vain valituille käyttäjille / ylläpitäjille

Lisäksi minulla on joitakin ajatuksia ylimääräisille toiminnoille, joita saatan toteuttaa riippuen niiden toteuttamisen haastavuudesta ja motivaatiostani:
- Jonkinlainen mahdollisuus kuvien käyttöön. Joko mahdollisuus lisätä itse kuvia tai todennäköisemmin jokin pieni kokoelma valmiita hymiöitä
- Enemmän ylläpito-oikeuksia
  - Ylläpitäjä voi poistaa muiden käyttäjien viestejä ja ketjuja (ei mainittu aihe-ehdotuksessa)
  - Ylläpitäjä voi estää yksittäisiä käyttäjiä luomasta ketjuja / lähettämästä viestejä (mute/ban)
- Viesteihin/ketjuihin viittaaminen yksilöllistävien tunnisteiden avulla
- Yksittäisten käyttäjien viestien piilottaminen omasta näkymästä ja piilotettujen käyttäjien hallinnointi