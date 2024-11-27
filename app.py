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
    'category': 'Non-Christmas Red Things',
    'words': ['Pimple', 'Blood', 'Mars', 'Code']
}]

source_words = [
    word for category in db['categories'] for word in category['words']
]

db['words'] = [('word' + str(idx), word)
               for idx, word in enumerate(source_words)]


@app.route('/')
def index():
    if not session.get('mistakes_remaining'):
        session['mistakes_remaining'] = 4
    if not session.get('player_words'):
        player_words = [tuple(word.value) for word in db['words']]
        random.shuffle(player_words)
        session['player_words'] = player_words
    if not session.get('guessed_categories'):
        session['guessed_categories'] = []
    return render_template('index.html',
                           words=session['player_words'],
                           mistakes_remaining=session['mistakes_remaining'],
                           guessed_categories=session['guessed_categories'],
                           current_guesses=[])


@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


@app.route('/shuffle', methods=['POST'])
def shuffle():
    player_words = session['player_words']
    random.shuffle(player_words)
    session['player_words'] = player_words

    return render_template('word_tile_board.html',
                           words=session['player_words'],
                           mistakes_remaining=session['mistakes_remaining'],
                           guessed_categories=session['guessed_categories'],
                           current_guesses=[])


@app.route('/check-tiles', methods=['GET', 'POST'])
def check_tiles():
    mistakes_remaining = session.get('mistakes_remaining')
    previous_guesses = session.get('previous_guesses')
    if previous_guesses is None:
        previous_guesses = []
    guessed_categories = session.get('guessed_categories')
    print("Guessed categories", guessed_categories)
    if guessed_categories is None:
        guessed_categories = []
    words = session['player_words']

    current_guesses = [
        x[0] for x in list(request.form.items()) if x[1].strip() != ''
    ]

    for previous_guess in previous_guesses:
        if all(item in current_guesses for item in previous_guess):
            message = "Already guessed."
            return render_template('word_tile_board.html',
                                   words=session["player_words"],
                                   mistakes_remaining=mistakes_remaining,
                                   current_guesses=current_guesses,
                                   guessed_categories=guessed_categories,
                                   message=message)
    previous_guesses.append(current_guesses)
    session['previous_guesses'] = previous_guesses

    current_words = [x[1] for x in db['words'] if x[0] in current_guesses]
    word_lists = [x['words'] for x in db['categories']]
    match = -1
    category = None
    count = 0
    message = None
    flash = False
    for idx, word_list in enumerate(word_lists):
        sorted(word_list)
        sorted(current_words)
        cur_count = sum(1 for l_idx, item in enumerate(word_list)
                        if current_words[l_idx] == word_list[l_idx])
        if cur_count > count:
            count = cur_count
        if all(item in word_list for item in current_words):
            match = idx
            break
    if match != -1:
        category = {}
        flash = True
        for key, value in db['categories'][match].items():
            if key != 'words':
                category[key] = value
            else:
                category[key] = ", ".join(
                    [x for x in db['categories'][match]['words']])
        guessed_categories.append(category)
        session['guessed_categories'] = guessed_categories
        words = [
            x for x in session['player_words'] if x[0] not in current_guesses
        ]
        session['player_words'] = words
    else:
        mistakes_remaining -= 1
        session['mistakes_remaining'] = mistakes_remaining
        if mistakes_remaining == 0:
            message = 'No milk and cookies for you!'
        else:
            message = "One away..." if count == 3 else "Bah! Humbug!"

    if len(words) == 0:
        if mistakes_remaining == 4:
            message = "Ho! Ho! Ho!"
        elif mistakes_remaining == 3:
            message = "You got your wings!"
        elif mistakes_remaining == 2:
            message = "Good job Cindy Lou Who!"
        elif mistakes_remaining == 1:
            message = "Fra-jee-lay"

    return render_template('word_tile_board.html',
                           words=words,
                           mistakes_remaining=mistakes_remaining,
                           current_guesses=current_guesses,
                           match=match,
                           guessed_categories=guessed_categories,
                           flash=flash,
                           message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
