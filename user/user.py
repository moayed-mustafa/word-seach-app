


from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension

user_BP = Blueprint('user_blueprint', __name__,
                    template_folder='templates/user',
                    static_folder='static')

@user_BP.route('/list/<int:id>/user')
def user_profile(id):
    # you want to check the user associated words
    # if you find words then render the html page with a user list of words
    #  else: redirect to the search function
    # a of now, redirect to the search page right away since we have no user words nor a words table
    return redirect(url_for('user_blueprint.user_search', id=g.user.id))
    # return render_template('user.html')

@user_BP.route('/search/<int:id>/user')
def user_search(id):

    return render_template('search.html')