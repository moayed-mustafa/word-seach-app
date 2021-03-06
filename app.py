



import os
from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from auth.auth import auth_BP, CURR_USER_KEY
from anon.anon import anon_BP
from user.user import user_BP
from api.api import api_BP

from user.user_model import db, connect_db, Word,User
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.register_blueprint(auth_BP)
app.register_blueprint(anon_BP)
app.register_blueprint(user_BP)
app.register_blueprint(api_BP)

connect_db(app)



@app.before_request
def make_user_global():
    """ add the user to the global variable """
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


@app.route('/')
def homepage():
    """ shows home page """

    if g.user:
        return redirect(url_for('user_blueprint.user_search', id=g.user.id))

    return render_template('home.html')

# =============================================================================
@app.route('/about')
def about():
    """ shows the about page """
    return render_template('about.html')


