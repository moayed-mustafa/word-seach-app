



from flask import Flask,Blueprint, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

general_BP = Blueprint('general_blueprint', __name__,
                    template_folder='templates/general',
                    static_folder='static')

@general_BP.route('/general')
def test_general():
    return render_template('/general_template.html')