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
carts = db.carts
listings = db.listings
offers = db.offers

current_user = {"_id":"", "user_username":"", "user_first_name":"", "user_last_name":"", "user_password":"", "user_cart_id": "", "user_listings_id":"", "is_admin":False}


@app.route('/')
def index():
    return render_template('projects_index.html', current_user = current_user, projects = projects.find())

########################################### USERS ###########################################
@app.route('/home/<user_id>')
def user_home(user_id): #USER HOME
    current_user = users.find_one({'_id': ObjectId(user_id)})
    print(f"CURRENT USER IN HOME IS {current_user}")
    return render_template('projects_index.html', current_user = current_user, projects = projects.find())

@app.route('/user', methods=['POST']) #USER SUBMIT LOGIN/REGISTER
def user_submit():
    username = request.form.get('user_username').lower()
    password = request.form.get('user_password')
    
    if request.form.get('is_login') == None: #REGISTER
        confirm_password = request.form.get('user_confirm_password')
        first_name = request.form.get('user_first_name')
        last_name = request.form.get('user_last_name')
        user = {
            'user_username': username,
            'user_first_name': first_name,
            'user_last_name': last_name,
            'user_password': password,
            'user_confirm_password': confirm_password
        }
        #Error handling
        if username == "  " or username == " ":
            return render_template('user_register.html', username_error = True, error_message = "Please input a valid value", current_user = user, title = 'Register User')
        if first_name == "  " or first_name == " ":
            return render_template('user_register.html', first_name_error = True, error_message = "Please input a valid value", current_user = user, title = 'Register User')
        if last_name == "  " or last_name == " ":
            return render_template('user_register.html', last_name_error = True, error_message = "Please input a valid value", current_user = user, title = 'Register User')
        if password == "  " or password == " ":
            return render_template('user_register.html', password_error = True, error_message = "Please input a valid value", current_user = user, title = 'Register User')
        if username[0] == "@": #checks if username has @ in the beginning
            return render_template('user_register.html', username_error = True, error_message = "Invalid username: cannot start with '@'", current_user = user, title = 'Register User')
        if users.find({"user_username":username}).count() > 0: #check if username already exists
            return render_template('user_register.html', username_error = True, error_message = "Username already exist", current_user = user, title = 'Register User')
        if password != confirm_password: #check if passwords and confirm pass match
            return render_template('user_register.html', password_error = True, error_message = "Password and Confirm password does not match", current_user = user, title = 'Register User')
        
        cart = {'project_id':[]}
        cart_id = carts.insert_one(cart).inserted_id
        listing = {'project_id':[]}
        listing_id = listings.insert_one(listing).inserted_id
        user['user_cart_id'] = cart_id
        user['user_listings_id'] = listing_id
        user['is_admin'] = False
        user_id = users.insert_one(user).inserted_id #insert user and get the id
        return redirect(url_for('user_home', user_id = user_id)) 
    
    else: #LOGIN USER
        user = {
            'user_username': username,
            'user_password': password
        }
        #Error handling
        if username == "  " or username == " ":
            return render_template('user_login.html', username_error = True, error_message = "Please input a valid value", current_user = user, title = 'Login')
        if password == "  " or password == " ":
            return render_template('user_login.html', password_error = True, error_message = "Please input a valid value", current_user = user, title = 'Login')
        if username[0] == "@": #checks if username has @ in the beginning
            return render_template('user_login.html', username_error = True, error_message = "Invalid username: cannot start with '@'", current_user = user, title = 'Login')
        
        cursor = users.find({"user_username":username})
        if cursor.count() < 1: #check if username does not exist
            return render_template('user_login.html', username_error = True, error_message = "Username does not exist", current_user = user, title = 'Login')

        for doc in cursor:
            if doc['user_password'] != password:
                return render_template('user_login.html', password_error = True, error_message = "Incorrect password", current_user = user, title = 'Login')
            current_user['_id'] = doc['_id']
            current_user['user_username'] = doc['user_username']
            current_user['user_first_name'] = doc['user_first_name']
            current_user['user_last_name'] = doc['user_last_name']
            current_user['user_password'] = doc['user_password']
            current_user['user_cart_id'] = doc['user_cart_id']
            current_user['user_listings_id'] = doc['user_listings_id']
            current_user['is_admin'] = doc['is_admin']
        return redirect(url_for('user_home', user_id = current_user['_id']))
    return render_template('user_login.html', username_error = True, error_message = "Incorrect username or password", current_user = current_user, title = 'Login')

