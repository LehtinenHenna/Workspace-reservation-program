Workspace booking system

We made a workspace booking system as a group project for our application programming course.
Members of our group: Joonas, Atte, Henna, Timo, Roni. 
All code is based on the book Python API Development Fundamentals by Jack Chan, Ray Chung and Jack Huang.

Here's some information about the project:

-	Workspaces can only be booked between 16 and 21 o'clock

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



-	When a user is making a reservation, the program checks that there are no overlapping reservations

-	A user should only see future reservations
 


- Admin user: Let's create a user with the name "admin" in the database, the program will check if current_user=="admin" before it gives the user admin rights. Only an admin can:   
    o   create new workspaces / modify existing workspaces / delete workspaces  
    o   look at information about all users or about a specific user, modify any user's information or delete any user account
      

- Basic user can:  
    o   create a user account 
    o   log in  
    o   create a reservation 
    o   look up all future reservations made by anyone and all their own reservations 
    o   look up reservations based on workspace name 
    o   delete their own future reservation
    o   look up all workspaces or a specific workspace 
    o   look up / modify / delete their own user account
  


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


-   To use this program one must install PostgreSQL and create a database: 
    Once PostgreSQL is installed open pgAdmin. 
    Create a 'Login/Group Role' and give it a username in the 'General' tab and a password in the 'Definition' tab. In the 'Privileges'
    tab change the 'Can login?' option to 'yes'. Then create a database, and make the owner of that database the user you just created.
    Give the database also a name.

    In the program code in the file config.py in SQLALCHEMY_DATABASE_URI definition, replace username:password with the ones 
    you just created for the Login/Group Role and database_name with the name of the database you just created. 
    To create the tables for the database, go to the terminal in your programming environment and run first the command flask db init
    to initialize the database. Then run the command flask db migrate. Finally, run the command flask db upgrade.
    If everything worked like it should, you should now see the tables in your database when you look at it in pgAdmin.
    More detailed instructions can be found from the book Python API Development Fundamentals.

-   All required packages are listed in requirements.txt

-   We did all testing for this project with Postman.
