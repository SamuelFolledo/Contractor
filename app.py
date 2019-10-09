from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host = f'{host}?retryWrites=false')
db = client.get_default_database()
users = db.users
projects = db.projects

current_user = {"_id":"", "user_username":"", "user_first_name":"", "user_last_name":"", "user_password":"", "user_favorites": [], "user_listings":[]}

@app.route('/')
def index():
    return render_template('projects_index.html', current_user = current_user, projects = projects.find())

########################################### USERS ###########################################
@app.route('/user/new') #USER NEW
def user_register():
    return render_template('user_register.html', current_user = {}, title = 'New User')

@app.route('/user', methods=['POST']) #USER SUBMIT
def user_submit():
    username = request.form.get('user_username') #add @ before username to know that it is a username
    password = request.form.get('user_password')
    confirm_password = request.form.get('user_confirm_password')
    user = {
        'user_username': username,
        'user_first_name': request.form.get('user_first_name'),
        'user_last_name': request.form.get('user_last_name'),
        'user_password': password,
        'user_confirm_password': confirm_password
    }
    #Error handling
    # if username
    if username[0] == "@":
        return render_template('user_register.html', username_error = True, error_message = "Invalid username: cannot start with '@'", current_user = user, title = 'New User')
    if password != confirm_password:
        return render_template('user_register.html', password_error = True, error_message = "Password and Confirm password does not match", current_user = user, title = 'New User')

    

    username = insert_at_symbol(username) #insert @ to username
    user_id = users.insert_one(user).inserted_id
    current_user= {"_id":user_id, "user_username":username}
    return redirect(url_for('index', current_user = current_user, user_id = user_id))

def fetch_user(username):
    user = users.find_one({"user_username": username})

def insert_at_symbol(username): #user's helper method that inserts @ symbol to a username
    return username[:0]+"@"+username[0:]

def remove_at_symbol(username): #user's helper method that removes @ symbol to a username
    return username[1:]

########################################### PROJECTS ########################################### 
@app.route('/projects/new') #NEW
def projects_new():
    return render_template('projects_new.html', current_user = current_user, project = {}, title = 'New Project')

@app.route('/projects', methods=['POST']) #SUBMIT
def projects_submit():
    project = {
        'project_name': request.form.get('project_name'),
        'project_description': request.form.get('project_description'),
        'project_rating': int(request.form.get('project_rating')),
        'project_image': request.form.get('project_image'),
        'project_linkedin': request.form.get('project_linkedin'),
        'project_facebook': request.form.get('project_facebook'),
        'project_github': request.form.get('project_github')
    }
    project_id = projects.insert_one(project).inserted_id
    return redirect(url_for('projects_show', current_user = current_user, project_id = project_id))

@app.route('/projects/<project_id>') #SHOW
def projects_show(project_id):
    project = projects.find_one({'_id': ObjectId(project_id)})
    return render_template('projects_show.html', current_user = current_user, project = project)

@app.route('/projects/<project_id>/edit') #EDIT
def projects_edit(project_id):
    project = projects.find_one({'_id': ObjectId(project_id)})
    return render_template('projects_edit.html', current_user = current_user, project=project, title = 'Edit project')

@app.route('/projects/<project_id>', methods=['POST']) #Submit the UPDATED project
def projects_update(project_id):
    updated_project = {
        'project_name': request.form.get('project_name'),
        'project_description': request.form.get('project_description'),
        # 'videos': request.form.get('videos').split()
        'project_rating': int(request.form.get('project_rating')),
        'project_image': request.form.get('project_image'),
        'project_linkedin': request.form.get('project_linkedin'),
        'project_facebook': request.form.get('project_facebook'),
        'project_github': request.form.get('project_github')
    }
    projects.update_one(
        {'_id': ObjectId(project_id)},
        {'$set': updated_project})
    return redirect(url_for('projects_show', current_user = current_user, project_id=project_id))

@app.route('/projects/<project_id>/delete', methods=['POST']) #DELETE
def projects_delete(project_id):
    projects.delete_one({'_id': ObjectId(project_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))