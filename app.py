import os
import random

from flask import Flask, redirect, render_template, request, session
from replit import db

app = Flask(__name__)
app.secret_key = os.environ.get('CONNECSHUNS_SECRET_KEY')

db['categories'] = [{
    'level': 1,
    'category': 'Christmas Movies',
    'words': ['Die Hard', 'Elf', 'Gremlins', 'Love Actually']
}, {
    'level': 2,
    'category': 'Letters Starting with A',
    'words': ['A', 'A', 'A', 'A']
}, {
    'level': 3,
    'category': 'Words Used in Programming',
    'words': ['Hello', 'Foo', 'World', 'Bar']
}, {
    'level': 4,
    'category': 'Non-Christmans Red Things',
    'words': ['Pimple', 'Blood', 'Mars', 'Code']
}]

source_words = [
    word for category in db['categories'] for word in category['words']
]

db['words'] = [('word' + str(idx), word)
               for idx, word in enumerate(source_words)]


@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


@app.route('/')
def index():
    if session.get('mistakes_remaining') is None:
        session['mistakes_remaining'] = 4
    if session.get('player_words') is None:
        session['player_words'] = random.sample(db['words'], 
                                                len(db['words']))
    return render_template('index.html',
                           words=session['player_words'],
                           mistakes_remaining=session['mistakes_remaining'])


@app.route('/check-tiles', methods=['GET', 'POST'])
def check_tiles():
    mistakes_remaining = session.get('mistakes_remaining')
    
    previous_guesses = session.get('previous_guesses')
    if previous_guesses is None:
        previous_guesses = []
        
    words = session.get('player_words')
    
    guessed_categories = session.get('guessed_categories')
    if guessed_categories is None:
        guessed_categories = []
    
    post_vals=[x[1] for x in list(request.form.items()) 
                if x[1] != '']
    previous_guesses.append(post_vals)
    session['previous_guesses'] = previous_guesses
    
    word_lists = [x['words'] for x in db['categories']]

    match = -1
    for idx,word_list in enumerate(word_lists):
        if all(item in word_list for item in post_vals):
            match = idx
            break
    if match != -1:
        category = db['categories'][match]    
    print(post_vals)

    
    if session['previous_guesses'] is None:
        session['previous_guesses'] = [post_vals]
        

    return 'foo'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
