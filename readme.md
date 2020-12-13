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
        -created_at  
        -updated_at   
        
    o	reservations  
        -id  
        -start_time  
        -end_time  
        -workspace_id  
        -user_id
        -created_at  
        -updated_at   



-	Käyttäjän tehdessä varausta ohjelma tarkistaa databasesta ettei päällekkäisiä varauksia ole  
        
-	Poistetaan publish toiminto. Eli kun varaus tehdään, se on automaattisesti julkinen  

-	Käyttäjälle pitäisi näkyä vain tulevat varaukset  
 


- Admin tunnukset: Tehdään käyttäjä jonka nimi on Admin, ohjelma tarkistaa if current_user=="Admin" ennenkuin antaa käyttöoikeudet. Vain Admin voi:  
    o   kirjautua sisään  
    o   luoda uusia / muokata / poistaa työtiloja  
    o   tarkastella kaikkia tulevia ja menneitä varauksia mukaanlukien varaajan tiedot  
    o   tarkastella kaikkia käyttäjiä tai tiettyä käyttäjää, muokata käyttäjätunnuksia / poistaa käyttäjätunnuksia  
      

- Peruskäyttäjä voi:  
    o   luoda käyttäjätunnuksen  
    o   kirjautua sisään  
    o   luoda varauksen  
    o   tarkastella kaikkia tulevia varauksia ja kaikkia omia varauksiaan  
    o   tarkastella varauksia työtilan id:n mukaan  
    o   perua oman tulevan varauksensa  
    o   tarkastella kaikkia työtiloja tai tiettyä työtilaa  
    o   tarkastella / muokata / poistaa omat käyttäjätunnukset  


- Käyttäjän näkymä varauksia hakiessa: Jos mahdollista, olisi hyvä jos käyttäjän hakiessa tiloja jokaisen tilan kohdalla näkyisi milloin se kyseinen tila on varattavissa (tai jos se on liian vaikeaa niin vaihtoehtoisesti käyttäjä näkee kunkin tilan kohdalla siihen tilaan tehdyt varaukset), sen sijaan että käyttäjä joutuisi erikseen hakemaan listauksen tiloista ja listauksen varauksista  


End point design:  

| HTTP verb |                Description                 |   Methods to handle the request   |                          URL                           |                          Comments                     | Done | By |
|-|-|-|-|-|-|-|
| GET | Gets all workspaces | WorkspaceListResource.get | http://localhost:5000/workspaces | Workspaces include information about reservations, accessible without logging in. Admin also sees the users who made the reservations. | X | Atte |
| POST | Create a new workspace | WorkspaceListResource.post | http://localhost:5000/workspaces | Only accessible by Admin | X | Atte |
| GET | Gets a specific workspace | WorkspaceResource.get | http://localhost:5000/workspaces/<string:workspace_name> | Includes reservation info, accessible without logging in. Admin also sees info about the user who made the reservation. | X | Atte |
| PATCH | Modify a workspace | WorkspaceResource.patch | http://localhost:5000/workspaces/<string:workspace_name> | Only accessible by Admin | X | Atte |
| DELETE | Delete a workspace | WorkspaceResource.delete | http://localhost:5000/workspaces/<string:workspace_name> | Only accessible by Admin | X | Atte |
| GET | Gets information about all users | UserListResource.get | http://localhost:5000/users | Only accessible by Admin | X | Joonas |
| POST | Create a user | UserListResource.post | http://localhost:5000/users | Anyone can create a user | X | Joonas |
| GET | Get user information by username | UserResource.get | http://localhost:5000/users/<string:username> | Only accessible by Admin | X | Joonas |
| PATCH | Modify any user's information | UserResource.patch | http://localhost:5000/users/<string:username> | Only accessible by Admin; Admin can change any user's email or name | X | Joonas |
| DELETE | Delete user account by username | UserResource.delete | http://localhost:5000/users/<string:username> | Only accessible by Admin | X | Joonas |
| GET | Get user's own information | MeResource.get | http://localhost:5000/me | Gets user's own username, email, future reservations | X | Joonas |
| PATCH | Modify user's own information | MeResource.patch | http://localhost:5000/me | User can modify their own username or email | X | Joonas |
| DELETE | Delete user's own account | MeResource.delete | http://localhost:5000/me | Delete user's own account | X | Joonas |
| GET | Get all reservations | ReservationListResource.get | http://localhost:5000/reservations | Displays all reservations | X | Henna, Joonas, Atte |
| POST | Create a reservation | ReservationListResource.post | http://localhost:5000/reservations | Only for logged in users | X | Henna, Joonas |
| GET | Get user's own information | ReservationMeResource.get | http://localhost:5000/reservations/me | Displays logged in user's own reservations | X | Henna |
| GET | Get all reservations by workspace id | ReservationWorkspaceResource.get | http://localhost:5000/reservations/<int:workspace_id> | Only for logged in users | X | Henna |
| DELETE | Delete user's own reservation by ID | ReservationResource.delete | http://localhost:5000/reservations/<int:reservation_id> | User can delete their own reservation | X | Henna |
| POST | Create a json web token | TokenResource.post | http://localhost:5000/token |  | X |  |
| POST | Create a refresh token | RefreshResource.post | http://localhost:5000/refresh |  | X |  |
| POST | Blacklists token for logout | RevokeResource.post | http://localhost:5000/revoke |  | X |  |


Other tasks:

| Task | Done by |
|-|-|
| working with git and github | Everyone |
| End point design | Everyone |
| models, schemas | Joonas, Henna, Atte |
| code testing | Timo, Joonas, Atte, Henna |
| meeting attendance | Everyone |
| readme file | Henna, Joonas |
| End point design table | Henna |



Self assessment for points:  
  
All minimum requirements filled: 15/15 points  
Login functionality +5 points  
Data validation with marshmallow +5 points  
MVC architectural pattern followed +5 points  
Project managed and developed with Git and GitHub +5 points  

Total points: 35/35  
