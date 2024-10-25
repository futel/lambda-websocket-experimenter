# def get_instance(env):
#     # We could use the host header in the request instead?
#     return env['stage']

def log(msg):
    print(msg)

# def log_request(request):
#     msg = 'request '
#     msg += 'query_params:{} '.format(request.query_params)
#     msg += 'uri_params:{} '.format(request.uri_params)
#     msg += 'path:{} '.format(request.path)
#     msg += 'raw_body:{}'.format(request.raw_body)
#     log(msg)

# def log_response(response):
#     msg = 'response '
#     msg += 'status_code:{} '.format(response.status_code)
#     msg += 'body:{}'.format(response.body)
#     log(msg)


def announce_connection(connection_id, env):
    #sns_client.publish(event.connection_id, env)
    #env['table'].put_item(
    #    Item={"operation": "connect", "connection_id": event.connection_id})
    env['table'].put_item(
        #TableName="lambda_websocket_experimenter",
        #Item={
        #    "operation": "connect",
        #    "connection_id": event.connection_id})
        Item={"operation": "connect", "connection_id": connection_id})

def remove_connection(connection_id, env):
    env['table'].delete_item(
        Key={'connection_id': connection_id})
