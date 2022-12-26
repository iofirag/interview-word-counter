from dotenv import load_dotenv
load_dotenv() # take environment variables from .env.
import asyncio
import platform
from flask import Flask, Response
from bp_word_counter import bp_app


# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/health')
def health():
    return Response('OK', status=200)

# start the server with the 'run()' method
if __name__ == '__main__':
    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.register_blueprint(bp_app, url_prefix="/api/v1")
    app.run(host='0.0.0.0', port=5000, debug=True)
    