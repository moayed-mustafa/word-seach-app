


from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm


auth_BP = Blueprint('auth_blueprint', __name__,
                    template_folder='templates/auth',
                    static_folder='static')

@auth_BP.route('/signup')
def signup():
    form = SignupForm()

    return render_template('/signup.html', form)
# ===============================================================================================

@auth_BP.route('/login')
def login():
    return render_template('/login.html')
