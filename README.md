## Steps to set up the project:

### Local setup

* create a virtual environment and activate it
* install all the requirements 
    > pip install -r requirements.txt
* Do the migrations
    > python manage.py makemigrations
* and now time to migrate the changes
    > python manage.py migrate
* then run the server
    > python manage.py runserver
* To Access all the APIs on swagger
    > localhost:8000/api-doc/
* to create the admin run below command and provide email password etc
    > python manage.py createsuperuser
* To check the data please visit to admin panel of django by providing username and password
    > localhost:8000/admin/

* Postman collection link
    > https://www.postman.com/material-meteorologist-52102999/workspace/social-media/collection/36298622-fc9ee01a-7ddc-4060-b067-7da00ddd776d?action=share&creator=36298622

* For any assistance for setting up the project feel free to reach me on my below email id
    > shubhksj1@gmail.com