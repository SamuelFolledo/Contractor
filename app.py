from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.Contractor
users = db.users

@app.route('/')
def users_index():
    return render_template('users_index.html', msg='Flask is Cool!!')

@app.route('/users/new') #NEW
def playlists_new():
    return render_template('users_new.html')

@app.route('/users', methods=['POST']) #SUBMIT
def playlists_submit():
    user = {
        'user_name': request.form.get('user_name'),
        'user_description': request.form.get('user_description')
    }
    users.insert_one(user)
    return redirect(url_for('users_index'))

if __name__ == '__main__':
    app.run(debug=True)
