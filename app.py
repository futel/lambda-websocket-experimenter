from boto3.session import Session
import chalice
#from chalice import Chalice
#from chalice import WebsocketDisconnectedError

from chalicelib import env_util
from chalicelib import sns_client
from chalicelib import util

env = env_util.get_env()

app = chalice.Chalice(app_name='experimenter')
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

# {'Items': [{'connection_id': 'AIyPpcY0vHcCJgQ=', 'operation': 'connect'}, {'connection_id': 'AIzKXfJQPHcCGDA=', 'operation': 'connect'}, {'connection_id': 'bar', 'operation': 'connect'}, {'connection_id': 'foo', 'operation': 'connect'}], 'Count': 4, 'ScannedCount': 4, 'ResponseMetadata': {'RequestId': 'HV490E4VHA6UIMN7RI76BTDF37VV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Oct 2024 04:24:02 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '296', 'connection': 'keep-alive', 'x-amzn-requestid': 'HV490E4VHA6UIMN7RI76BTDF37VV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3712998993'}, 'RetryAttempts': 0}}
def _connections():
    # Every item with connection_id is for a connected client.
    items = env['table'].scan()
    items = items['Items']
    items = [i['connection_id'] for i in items]
    return items

def _broadcast(event):
    connection_ids = _connections()
    for connection_id in connection_ids:
        try:
            app.websocket_api.send(
                connection_id=connection_id,
                message=event.body)
        except chalice.WebsocketDisconnectedError:
            util.log("broadcast removing disconected {}".format(connection_id))
            util.remove_connection(connection_id, env)
        except chalice.BadRequestError:
            util.log("broadcast removing bad {}".format(connection_id))
            util.remove_connection(connection_id, env)
        except Exception as e:
            util.log("broadcast unknown exception {}".format(e))

@app.on_ws_connect()
def connect(event):
    util.log("connect")
    util.log(event.to_dict())
    util.announce_connection(event.connection_id, env)

@app.on_ws_disconnect()
def disconnect(event):
    util.log("disconnect")
    util.log(event.to_dict())

@app.on_ws_message()
def message(event):
    util.log("message")
    util.log(event.to_dict())
    _broadcast(event)

# @app.on_sns_message(topic='lambda_websocket_experimenter')
# def event_handler(event):
#     util.log(
#         "message {}".format(event.message))
