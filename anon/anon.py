



from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

anon_BP = Blueprint('anon_blueprint', __name__,
                    template_folder='templates/anon',
                    static_folder='static',
                    static_url_path='/anon/static'
                    )

@anon_BP.route('/anon')
def anon_search():
    """ sends a guest user to the search page """
    return render_template('search.html')