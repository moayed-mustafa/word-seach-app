


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
def user_profile(id):
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
# check if a word is in the user's list
@user_BP.route('/find-word', methods=["POST"])
def find_word_in_user_list():
    """
    Recieves a word definition from the client and checks
    in the user's list if a word with such definition exists
    """
    data = request.get_json()
    word = Word.query.filter(Word.definition==data['definition']).first()
    if word != None and word in g.user.words:
        return 'Found'

    return ('Not Found', 204)

# =============================================================================

@user_BP.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
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
            user.bio = form.bio.data

            db.session.commit()
            return redirect(url_for('homepage'))

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form)
# =============================================================================


                        #User api routes
@user_BP.route('/add-word', methods=['POST'])
def add_word_to_user_list():
    """ recieves a Json containtg the word details from the frontEnd and addes the word to
        the list of words belonging to the current user.
    """
    if g.user == None:
        return ('Error')

    else:

        data = request.get_json()

        if "synonyms" not in data["info"]:
            syn = Word.synonym.default.arg
        else:
            syn = data["info"]["synonyms"][0]

        if "examples" not in data["info"]:
            example = Word.example.default.arg
        else:
            example = data["info"]["examples"][0]

        word = Word(word=data["word"],
        definition=data["info"]["definition"],
        part_of_speech=data["info"]["partOfSpeech"],
        synonym=syn,
        example=example)

        db.session.add(word)
        db.session.commit()
        user_id = g.user.id
        user_word = List(user_id= user_id, word_id=word.id)
        db.session.add(user_word)

        db.session.commit()
        return ('Word created and appended to user list', 201)
# =============================================================================

# '/delete-word'
@user_BP.route('/delete-word', methods=['POST'])
def delete_word_from_user_list():
    """ recieves a request the word details from the frontEnd and addes the word to
        the list of words belonging to the current user.
    """
    if g.user == None:
        return ('Error')

    else:
        definition = request.json['definition']
        # get the word by definition
        word = Word.query.filter_by(definition=definition).first()
        print(word)
        if word and word in g.user.words:
            # db.session.delete(word)
            g.user.words.remove(word)
            db.session.delete(word)
            db.session.commit()
            return 'Word Removed!'


        return ('word Not found', 202)
# =============================================================================
@user_BP.route('/user-exists')
def user_or_guest():
    if g.user:
        return 'User'
    return ('Guest', 202)