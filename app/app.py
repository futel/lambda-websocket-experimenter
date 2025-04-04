"""
Chalice top level module. Read on application init. Websocket endpoints are
defined by the on_ws_* decorators.

For a websocket interaction, this exists to start the application,
to get the event, run a single endpoint function, and return the result.
There may be other actions enabled by chalice, like scheduled tasks.
"""

from boto3.session import Session
import chalice
import json

from chalicelib import env_util
#from chalicelib import sns_client
from chalicelib import util

env = env_util.get_env()

app = chalice.Chalice(app_name='experimenter')
app.websocket_api.session = Session()
app.experimental_feature_flags.update([
    'WEBSOCKETS'
])

# {'Items': [{'connection_id': 'AIyPpcY0vHcCJgQ=', 'operation': 'connect'}, {'connection_id': 'AIzKXfJQPHcCGDA=', 'operation': 'connect'}, {'connection_id': 'bar', 'operation': 'connect'}, {'connection_id': 'foo', 'operation': 'connect'}], 'Count': 4, 'ScannedCount': 4, 'ResponseMetadata': {'RequestId': 'HV490E4VHA6UIMN7RI76BTDF37VV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Oct 2024 04:24:02 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '296', 'connection': 'keep-alive', 'x-amzn-requestid': 'HV490E4VHA6UIMN7RI76BTDF37VV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3712998993'}, 'RetryAttempts': 0}}
def _connections():
    """ Return a sequence of connection IDs from the table."""
    # Every item in the table has the connection_id for a connected client.
    items = env['table'].scan()
    items = items['Items']
    items = [i['connection_id'] for i in items]
    return items

def _broadcast(connection_id, payload):
    """Play paylod to all connections except the one with connection_id."""
    connection_ids = _connections()
    connection_ids = (cid for cid in connection_ids if cid != connection_id)
    for cid in connection_ids:
        util.log("broadcast attempting {}".format(cid))
        try:
            app.websocket_api.send(
                connection_id=cid,
                message=payload)
        except chalice.WebsocketDisconnectedError:
            util.log("broadcast removing disconnected {}".format(cid))
            util.remove_connection(cid, env)
        except chalice.BadRequestError:
            util.log("broadcast removing bad {}".format(cid))
            util.remove_connection(cid, env)
        except Exception as e:
            util.log("broadcast unknown exception {}".format(e))

def _event_payload(event):
    try:
        return event.json_body['media']['payload']
    except Exception as e:
        util.log("no event payload")
        return None

@app.on_ws_connect()
def connect(event):
    """Handle connect event."""
    util.log("connect {}".format(event.connection_id))
    # util.log(event.to_dict())
    util.announce_connection(event.connection_id, env)
    # connection_ids = _connections()
    # for connection_id in connection_ids:
    #     util.log("existing")
    #     util.log(connection_id)

@app.on_ws_disconnect()
def disconnect(event):
    """Handle disconnect event."""
    util.log("disconnect {}".format(event.connection_id))
    # Don't do anything, we deal with this lazily.
    # connection_ids = _connections()
    # for connection_id in connection_ids:
    #     util.log("existing")
    #     util.log(connection_id)
    #util.log(event.to_dict())

# def _body(stream_sid, payload):
#     return json.dumps(
#         {"event": "media",
#          "streamSid": self.stream_sid,
#          "media": {"payload": payload}}))

@app.on_ws_message()
def message(event):
    """ Handle incoming message event."""
    util.log("message {}".format(event.connection_id))
    util.log(event.to_dict())

    # XXX Testing, play to other clients.
    payload = _event_payload(event)
    if payload:
        util.log("media payload")
        #payload = _body(event.stream_sid, payload)
        _broadcast(event.connection_id, payload)

# @app.on_sns_message(topic='lambda_websocket_experimenter')
# def event_handler(event):
#     util.log(
#         "message {}".format(event.message))
