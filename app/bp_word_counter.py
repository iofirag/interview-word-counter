import os
from flask import Blueprint, request, Response
from datetime import datetime, timedelta
from services.redis_driver import RedisDriver


# init variables
redis_driver = RedisDriver(host=os.getenv('REDIS_HOST'))
WORD_LIST: list[str] = os.getenv('WORD_LIST').split(',')
# create Blueprint object for add a prefix to all Flask routes
bp_app = Blueprint('words_counter', __name__)


# rest api
@bp_app.route('/events', methods=['POST'])
async def events() -> Response:
    ts: float = datetime.now().timestamp()
    body_word_lst: list[str] = request.get_data().decode('utf-8').split()
    for word in body_word_lst:
        word = word.lower()
        if word in WORD_LIST:
            await redis_driver.save_word_ts(word, ts)
    return Response(status=204)


@bp_app.route('/stats', methods=['GET'])
async def stats() -> dict[str, int]:
    interval_seconds = int(request.args.get('interval'))
    old_ts = (datetime.now() - timedelta(seconds=interval_seconds)).timestamp()
    # init word as zeros
    output = {word: 0 for word in WORD_LIST}
    # set real data
    for word in WORD_LIST:
        ts_lst: list[float] = await redis_driver.get_word_ts_list(word)
        for ts in ts_lst:
            tsDecoded: float = float(ts.decode('utf-8'))
            if tsDecoded >= old_ts:
                output[word] += 1
            else:
                break
    return output
    