from flask import request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY='AIzaSyAH59eBDXgoqaID5KsMHFx_GCmuwRMRhSY'

from flask import render_template, flash
import datetime
from random import randint

from flask_wtf import form

from app.email import send_email, send_redeem_email
from app.forms import LoginForm, RedeemForm
from app import app

from datetime import datetime as dt



@app.route("/")
@app.route('/home')
def home():
    date_str = '2024-05-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta = today - given_date
    months1 = delta.days // 30
    daysmonths1 = delta.days % 30

    date_str = '2024-09-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta2 = today - given_date
    months2 = delta2.days // 30
    daysmonths2 = delta2.days % 30

    target_date = dt(2004, 4, 7)
    days_since = (dt.now() - target_date).days
    age = (days_since // 365) - 1

    if today.month == 4:
        return render_template('birthday.html', firstday=delta.days, dateday=delta2.days, months1=months1,
                               months2=months2
                               , daysmonths1=daysmonths1, daysmonths2=daysmonths2, days_since=days_since, age=age)

    else:
        return render_template('index.html', firstday=delta.days, dateday=delta2.days, months1=months1, months2=months2
                               , daysmonths1=daysmonths1, daysmonths2=daysmonths2)


@app.route('/flirt')
def flirt():
    flirtlines = ['Girl are you my daily flintstones gummies, because i could eat you up every single day ahaha',
                  'Girl are you a subway employee, because id pay you 5 dollars to make me a foot long ahaha',
                  'Girl are you the dying dehydrated basil plant on my window sill, because all i wanna do is see you get wet']
    flirtline = flirtlines[randint(0, len(flirtlines) - 1)]
    return render_template('pickupline.html', line=flirtline)


@app.route('/date', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('success.html', choice=form.choice.data, other=form.otherrestaurant.data)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/coupons', methods=['GET', 'POST'])
def coupons():
    coupons = [
        {"title": "Breakfast in Bed", "code": "LOVE123", "valid": True},
        {"title": "5 Minute Makeout", "code": "KIS456", "valid": True},
        {"title": "1 Free Raspberry", "code": "RAS343", "valid": True},
        {"title": "Full Expense Panera Trip", "code": "PAN346", "valid": True},
        {"title": "Back Massage", "code": "BAK983", "valid": True},
        {"title": "10 No Resistance Ass Slaps", "code": "ASS069", "valid": True},
        {"title": "Piggy Back Ride to any Valid Location", "code": "PIG287", "valid": True},
        {"title": "Day Long Cornball Pass", "code": "COR477", "valid": True},
        {"title": "Movie Pick for the Night", "code": "MOV135", "valid": True}
    ]
    form = RedeemForm()
    if form.validate_on_submit():
        send_redeem_email(form)
        flash('Redeemed ' + form.name.raw_data[1] + ' Coupon!')
        return render_template('coupons.html', title="Coupons", coupons=coupons, form=form)
    return render_template('coupons.html', title="Coupons", coupons=coupons, form=form)


@app.route('/reasons')
def reasons():
    return render_template('love_reasons.html', title="LoveReasons")


@app.route('/birthday')
def birthday():
    date_str = '2024-05-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta = today - given_date
    months1 = delta.days // 30
    daysmonths1 = delta.days % 30

    date_str = '2024-09-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta2 = today - given_date
    months2 = delta2.days // 30
    daysmonths2 = delta2.days % 30

    target_date = dt(2004, 4, 7)
    days_since = (dt.now() - target_date).days
    age = (days_since // 365) - 1

    return render_template('birthday.html', firstday=delta.days, dateday=delta2.days, months1=months1, months2=months2
                           , daysmonths1=daysmonths1, daysmonths2=daysmonths2, days_since=days_since, age=age)


import random
from flask import session

# Add this to your imports at the top
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

from flask import session


# Add these routes to your existing Flask app

@app.route('/pokemon-game', methods=['GET', 'POST'])
def pokemon_game():
    # Initialize or reset game state
    if 'game_state' not in session or request.method == 'POST':
        session['game_state'] = {
            'score': 0,
            'current_pokemon': None,
            'options': [],
            'correct_guesses': 0,
            'total_guesses': 0,
            'cute_list': session.get('game_state', {}).get('cute_list', [])
        }
        session.modified = True

    game_state = session['game_state']

    # Get a random Pokémon if none is set
    if not game_state['current_pokemon']:
        random_pokemon_id = random.randint(1, 1000)  # Gen 1 only for simplicity
        pokemon_data = get_pokemon_data(random_pokemon_id)

        if pokemon_data:
            game_state['current_pokemon'] = pokemon_data
            # Generate 3 wrong options and 1 correct option
            options = generate_options(pokemon_data['name'])
            game_state['options'] = options
            session.modified = True

    return render_template('pokemon_game.html', game_state=game_state)


@app.route('/pokemon-guess/<guess>')
def pokemon_guess(guess):
    game_state = session.get('game_state', {})
    correct = False

    if game_state and game_state['current_pokemon']:
        correct_pokemon = game_state['current_pokemon']['name']
        correct = guess.lower() == correct_pokemon.lower()

        game_state['total_guesses'] += 1
        if correct:
            game_state['correct_guesses'] += 1
            game_state['score'] += 10

        # Reset current Pokémon for next round
        game_state['current_pokemon'] = None
        session.modified = True

    return jsonify({
        'correct': correct,
        'correct_pokemon': correct_pokemon if game_state else None,
        'score': game_state.get('score', 0),
        'accuracy': calculate_accuracy(game_state) if game_state else 0
    })


@app.route('/add-cute/<pokemon_name>')
def add_cute(pokemon_name):
    game_state = session.get('game_state', {})
    if game_state:
        if 'cute_list' not in game_state:
            game_state['cute_list'] = []

        # Get full pokemon data to save
        pokemon_data = None
        if game_state['current_pokemon'] and game_state['current_pokemon']['name'] == pokemon_name:
            pokemon_data = game_state['current_pokemon']
        else:
            # If not current pokemon, fetch fresh data
            response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{pokemon_name.lower()}")
            if response.status_code == 200:
                data = response.json()
                pokemon_data = {
                    'id': data['id'],
                    'name': data['name'],
                    'sprite': data['sprites']['front_default']
                }

        if pokemon_data and pokemon_data not in game_state['cute_list']:
            game_state['cute_list'].append(pokemon_data)
            session.modified = True
            return jsonify({'success': True, 'message': f'{pokemon_name.title()} added to cute list!'})

    return jsonify({'success': False, 'message': 'Failed to add to cute list'})


@app.route('/view-cute-list')
def view_cute_list():
    game_state = session.get('game_state', {})
    cute_list = game_state.get('cute_list', [])
    return render_template('cute_list.html', cute_list=cute_list)


# Keep all the existing helper functions (get_pokemon_data, generate_options, calculate_accuracy)


def get_pokemon_data(pokemon_id):
    try:
        response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}")
        if response.status_code == 200:
            data = response.json()
            return {
                'id': data['id'],
                'name': data['name'],
                'sprite': data['sprites']['front_default'],
                'silhouette': data['sprites']['front_default']  # We'll process this to silhouette in JS
            }
    except Exception as e:
        print(f"Error fetching Pokémon data: {e}")
    return None


def generate_options(correct_name):
    # Get 3 random Pokémon names as wrong options
    options = [correct_name]
    while len(options) < 4:
        random_id = random.randint(1, 1000)
        pokemon = get_pokemon_data(random_id)
        if pokemon and pokemon['name'] not in options:
            options.append(pokemon['name'])
    random.shuffle(options)
    return options


def calculate_accuracy(game_state):
    if game_state['total_guesses'] == 0:
        return 0
    return (game_state['correct_guesses'] / game_state['total_guesses']) * 100



if __name__ == "__main__":
    app.run()