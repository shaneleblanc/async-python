from flask import Flask, jsonify
from flask import session as storage
from requests_futures.sessions import FuturesSession
import os, json, time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()


def response_hook(resp, *args, **kwargs):
    print('Got response: ', resp.json())


@app.route('/count', methods=['GET',])
def count():
    start_time = time.time()
    if 'count' not in storage.keys():
        storage['count'] = 1
    else:
        storage['count'] += 1

    session = FuturesSession()
    futures = [session.get(f'https://postman-echo.com/get?x={i}', hooks={'response': response_hook,}) for i in range(storage['count'])]
    data = []
    for future in futures:
        result = future.result()
        data.append(json.loads(result.text))

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    end_time = time.time()
    print("Total time:", end_time - start_time, "seconds")
    return response, 200


if __name__ == '__main__':
    app.run()
