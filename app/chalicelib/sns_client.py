"""
Publish messages to sns.
"""

#import json

# def _publish(message, arn, env):
#     return env['sns_client'].publish(
#         TargetArn=arn,
#         Message=json.dumps({'default': json.dumps(message)}),
#         MessageStructure='json')

# def publish(message, env):
#     return env['sns_client'].publish(
#         TargetArn=env['SNS_ARN'],
#         Message=message)
