


from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g, url_for, json
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Word

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
# =============================================================================

@user_BP.route('/search/<int:id>/user')
def user_search(id):

    return render_template('search.html')
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
        print(data)
        if "synonyms" not in data["info"]:
            syn = Word.synonym.default.arg
        else:
            syn = data["info"]["synonyms"][0]

        if "examples" not in data["info"]:
            example = Word.example.default.arg
        else:
            example = data["info"]["examples"][0]
        print(data)
    # add word to db

        word = Word(word=data["word"],
        definition=data["info"]["definition"],
        part_of_speech=data["info"]["partOfSpeech"],
        synonym=syn,
        example=example)
        print(word)
        db.session.add(word)
        g.user.words.append(word)
        db.session.commit()
        print(g.user.words)
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
        if word:
            db.session.delete(word)
            db.session.commit()
            print(g.user.words)
            return 'OK!'


        return 'word Not found'