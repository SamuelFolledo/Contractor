# Welcome to [Contractor](https://folledo-contractor.herokuapp.com)

### What is Contractor?
Contractor is an e-commerce website where users can sell their projects (iOS, Android, Website) following the CRUD principle which allow users to create, read, update, delete users and projects. This website is written in Python, utilizes Flask and Jinja2 for templating, MongoDB as its database, Heroku as the web server, and Bootstrap for basic styling.

## Link to [Contractor](https://folledo-contractor.herokuapp.com) while live
https://folledo-contractor.herokuapp.com

## Screenshots
### Welcome Screen
<img src="/static/photos/welcome_page.PNG" width="621" height="350">
---

### User Login in Mobile
<img src="https://github.com/SamuelFolledo/Contractor/blob/master/static/photos/mob_login_user.png" width="536" height="726">

### User Register in Mobile
<img src="https://github.com/SamuelFolledo/Contractor/blob/master/static/photos/mob_register_user.png" width="536" height="726">
---


### Welcome Screen
<img src="/static/photos/welcome_page.PNG" width="621" height="350">
---



## To Run Locally
- __With Python installed, create a virtual environment__
```
$ cd contractor
$ python3 -m venv env
```
- __Activate the newly created virtual environment to install Python packages__
```
$ source env/bin/activate
```
- __Make sure Flask is installed in the virtual environment to get started with the project__
```
(env) $ pip3 install flask
```
- __To install packages from a requirements.txt file:__ 
```
$ pip3 install -r requirements.txt
```
- __To run the project__ 
```
(env) $ export FLASK_ENV=development; flask run
```
===============================


## Relevant Links
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) to build the web
- [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) for templating
- [MongoDB](https://www.mongodb.com)
- [PyMongo](https://api.mongodb.com/python/current/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
- [Heroku](https://heroku.com)
- [Make School Courses](https://www.makeschool.com/academy)
- [Playlister Tutorial](https://www.makeschool.com/academy/track/playlistr-video-playlists-with-flask-and-mongodb-1c)
- [My Playlister Repo](https://github.com/SamuelFolledo/Playlister)
- [BEW1.1 Contractor Project Instructions](https://docs.google.com/document/d/1C8eOyLBeGMKJ2y50QwLU5tWjNb2JVcpAE4khUBIfm0U/edit#)