@app.route('/register') #USER REGISTER - NEW
def user_register():
    current_user = {"_id":"", "user_username":"", "user_first_name":"", "user_last_name":"", "user_password":"", "user_cart_id": "", "user_listings_id":"", "is_admin":False}
    return render_template('user_register.html', current_user = current_user, title = 'Register User')

@app.route('/login') #USER LOGIN - READ
def user_login():
    current_user = {"_id":"", "user_username":"", "user_first_name":"", "user_last_name":"", "user_password":"", "user_cart_id": "", "user_listings_id":"", "is_admin":False}
    return render_template('user_login.html', current_user = current_user, title = 'Login User')

@app.route('/user/<user_id>/edit') #USER EDIT - UPDATE
def user_edit(user_id):
    current_user = users.find_one({'_id': ObjectId(user_id)})
    return render_template('user_edit.html', current_user = current_user, title = 'Update User')

@app.route('/user/<user_id>', methods=['POST']) #Submit the UPDATED user
def user_update(user_id):

    ########################
    username = request.form.get('user_username').lower()
    password = request.form.get('user_password')
    first_name = request.form.get('user_first_name')
    last_name = request.form.get('user_last_name')
    user = {
        'user_username': username,
        'user_first_name': first_name,
        'user_last_name': last_name,
        'user_password': password,
        'is_admin': False
    }
    #Error handling
    user_admin_password = request.form.get('user_admin_password','') #for admin
    if user_admin_password == "admin!":
        user['is_admin'] = True
    elif user_admin_password == "" or user_admin_password == " ":
        user['is_admin'] = False
    else: 
        return render_template('user_edit.html', admin_error = True, error_message = "Please input a password or leave it blank", current_user = user, title = 'Update User')

    if username == "  " or username == " ":
        return render_template('user_edit.html', username_error = True, error_message = "Please input a valid value", current_user = user, title = 'Update User')
    if first_name == "  " or first_name == " ":
        return render_template('user_edit.html', first_name_error = True, error_message = "Please input a valid value", current_user = user, title = 'Update User')
    if last_name == "  " or last_name == " ":
        return render_template('user_edit.html', last_name_error = True, error_message = "Please input a valid value", current_user = user, title = 'Update User')
    if password == "  " or password == " ":
        return render_template('user_edit.html', password_error = True, error_message = "Please input a valid value", current_user = user, title = 'Update User')
    if username[0] == "@": #checks if username has @ in the beginning
        return render_template('user_edit.html', username_error = True, error_message = "Invalid username: cannot start with '@'", current_user = user, title = 'Update User')
    if users.find({"user_username":username}).count() > 0: #check if username already exists
        return render_template('user_edit.html', username_error = True, error_message = "Username already exist", current_user = user, title = 'Update User')
    print(f"USER WE ARE UPDATING IS {user}")
    cursor = users.find({"user_username":username})
    if cursor.count() < 1: #check if username does not exist
        return render_template('user_edit.html', username_error = True, error_message = "Username does not exist", current_user = user, title = 'Login')

    for doc in cursor:
        user['_id'] = doc['_id']
        user['user_cart_id'] = doc['user_cart_id']
        user['user_listings_id'] = doc['user_listings_id']
    print(f"USER WE UPDATED IS {user}")
    return redirect(url_for('user_home', user_id = user['_id']))
    

    ########################
    updated_user = {
        'project_name': request.form.get('project_name'),
        'project_description': request.form.get('project_description'),
        'project_rating': int(request.form.get('project_rating')),
    }
    users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_user})
    return redirect(url_for('user_home', current_user = current_user, user_id=user_id))


def insert_at_symbol(username): #user's helper method that inserts @ symbol to a username
    return username[:0]+"@"+username[0:]

def remove_at_symbol(username): #user's helper method that removes @ symbol to a username
    return username[1:] #return username without first character

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
        'project_image_file': request.form.get('project_image_file'),
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
    project_offers = offers.find({'projects_id':ObjectId(project_id)})
    return render_template('projects_show.html', current_user = current_user, project = project, offers=project_offers)

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
        'project_image_file': request.form.get('project_image_file'),
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


########################################### OFFERS ROUTES ###########################################

@app.route('/projects/offers', methods=['POST'])
def offers_new():
    """Submit a new offer."""
    offer = {
        'price': request.form.get('price'),
        'description': request.form.get('description'),
        'project_id': ObjectId(request.form.get('project_id'))
    }
    print(offer)
    offer_id = offers.insert_one(offer).inserted_id
    return redirect(url_for('projects_show', project_id=request.form.get('project_id')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))