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
    if not session.get('mistakes_remaining'):
        session['mistakes_remaining'] = 4
    if not session.get('player_words'):
        session['player_words'] = [tuple(word.value) for word in db['words']]
    return render_template('index.html',
                           words=session['player_words'],
                           mistakes_remaining=session['mistakes_remaining'],
                           current_guesses=[])


@app.route('/check-tiles', methods=['GET', 'POST'])
def check_tiles():
    mistakes_remaining = session.get('mistakes_remaining')

    # previous_guesses = session.get('previous_guesses')
    # if previous_guesses is None:
    #     previous_guesses = []

    # successfully_guessed_categories = session.get(
    #     'successfully_guessed_categories')
    # if not successfully_guessed_categories:
    #     successfully_guessed_categories = []

    current_guesses = [x[0] for x in list(request.form.items()) if x[1].strip() != '']
    # previous_guesses.append(current_guesses)
    # session['previous_guesses'] = previous_guesses

    # word_lists = [x['words'] for x in db['categories']]

    # match = -1
    # for idx, word_list in enumerate(word_lists):
    #     if all(item in word_list for item in current_guesses):
    #         match = idx
    #         break
    # if match != -1:
    #     category = db['categories'][match]

    print(current_guesses)

    return render_template('word_tile_board.html',
                           words=session['player_words'],
                           mistakes_remaining=mistakes_remaining,
                           current_guesses=current_guesses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
