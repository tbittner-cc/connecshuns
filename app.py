import random

from flask import Flask, render_template

app = Flask(__name__)

words = []
categories = []

@app.route('/')
def index():
    words = [
        'Hello', 'World', 'Foo', 'Bar', 'A', 'A', 'A', 'A', 'Pimple', 'Blood',
        'Mars', 'Code', 'Die Hard', 'Gremlins', 'Love Actually', 'Elf'
    ]

    categories = [
        'Words Used in Programming', 'Letters Starting with A',
        'Non-Christmas Red Things', 'Christmas Movies'
    ]

    mistakes_remaining = 4

    random.shuffle(words)
    return render_template('index.html',
                           words=words,
                           mistakes_remaining=mistakes_remaining)

@app.route('/check-tiles', methods=['GET','POST'])
def check_tiles():
    return 'foo'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
