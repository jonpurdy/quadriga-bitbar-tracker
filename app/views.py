from flask import render_template
from app import app

@app.route('/')
@app.route('/index')

def index():
    spreads = get_all_spreads2()
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
   