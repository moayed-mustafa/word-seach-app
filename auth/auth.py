


from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
# blueprint_one = Blueprint('test_blueprint_one', __name__,
#     template_folder='templates/blueprint_one',
#     static_folder='static');

auth_BP = Blueprint('auth_blueprint', __name__,
                    template_folder='templates/auth',
                    static_folder='static')

@auth_BP.route('/signup')
def signup():
    return render_template('/signup.html')
# ===============================================================================================

@auth_BP.route('/login')
def login():
    return render_template('/login.html')
