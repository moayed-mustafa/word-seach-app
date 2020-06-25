


from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

user_BP = Blueprint('user_blueprint', __name__,
                    template_folder='templates/user',
                    static_folder='static')

@user_BP.route('/user/<int:id>/list')
def user_profile(id):
    return render_template('user.html')