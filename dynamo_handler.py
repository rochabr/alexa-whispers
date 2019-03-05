from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
#import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             if abs(o) % 1 > 0:
#                 return float(o)
#             else:
#                 return int(o)
#         return super(DecimalEncoder, self).default(o)

def write_whisper(whisper):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('whispers')
    
    ext_whisper = table.query(
        KeyConditionExpression=Key('userId').eq(whisper.userId)
    )
    
    if ext_whisper['Count'] == 0:
        whisper_list = []
        whisper_list.append({
            'userId': whisper.userId,
            'whisper': whisper.whisper,
            'password': whisper.password,
            'to':whisper.to
        })
        
        table.put_item(
            Item={
                'userId': whisper.userId,
                'whispers': whisper_list
            }
            )
    else:
        whisper_list = ext_whisper['Items'][0]['whispers']
        
        whisper_list.append({
            'userId': whisper.userId,
            'whisper': whisper.whisper,
            'password': whisper.password,
            'to':whisper.to
        })
        table.update_item(
            Key={
                'userId': whisper.userId
            },
            UpdateExpression='SET whispers = :whisper_list',
            ExpressionAttributeValues={
                ':whisper_list': whisper_list
            },
            ReturnValues="UPDATED_NEW"
        )
    return True
    
def read_whisper(userId, password):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('whispers')
    
    ext_whisper = table.query(
        KeyConditionExpression=Key('userId').eq(userId)
    )
    
    whisper_list = []
    if ext_whisper['Count'] > 0:
        for whisper in ext_whisper['Items'][0]['whispers']:
            if whisper['password'] == password:
                whisper_list.append(whisper['whisper'])
        
    print(whisper_list)
    return whisper_list

class Whisper:
    def __init__(self, userId, whisper, password, to):
        self.userId = userId
        self.whisper = whisper
        self.password = password
        self.to = to

    
# title = "The Big New Movie"
# year = 2015

# response = table.put_item(
#   Item={
#         'year': year,
#         'title': title,
#         'info': {
#             'plot':"Nothing happens at all.",
#             'rating': decimal.Decimal(0)
#         }
#     }
# )

# print("PutItem succeeded:")
# print(json.dumps(response, indent=4, cls=DecimalEncoder))
