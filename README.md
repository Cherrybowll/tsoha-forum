# Keskustelusovellus

### Nykytila ja tämänhetkiset käyttöohjeet (kolmas välipalautus 21.4)

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
Määritä tietokannan skeema ja luo ylläpitäjä-käyttäjä **admin** salasanalla **admin** komennolla:
```
psql < schema.sql
```
Nyt voit käynnistää sovelluksen komennolla:
```
flask run
```

**HUOMIO!** Ainakin toistaiseksi ainoa tapa toimia ylläpitäjänä on käyttää skeemassa valmiiksi määriteltyä ylläpitäjäkäyttäjää **admin** tai `psql`-tulkin kautta muuttaa jokin käyttäjä ylläpitäjäksi komennolla:
```
UPDATE users SET admin_role=TRUE WHERE name="[käyttäjänimi]";
```

Nykytilassaan sovellus ei vielä oikein yllä viikkopalautuksen tavoitteisiin eli siitä puuttuu useitakin oleellisia ominaisuuksia, joihin lukeutuu muun muassa seuraavat: mahdollisuus tehdä käyttäjistä ylläpitäjiä, käyttäjien profiilisivut, CSRF-hyökkäykseltä suojaaminen, kunnolliset ERROR-sivut ja viestien hakuominaisuus.

Tällä hetkellä sovelluksessa on toteutettu ensinnäkin käyttäjän rekisteröinti sekä sisään- ja uloskirjautuminen ja varsinaisen keskutelun osalta rajattujen/julkisten aihealueiden luominen ja poistaminen (ylläpitäjät) ja ketjujen ja viestien luominen, muokkaaminen sekä poistaminen.

Vertaiarvioijan työn mahdolliseksi helpottamiseksi mainitsen muutamia ongelmia, joiden olemassaolosta olen tietoinen ja siten niistä ei tarvitse välttämättä palautteessa mainita:
- "ERROR-sivut" ovat vain palautettuja merkkijonoja ja siten varsin epäkäytännöllisiä
- URL:ää muokkaamalla saa useilla sivuilla helposti virhetilanteen koodissa (tosin saa miellelään mainita jos onnistuu URL-muokkauksen avulla tekemeään jotain oletettavasti ei-toivottuja muutoksia)
- "muokkaa viestiä"- ja "poista viesti"-painikkeet näkyvät kaikille käyttäjille kaikissa viesteissä, vaikkei niiden käyttö olisi mahdollista kyseiselle käyttäjälle
- missään tekstikentässä ei ole syötteelle pituusrajoituksia (paitsi salasana ei voi olla tyhjä)
- Aikaleimat ovat todella rumat millisekunteineen

## Tästä eteen päin vanhaa ja epäoleellista dokumentaatiota

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

Tiedettyjä ongelmia tällä hetkellä ovat VARMASTI ainakin se, että kuka vain voi poistaa kenen tahansa viestejä/ketjuja, ulkoasu on hirvittävä, joiltain sivulta puuttuu takaisin-painikkeita, URL:n muuttaminen käsin voi aiheuttaa lukuisia ei-toivottuja seurauksia, jne., joten valitettavasti sovelluksen anti vertaisarvioijaille on tällä hetkellä melko häviävä.

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