import os
import json
from dotenv import load_dotenv
from flask import Flask, Blueprint, request, Response
from datetime import datetime, timedelta
import redis

# init redis connection
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

# take environment variables from .env.
load_dotenv()

# init variables
WORD_LIST = json.loads(os.environ['WORD_LIST'])
counter = {}

# create Blueprint object for add a prefix to all Flask routes
bp = Blueprint('words_counter_rest_api', __name__)
# create the application object
app = Flask(__name__)
# use decorators to link the function to a url
@bp.route('/events', methods=['POST'])
def events():
    ts = datetime.now().timestamp()
    body_word_lst = request.get_data().decode('utf-8').split()
    for word in body_word_lst:
        word = word.lower()
        if word in WORD_LIST:
            redis.lpush(word, ts) # insert at the head
    return Response(status=204)


@bp.route('/stats', methods=['GET'])
def stats():
    interval_seconds = int(request.args.get('interval'))
    old_ts = (datetime.now() - timedelta(seconds=interval_seconds)).timestamp()
    print(old_ts)
    # init word as zeros
    output = {word: 0 for word in WORD_LIST}
    # set real data
    for word in WORD_LIST:
        ts_lst = redis.lrange(word, 0, -1)
        for ts in ts_lst:
            tsDecoded = float(ts.decode('utf-8'))
            if tsDecoded >= old_ts:
                output[word] += 1
            else:
                break
    return output


# start the server with the 'run()' method
if __name__ == '__main__':
    app.register_blueprint(bp, url_prefix="/api/v1")
    app.run(port=3000, debug=True)
