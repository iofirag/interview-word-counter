import os
import json
from dotenv import load_dotenv
from flask import Flask, Blueprint, request, Response
from datetime import datetime, timedelta
from services.redisDriver import RedisDriver

# take environment variables from .env.
load_dotenv()

# init variables
redisDriver = RedisDriver(host=os.environ['REDIS_HOST'])
WORD_LIST = json.loads(os.environ['WORD_LIST'])
# create Blueprint object for add a prefix to all Flask routes
bp = Blueprint('words_counter_rest_api', __name__)
# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/ping')
def ping():
    return 'PONG', 200


@bp.route('/events', methods=['POST'])
def events():
    ts = datetime.now().timestamp()
    body_word_lst = request.get_data().decode('utf-8').split()
    for word in body_word_lst:
        word = word.lower()
        if word in WORD_LIST:
            redisDriver.saveWordTs(word, ts)
    return Response(status=204)


@bp.route('/stats', methods=['GET'])
def stats():
    interval_seconds = int(request.args.get('interval'))
    old_ts = (datetime.now() - timedelta(seconds=interval_seconds)).timestamp()
    # init word as zeros
    output = {word: 0 for word in WORD_LIST}
    # set real data
    for word in WORD_LIST:
        ts_lst = redisDriver.getWordTimestampList(word)
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
    app.run(host='0.0.0.0', port=5000, debug=True)
