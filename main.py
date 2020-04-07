from flask import Flask, request
import logging
import json
import random
import requests
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    if req['session']['new']:
        res['response']['text'] = 'Привет! Напиши: Переведите(переведи) слово: {слово}, и я его тут же переведу.'
        return
    else:
        if 'переведи' in req["request"]["original_utterance"].lower() or 'переведите' in req["request"]["original_utterance"].lower():
            key = 'trnsl.1.1.20200328T113348Z.1e31218feeb49d12.62b5b05ee18f7ce91d5b00489d99c308787e889e'
            t = req["request"]["nlu"]["tokens"][-1]
            text = f'https://translate.yandex.net/api/v1.5/tr.json/translate?key={key}&text={t}&lang=en'
            try:
                res["response"]["text"] = requests.get(text).json()["text"][0]
            except Exception as e:
                res["response"]["text"] = e
        else:
            res["response"]["text"] = "Немного не поняла Вас, проверьте корректность запроса."


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)