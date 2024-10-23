from boto3.session import Session
from chalice import Chalice
from chalice import WebsocketDisconnectedError

from chalicelib import env_util
from chalicelib import sns_client
from chalicelib import util

env = env_util.get_env()

app = Chalice(app_name='experimenter')
app.websocket_api.session = Session()
app.experimental_feature_flags.update([
    'WEBSOCKETS'
])

@app.route('/index.xml')
def foo():
    # XXX instead of pause, redirect back to handle stream close
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="wss://stage.experimenter.phu73l.net/socket"></Stream>
  </Connect>
  <Pause length="40"/>
</Response>"""

@app.on_ws_connect()
def connect(event):
    util.log("connect")
    util.log(event.to_dict())
    # Announce presence.
    sns_client.publish(event.connection_id, env)

@app.on_ws_disconnect()
def disconnect(event):
    util.log("disconnect")
    util.log(event.to_dict())

@app.on_ws_message()
def message(event):
    util.log("message")
    util.log(event.to_dict())
    try:
        # Echo.
        app.websocket_api.send(
            connection_id=event.connection_id,
            message=event.body)
        # Announce presence.
        sns_client.publish(event.connection_id, env)
    except WebsocketDisconnectedError as e:
        pass

@app.on_sns_message(topic='lambda_websocket_experimenter')
def event_handler(event):
    util.log(
        "message {}".format(event.message))
