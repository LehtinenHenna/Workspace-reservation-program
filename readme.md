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
        -create user (user) 
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

-	Poistetaanko publish toiminto? Eli kun varaus tehdään, se on automaattisesti julkinen <- Joo!  

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


End point design:

| HTTP verb |                Description                 |   Methods to handle the request   |                          URL                           |                          Comments                     | Done |
|-|-|-|-|-|-|
| GET | Gets all workspaces | WorkspaceListResource.get | http://localhost:5000/workspaces | Workspaces include information about reservations, accessible without logging in. Admin also sees the users who made the reservations. |  |
| POST | Create a new workspace | WorkspaceListResource.post | http://localhost:5000/workspaces | Only accessible by Admin |  |
| GET | Gets a specific workspace | WorkspaceResource.get | http://localhost:5000/workspaces/<string:workspace_name> | Includes reservation info, accessible without logging in. Admin also sees info about the user who made the reservation. |  |
| PUT | Modify a workspace | WorkspaceResource.put | http://localhost:5000/workspaces/<string:workspace_name> | Only accessible by Admin |  |
| DELETE | Delete a workspace | WorkspaceResource.delete | http://localhost:5000/workspaces/<string:workspace_name> | Only accessible by Admin |  |
| GET | Gets information about all users | UserListResource.get | http://localhost:5000/users | Only accessible by Admin |  |
| POST | Create a user | UserListResource.post | http://localhost:5000/users | Anyone can create a user |  |
| GET | Get user information by username | UserResource.get | http://localhost:5000/users/<string:username> | Only accessible by Admin |  |
| PUT | Modify any user's information | UserResource.put | http://localhost:5000/users/<string:username> | Only accessible by Admin; Admin can change any user's email, name or password |  |
| DELETE | Delete user account by username | UserResource.delete | http://localhost:5000/users/<string:username> | Only accessible by Admin |  |
| GET | Get user's own information | MeResource.get | http://localhost:5000/me | Gets user's own username, email, future reservations |  |
| PUT | Modify user's own information | MeResource.put | http://localhost:5000/me | User can modify their own username, email or password |  |
| DELETE | Delete user's own account | MeResource.delete | http://localhost:5000/me | Delete user's own account |  |
| GET | Get user's own reservations | ReservationListResource.get | http://localhost:5000/reservations | Displays user's own reservations |  |
| POST | Create a reservation | ReservationListResource.post | http://localhost:5000/reservations | Only for logged in users |  |
| DELETE | Delete old reservations | ReservationListResource.delete | http://localhost:5000/reservations | Automatically deletes old reservations once a week (optional) |  |
| DELETE | Delete user's own reservation by ID | ReservationResource.delete | http://localhost:5000/reservations/<int:reservation_id> | User can delete their own reservation |  |
| POST | Create a json web token | TokenResource.post | http://localhost:5000/token |  | X |
| POST | Create a refresh token | RefreshResource.post | http://localhost:5000/refresh |  | X |
| POST | Blacklists token for logout | RevokeResource.post | http://localhost:5000/revoke |  | X |