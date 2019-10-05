from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient()
db = client.Contractor
users = db.users

@app.route('/')
def users_index():
    return render_template('users_index.html', users = users.find())

@app.route('/users/new') #NEW
def userss_new():
    return render_template('users_new.html', user = {}, title = 'New User')

@app.route('/users', methods=['POST']) #SUBMIT
def users_submit():
    user = {
        'user_name': request.form.get('user_name'),
        'user_description': request.form.get('user_description'),
        'user_rating': int(request.form.get('user_rating'))
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
        'user_rating': int(request.form.get('user_rating'))
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
    app.run(debug=True)
