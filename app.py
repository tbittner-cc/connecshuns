import os
import random
import secrets

from flask import Flask, redirect, render_template, request, session
from replit import db

app = Flask(__name__)
app.secret_key = os.environ.get('CONNECSHUNS_SECRET_KEY')

categories = [{
    'level':
    1,
    'category':
    'Christmas Movies',
    'words': [('word1', 'Die Hard'), ('word2', 'Elf'), ('word3', 'Gremlins'),
              ('word4', 'Love Actually')]
}, {
    'level':
    2,
    'category':
    'Letters Starting with A',
    'words': [('word5', 'A'), ('word6', 'A'), ('word7', 'A'), ('word8', 'A')]
}, {
    'level':
    3,
    'category':
    'Words Used in Programming',
    'words': [('word9', 'Hello'), ('word10', 'Foo'), ('word11', 'World'),
              ('word12', 'Bar')]
}, {
    'level':
    4,
    'category':
    'Non-Christmas Red Things',
    'words': [('word13', 'Pimple'), ('word14', 'Blood'), ('word15', 'Mars'),
              ('word16', 'Code')]
}]

db['empty_categories'] = [{
    'level': 1,
    'category': '',
    'words': [('', ''), ('', ''), ('', ''), ('', '')]
}, {
    'level': 2,
    'category': '',
    'words': [('', ''), ('', ''), ('', ''), ('', '')]
}, {
    'level': 3,
    'category': '',
    'words': [('', ''), ('', ''), ('', ''), ('', '')]
}, {
    'level': 4,
    'category': '',
    'words': [('', ''), ('', ''), ('', ''), ('', '')]
}]


@app.route('/')
def index():
    # If you're wondering why I'm mixing and matching the 
    # key/value store vs. the dict, it's due to the fact that
    # the KV store uses non-standard Python data structures.
    if db['categories'] == db['empty_categories']:
        db['categories'] = categories
        
    if session.get('mistakes_remaining') is None:
        session['mistakes_remaining'] = 4

    if session.get('player_words') is None:
        player_words = [(key, val) for category in db['categories']
                        for (key, val) in category['words']]
        random.shuffle(player_words)
        session['player_words'] = player_words

    if session.get('guessed_categories') is None:
        session['guessed_categories'] = []

    if session.get('previous_guesses') is None:
        session['previous_guesses'] = []

    if session.get('guessed_categories') is None:
        session['guessed_categories'] = []

    return render_template('index.html',
                           words=session['player_words'],
                           mistakes_remaining=session['mistakes_remaining'],
                           categories=session['guessed_categories'],
                           current_guesses=[])


@app.route('/words', methods=['GET'])
def words():
    return render_template('create_words.html',categories=db['categories'])

@app.route('/info', methods=['GET'])
def info():
    return render_template('information.html')

@app.route('/delete-all', methods=['POST'])
def delete_all():
    db['categories'] = db['empty_categories']
    return render_template('create_words.html',categories=db['categories'])

@app.route('/update-categories', methods=['POST'])
def update_categories():
    req_vals = list(request.form.items())

    for idx in range(1,5):
        cat_key = f'category{str(idx)}'
        cat_val = [val for (key, val) in req_vals if key == cat_key][0]
        db['categories'][idx-1]['category'] = cat_val
        
        word_key_1 = f'word{str(1 + 4*(idx-1))}'
        word_val_1 = [val for (key, val) in req_vals if key == word_key_1][0]
        db['categories'][idx-1]['words'][0] = (word_key_1, word_val_1)

        word_key_2 = f'word{str(2 + 4*(idx-1))}'
        word_val_2 = [val for (key, val) in req_vals if key == word_key_2][0]
        db['categories'][idx-1]['words'][1] = (word_key_2, word_val_2)

        word_key_3 = f'word{str(3 + 4*(idx-1))}'
        word_val_3 = [val for (key, val) in req_vals if key == word_key_3][0]
        db['categories'][idx-1]['words'][2] = (word_key_3, word_val_3)

        word_key_4 = f'word{str(4 + 4*(idx-1))}'
        word_val_4 = [val for (key, val) in req_vals if key == word_key_4][0]
        db['categories'][idx-1]['words'][3] = (word_key_4, word_val_4)

        new_secret = secrets.token_hex(24)
        os.environ['CONNECSHUNS_SECRET_KEY'] = new_secret
        app.secret_key = os.environ.get('CONNECSHUNS_SECRET_KEY')
        
    return render_template('create_words.html',categories=db['categories'])

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
                           categories=session['guessed_categories'],
                           current_guesses=[])


@app.route('/check-tiles', methods=['GET', 'POST'])
def check_tiles():
    mistakes_remaining = session.get('mistakes_remaining')
    previous_guesses = session.get('previous_guesses')
    guessed_categories = session.get('guessed_categories')
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
                                   categories=guessed_categories,
                                   message=message)
    previous_guesses.append(current_guesses)
    session['previous_guesses'] = previous_guesses

    word_lists = [[word[0] for word in x['words']] for x in db['categories']]
    match = -1
    category = None
    count = 0
    message = None
    flash = False

    for idx, word_list in enumerate(word_lists):
        cur_count = sum(1 for item in word_list if item in current_guesses)
        if cur_count > count:
            count = cur_count
        if all(item in word_list for item in current_guesses):
            match = idx
            break
    if match != -1:
        flash = True
        category = _create_category_entry(match)
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
        message = _get_final_message(mistakes_remaining)

    if mistakes_remaining == 0:
        words = []
        session['player_words'] = words
        guessed_matches = [x['level'] for x in session['guessed_categories']]
        unguessed_matches = [
            # Levels are 1-indexed
            x['level'] - 1 for x in db['categories']
            if x['level'] not in guessed_matches
        ]
        categories = [_create_category_entry(x) for x in unguessed_matches]
        guessed_categories = session['guessed_categories']
        guessed_categories.extend(categories)
        session['guessed_categories'] = guessed_categories

    return render_template('word_tile_board.html',
                           words=words,
                           mistakes_remaining=mistakes_remaining,
                           current_guesses=current_guesses,
                           match=match,
                           categories=guessed_categories,
                           flash=flash,
                           message=message)


def _create_category_entry(match):
    category = {}
    for key, value in db['categories'][match].items():
        if key != 'words':
            category[key] = value
        else:
            category[key] = ", ".join(
                [x[1] for x in db['categories'][match]['words']])
    return category


def _get_final_message(mistakes_remaining):
    if mistakes_remaining == 4:
        message = "Ho! Ho! Ho!"
    elif mistakes_remaining == 3:
        message = "You got your wings!"
    elif mistakes_remaining == 2:
        message = "Good job Cindy Lou Who!"
    elif mistakes_remaining == 1:
        message = "Fra-jee-lay"
    else:
        message = None
    return message


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
