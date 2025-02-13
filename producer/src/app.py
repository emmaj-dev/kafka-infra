from flask import Flask, request
from event_publisher import Publisher
import logging
import json

app = Flask(__name__)
dispatcher = Publisher()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


@app.route("/")
def index():
    return "This is the Event generator.  To send an event to the stats " + \
           "processor POST to the /events endpoint."


@app.route("/events", methods=['POST'])
def post_event():
    message = request.get_json()
    logger.debug("request had the following data: {0}".format(message))
    dispatcher.push(message)
    return json.dumps({'status': 'success'}), 200

@app.route("/batch", methods=['POST'])
def post_batch_event():
    try:
        messages = request.get_json()
        if not messages:
            raise ValueError("No message content provided.")
        dispatcher.batch_publish(messages)
        return json.dumps({'status': 'success'}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return json.dumps({'status': 'error', 'message': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)