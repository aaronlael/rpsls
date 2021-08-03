from flask import Flask, render_template, request, session
from model import model as db
import random
import config as cfg

outcomes = { 'rock' : { 'win' : ['scissors', 'lizard'],
                      'lose' : ['spock', 'paper'] },
             'paper' : { 'win' : ['rock', 'spock'],
                      'lose' : ['lizard', 'scissors'] },
             'scissors' : { 'win' : ['paper', 'lizard'],
                      'lose' : ['spock', 'rock'] },
             'lizard' : { 'win' : ['paper', 'spock'],
                      'lose' : ['scissors', 'rock'] },
             'spock' : { 'win' : ['rock', 'scissors'],
                      'lose' : ['paper', 'lizard'] }
             }


app = Flask(__name__)

app.secret_key = cfg.secret_key

def rpsls(shoot):
    """rock, paper, scissors, lizard, spock"""
    opt = ['rock', 'paper', 'scissors', 'lizard', 'spock']
    opponent = random.choice(opt)
    if shoot not in opt:
        return f"{shoot} is not a valid choice"
    else:
        if opponent == shoot:
            db.writestats(shoot, opponent, "d")
            return f"you both chose {shoot}, draw!"
        elif opponent in outcomes[shoot]['win']:
            db.writestats(shoot, opponent, "w")
            return f"{shoot} beats {opponent}, you win!"
        else:
            db.writestats(shoot, opponent, "l")
            return f"{opponent} beats {shoot}, you lose..."



@app.route('/')
def my_form():
    return render_template("template.html")

@app.route('/', methods=['POST'])
def postop():
    if 'hist' not in session:
        session['hist'] = []
    res = rpsls(request.form['text'].lower())
    if len(session['hist']) > 11:
        del session['hist'][-1]
    session['hist'] = [res] + session['hist']
    return render_template("template.html", res=res, hist=session['hist'][1:], output=db.process_stats(db.rpsls_stats()))


@app.route('/session')
def sessioninfo():
    session['hist'] = []
    return render_template("template.html")
