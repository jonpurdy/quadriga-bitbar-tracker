from flask import Flask

app = Flask(__name__)
#from app import views

from app.mod_arbcalc.arbcalc import get_all_spreads as get_all_spreads

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')

def index():
    spreads, title = get_all_spreads()
    user = {'nickname': ' '}  # fake user
    return render_template('index.html',
                           title=title,
                           user=user,
                           spreads=spreads)
