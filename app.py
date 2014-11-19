# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, \
    request, session, flash, g
from functools import wraps
import sqlite3
# create the application object
app = Flask(__name__)

app.secret_key = "my precious"
app.database = "flaskIntro.db"

# def connect_db():
#     return sqlite3.connect(app.database)

# Login require decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    # Following is another way to connect sqlite db
    # posts = []
    # cur = get_db().execute('select * from posts')
    # posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    # close_connection(sqlite3.OperationalError)
    try:
        g.db = connect_db()
        cur = g.db.execute('select * from posts')
        posts_dict= []
        for row in cur.fetchall():
            posts_dict.append( dict(title=row[0], description=row[1]) )
        # posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
        g.db.close()
    except sqlite3.OperationalError:
        flash('You have no database!')
    return render_template('index.html', posts=posts_dict)

# DATABASE= "flaskIntro.db"
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("You are just logged in")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("You are just logged out")
    return redirect(url_for("welcome"))

def connect_db():
    return sqlite3.connect(app.database)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
