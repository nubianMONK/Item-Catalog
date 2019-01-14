# Item Catalog
---
An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
# Design
---
The design implemented is based on the architectural pattern, MVC. 
- **Model:** This has been achieved by the creation of a Restful API which helps with all CRUD operations (Business Logic) against the backend database (PostgreSQL). 

- **Controller:** In tandem with routes helps pass data to the view ( Gate Keeper between the Model and View; Controller Logic)
- **View:** renders the requested information in HTML format to the browser(Presentation Logic). As this is a Flask application the Jinja2 templating engine has been leveraged.

Authentication and Authorization:
- OAUTH2 has been implemented by leveraging the Google OAUTH2 API

# How to Run Tool
---
#### Prerequisites
BackEnd Database:
- PostgreSQL
- Flask and numerous extensions

Step 0:
### Install Flask and extensions
Run the following within the project's root folder:

***Command Line run:*** 

```pip install -r requirements.txt```

Step 1:
### Create Database Schema:
Issue the following within psql shell:

```CREATE DATABASE catalog;```

Step 2: 
### Create catalog database tables:
Run the following python script, within the project's root folder:

***Command Line:***
```python create_catalog_db_tables.py```
 
 Which creates the following tables:
- users
- items
- categories
- flask_dance_oauth



Step 3:
### Set the following environment variables
> **Note:**
The following instructions are all done from the command line, but all these can equally be made within the config.py file, based on the instance of choice (Development, Test, Production). **Application runs in Development instance mode by default.**
- Set SQLALCHEMY_DATABASE_URI:

    ```export **SQLALCHEMY_DATABASE_URI**=*'postgresql+psycopg2://vagrant:vagrant@localhost/'```* **without any DATABASE name.**
    
 >Note: DATABASE name is already set as 'catalog' by default via a DATABASE environment variable.

- Google OAUTH API: **NO ACTION NECESSARY**

  However if you are running in Production do the following:

      export OAUTHLIB_INSECURE_TRANSPORT=1
      export OAUTHLIB_RELAX_TOKEN_SCOPE=1
      
 - To change the default configured Google OAuth Client Id and Client Secret, do the following:
 
       export GOOGLE_OAUTH_CLIENT_ID='To your client ID'
       export GOOGLE_OAUTH_CLIENT_SECRET='To your client SECRET'
       
   If above is changed you will also need to set the following within your Google OAuth 2.0  Client ID profile:
   
      - **authorized redirect URIs:**
      
           - <http://localhost:8000/login/google/authorized> or <https://localhost:8000/login/google/authorized> for https (change port number to what you've setup)


- Catalog RESTful API:
  
  The Catalog RESTful API service built for the application by default,
  is set to the **following Address: http://localhost:8001**. If there is a need to change,
  this can be achieved via the **API_ADDRESS** environment variable:

  - `export API_ADDRESS='Address of your choosing'` Caveat, the port must differ from that of core application

  >Note: Environment Instance: 
  Application by default runs a Development instance and if there's need to change that, set the following environment prior to any other environment variables mentioned above.
  export FLASKENV=config.ProductionConfig for Production and for Test export FLASKENV=config.TestConfig


## Application Launch:
### Execute in the following sequence:

**Catalog RESTful API**, a prerequisite leveraged by the Core Item Catalog Application:
- **Command Line:** ```python runner_api.py runserver```

The above will be running on **http://0.0.0.0:8001**
- To change run the following :
  - **Command Line:** `python runner_api.py runserver` **-h** 'provide your host address of choice' **-p** 'your port number of choice'

  
**Core Application:**
- **Command Line:** ```python runner.py runserver```

This will be running on **http://0.0.0.0:8000**
likewise just as running the API the host and port details can be changed, as described above. Navigate to **http://localhost:8000** to access the application.


## Note:
You are unable to carry out any CUD(Create. Edit. Delete) functionality until you are authenticated and logged into the system.