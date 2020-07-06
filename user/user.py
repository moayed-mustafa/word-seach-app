


from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g, url_for, json
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Word, List
from forms import UserEditForm

user_BP = Blueprint('user_blueprint', __name__,
                    template_folder='templates/user',
                    static_folder='static')
# =============================================================================
        # edit user
@user_BP.route('/profile/<int:id>/user',methods=["GET", "POST"])
def user_profile_edit(id):
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect(url_for('homepage'))

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data

            db.session.commit()
            return redirect(url_for('homepage'))

        flash("Wrong password, please try again.", 'danger')
    return render_template('user_profile.html', form=form)
# =============================================================================

@user_BP.route('/list/<int:id>/user')
def user_list(id):
    """ shows the words the user has chosen to save to their list
    """
    user = User.query.get_or_404(id)
    list = user.words

    return render_template('user_list.html', list=list)
# =============================================================================
@user_BP.route('/search/<int:id>/user')
def user_search(id):
    """ serves the main functionality of the app, searching
        for a specific word in the english language and returning
        a bunch of words with the definition, pronunciation
        part of speech of the word in addition to examples and synonyms of the word.

    """

    return render_template('search.html')

# =============================================================================
