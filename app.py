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
current_users = db.current_users


@app.route('/')
def users_index():
    user_id = current_users.find()
    print(f"User id is {user_id}")
    current_user = None
    if user_id == None:
        current_user = users.find_one({'_id': ObjectId(user_id)})
        print(f"User id is {current_user}") 
    
    return render_template('users_index.html', current_user = current_user, users = users.find())

@app.route('/users/new') #NEW
def userss_new():
    return render_template('users_new.html', user = {}, title = 'New User')

@app.route('/users', methods=['POST']) #SUBMIT
def users_submit():
    user = {
        'user_name': request.form.get('user_name'),
        'user_description': request.form.get('user_description'),
        'user_rating': int(request.form.get('user_rating')),
        'user_image': request.form.get('user_image'),
        'user_linkedin': request.form.get('user_linkedin'),
        'user_facebook': request.form.get('user_facebook'),
        'user_github': request.form.get('user_github')
    }
    user_id = users.insert_one(user).inserted_id
    return redirect(url_for('users_show', user_id = user_id))

@app.route('/users/<user_id>') #SHOW
def users_show(user_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    return render_template('users_show.html', user = user)

@app.route('/users/<user_id>/edit') #EDIT
def users_edit(user_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    return render_template('users_edit.html', user=user, title = 'Edit User')

@app.route('/users/<user_id>', methods=['POST']) #Submit the UPDATED user
def users_update(user_id):
    updated_user = {
        'user_name': request.form.get('user_name'),
        'user_description': request.form.get('user_description'),
        # 'videos': request.form.get('videos').split()
        'user_rating': int(request.form.get('user_rating')),
        'user_image': request.form.get('user_image'),
        'user_linkedin': request.form.get('user_linkedin'),
        'user_facebook': request.form.get('user_facebook'),
        'user_github': request.form.get('user_github')
    }
    users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_user})
    return redirect(url_for('users_show', user_id=user_id))

@app.route('/users/<user_id>/delete', methods=['POST']) #DELETE
def users_delete(user_id):
    users.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('users_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))