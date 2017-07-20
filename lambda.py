import json
import boto3
import time
import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    print("event")
    print(event)
    user = get_user(event)
    print (user)
    intent = event['result']['metadata']['intentName']
    
    if intent == "add event":
        name = event['result']['parameters']['given-name']
        env = event['result']['parameters']['event']
        save_event(user, name, env)
        return build_response("saved event")
    elif intent == "ask":
        name = event['result']['parameters']['given-name']
        env = event['result']['parameters']['event']
        return get_event(user, name, env)
    return build_response("hi?")

def save_event(user, name, event):

    data = {}
    
    data["kid"] = {"S": user+"-"+name+"-"+event}
    data["event"] = {"S": event}
    data["name"] = {"S":name}
    data["dateTime"] = {"S":str(datetime.datetime.now())}
    data["datetime"] = {'S':"1212-12-12T12:12:12"}
    data["user"] = {"S":user}
    dynamodb.put_item(TableName='remembrall', Item=data);
    

def get_event(user, name, event):
    result = dynamodb.get_item(
        TableName='remembrall', 
        Key = {'kid':{"S": str(user)+"-"+name+"-"+event},'datetime':{'S':"1212-12-12T12:12:12"}
            
    })
    if 'Item' not in result:
        return build_response("i dont recall that, sorry!")
    dt = datetime.datetime.strptime(result['Item']['dateTime']['S'], "%Y-%m-%d %H:%M:%S.%f")
    return build_response(name +" was "+ event +" at "+ str(dt.hour)+":"+str(dt.minute))


def on_launch(event):
    return build_response("Hello, Application Services!")
    
def build_response(response):
    return {
        'speech': response
    }
    
def get_user(event):
    source = event['originalRequest']['source']
    if source == 'agent':
        return 3
    elif source == 'google':
        return event['originalRequest']['data']['user']['userId']
    elif source == 'slack_testbot':
        return event['originalRequest']['data']['user']
    else:
        return 0
    
    
    
