from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

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
    
    table.put_item(
            Item={
                'userId': "aaaaaa",
                'username': "name",
                'lastname': "last"
            }
            )
    
    return "aaaa"

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
