from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import requests
import random

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/preguntas')
def preguntas():
    with open('preguntas.txt', 'r') as file:
        preguntas = file.readlines()[1:]
        preguntas = [pregunta.strip().split('|') for pregunta in preguntas]

    preguntas_json = []
    for pregunta in preguntas:
        pregunta_dict = {}
        try:
            pregunta_dict['pregunta'] = pregunta[0][1:-1]
            pregunta_dict['respuesta'] = pregunta[1]
        except IndexError:
            print(f"Skipping invalid question: {pregunta}")
        else:
            preguntas_json.append(pregunta_dict)

    return(jsonify(preguntas_json))

@app.route('/ahorcado', methods=['POST'])
def ahorcado():
    response = requests.get('http://localhost:5000/preguntas')
    preguntas = json.loads(response.text)

    pregunta = random.choice(preguntas)

    answer = pregunta['respuesta'].lower()
    guessed = set(request.json.get('guessed', []))
    incorrect = set(request.json.get('incorrect', []))
    max_guesses = 3

    if request.method == 'POST':
        guess = request.json.get('letra', '').lower()
        if guess in guessed or guess in incorrect:
            return jsonify({'message': 'You already guessed that letter!'})
        elif guess in answer:
            guessed.add(guess)
        else:
            incorrect.add(guess)

    state = {
        'answer': answer,
        'guessed': list(guessed),
        'incorrect': list(incorrect),
        'max_guesses': max_guesses,
        'counter_guesses': len(incorrect),
    }

    if set(answer) - guessed and len(incorrect) < max_guesses:
        state['message'] = f"Word: {' '.join([c if c in guessed else '_' for c in answer])}"
        state['message'] += f"\nIncorrect guesses [{len(incorrect)}]: {' '.join(incorrect)}"
    elif set(answer) - guessed:
        state['message'] = f"Sorry, you lose! The word was '{answer}'."
    else:
        state['message'] = "Congratulations, you win!"

    return jsonify(state)

if __name__ == '__main__':
    app.run(debug=True)