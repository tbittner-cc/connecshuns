import random

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    words = [
        'Hello', 'World', 'Foo', 'Bar', 'A', 'A', 'A', 'A', 'Pimple', 'Blood',
        'Mars', 'Code', 'Die Hard', 'Gremlins', 'Love Actually', 'Elf'
    ]
    #words = ['Mars', 'Code', 'Pimple', 'Blood']
    categories = [
        'Words Used in Programming', 'Letters Starting with A',
        'Non-Christmas Red Things', 'Christmas Movies'
    ]

    # random.shuffle(words)
    return render_template('index.html', words=words)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
