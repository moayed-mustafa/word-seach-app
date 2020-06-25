


from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import SignupForm, LoginForm
from models import User, db, connect_db




CURR_USER_KEY = 'current_user'
auth_BP = Blueprint('auth_blueprint', __name__,
                    template_folder='templates/auth',
                    static_folder='static')


        # Utility methods and variables

def login(user):
    session[CURR_USER_KEY] = user.id


def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    # use this to make a custome 404 page
# @app.errorhandler(404)
# def not_found():
#     """Page not found."""
#     return make_response(render_template("404.html"), 404)


# ===========================================================================================
@auth_BP.route('/signup', methods=['GET','POST'])
def signup_route():
    """ take user credintials from the form, hashes the password and signs user up."""
    form = SignupForm()
    if form.validate_on_submit():
        # cls, username, email, password, image_url, gender
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                gender = form.gender.data
            )
            db.session.add(user)
            db.session.commit();
            flash('user has been created', 'success')
            return redirect(url_for('homepage'))
        except IntegrityError:
            flash('Username is already taken', 'danger')
            return render_template('/signup.html', form=form)


    return render_template('/signup.html', form=form)

# ===============================================================================================

@auth_BP.route('/login', methods=['GET', 'POST'])
def login_route():
    """ route for logging the user to the system """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login(user)
            flash(f'welcome {user.username}', 'success')
            # we should take the user to his profile
            return redirect(url_for('homepage'))
        flash('Invalid credintials', 'danger')

    return render_template('/login.html', form=form)

# ===============================================================================================
@auth_BP.route('/logout')
def logout_route():
    # import pdb
    # pdb.set_trace()
    if  not g.user:
        flash('You need to login first', 'warning')
        return redirect(url_for('auth_blueprint.login_route'))

    else:
        logout()
        flash('Logged out successfuly', 'success')
        return redirect(url_for('homepage'))
