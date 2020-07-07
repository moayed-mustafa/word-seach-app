from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g, url_for, json
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Word, List
# from forms import UserEditForm

api_BP = Blueprint('api_blueprint', __name__)

@api_BP.route('/add-word', methods=['POST'])
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
@api_BP.route('/delete-word', methods=['POST'])
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
        if word and word in g.user.words:
            # db.session.delete(word)
            g.user.words.remove(word)
            db.session.delete(word)
            db.session.commit()
            return 'Word Removed!'


        return ('word Not found', 202)
# =============================================================================
@api_BP.route('/user-exists')
def user_or_guest():
    if g.user:
        return 'User'
    return ('Guest', 202)
# =============================================================================
# check if a word is in the user's list
@api_BP.route('/find-word', methods=["POST"])
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
