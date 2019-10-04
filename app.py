from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.Contractor
playlists = db.users

@app.route('/')
def index():
    """Return homepage."""
    return render_template('users_index.html', msg='Flask is Cool!!')

if __name__ == '__main__':
    app.run(debug=True)
