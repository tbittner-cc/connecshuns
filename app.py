import random

from flask import Flask, redirect, render_template, request, session
from replit import db

app = Flask(__name__)

db['categories'] = [{'level':1,
                     'category':'Christmas Movies',
                     'words':['Die Hard','Elf','Gremlins','Love Actually']},
                    {'level':2,
                     'category':'Letters Starting with A',
                     'words':['A','A','A','A']},
                    {'level':3,
                    'category':'Words Used in Programming',
                     'words':['Hello','Foo','World','Bar']},    
                    {'level':4,
                     'category':'Non-Christmans Red Things', 
                     'words':['Pimple','Blood','Mars','Code']}]

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


@app.route('/')
def index():

    source_words = [word for category in db['categories'] for word in     
                    category['words']]

    words = [('word' + str(idx), word)
             for idx, word in enumerate(source_words)]

    mistakes_remaining = 4

    #random.shuffle(words)
    return render_template('index.html',
                           words=words,
                           mistakes_remaining=mistakes_remaining)


@app.route('/check-tiles', methods=['GET', 'POST'])
def check_tiles():
    print(request.form)
    print(db['words'])
    return 'foo'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
