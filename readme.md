Tilanvarausjärjestelmä

-	Tiloja voi varata vain klo 16-21 välillä

-	Database tables (db.Models):
    o   users
        -id
        -username
        -email
        -password
        -created_at
        -updated_at
        
    o	workspaces
        -id
        -name
        -user_limit
        -available_from
        -available_till
        
    o	reservations
        -id
        -start_time
        -end_time
        -workspace_id
        -user_id

-   Resources (flask-restful Resources):
    o   users
        -create user (admin)
        -get user information by name/email (admin)
        -get own user information by login token (user)

    o   workspaces
        -create workspace (admin)
        -modify workspace (admin)
        -delete workspace (admin)
        -(get information about all workspaces) (user)
        -(get information about a specific workspace) (user)

    o   reservations
        -get reservations by workspace id/name, today VAI get available time slots based on these
            - reservations from today ->
            - reservations between dates a, b
            - with user info (admin)
            - without user info (user)
        -get own reservations (user)
            - reservations from today ->
        -create reservation (user)
        -delete own reservation (user)
        -delete old reservations (once a week, today - x months) (admin)



-	käyttäjän tehdessä varausta ohjelma tarkistaa databasesta ettei päällekkäisiä varauksia ole
        -uuden varauksen aloitusajankohta ja lopetusajankohta tsekkaus BETWEEN päivälle jo löytyvien varauksien kellonajat

-	Poistetaanko publish toiminto? Eli kun varaus tehdään, se on automaattisesti julkinen #Joo!

-	Tarviiko vanhat varaukset poistaa databasesta? Käyttäjälle pitäisi näkyä vain tulevat varaukset
        -poisto jonkun aikarajan jälkeen? today-x kuukautta esim. kerran viikossa ajona?

-	Tilavaraukset alkaa vain tasatunnein ja kestää x tuntia -> ohjelman täytyy tarkistaa vain tasatunnein ettei päällekkäisiä varauksia ole, kun käyttäjä tekee tilavarausta 

- Admin tunnukset: Tehdään käyttäjä jonka nimi on Admin, ohjelma tarkistaa if current_user=="Admin" ennenkuin antaa käyttöoikeudet. Vain Admin voi:
    o   luoda uusia käyttäjiä?
    o   luoda uusia /muokata työtiloja
    o   tarkastella kaikkia tulevia ja menneitä varauksia mukaanlukien varaajan tiedot
    o   muokata muidenkin varauksia <- tarvitaanko tällaista valtuutusta?

- Peruskäyttäjä voi:
    o   luoda varauksen
    o   tarkastella kaikkia tulevia varauksia ilman varaajan tietoja
    o   perua oman tulevan varauksensa

- Käyttäjän näkymä varauksia hakiessa: Jos mahdollista, olisi hyvä jos käyttäjän hakiessa tiloja jokaisen tilan kohdalla näkyisi milloin se kyseinen tila on varattavissa (tai jos se on liian vaikeaa niin vaihtoehtoisesti käyttäjä näkee kunkin tilan kohdalla siihen tilaan tehdyt varaukset), sen sijaan että käyttäjä joutuisi erikseen hakemaan listauksen tiloista ja listauksen varauksista