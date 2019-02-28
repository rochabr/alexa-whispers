"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
import random
from dynamo_handler import write_whisper, Whisper, read_whisper
# import dynamo_handler


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    
def build_whispered_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def build_output(whispers):
    if len(whispers) == 0:
        return "You don't have any whispers, today. Check again tomorrow!"
    elif len(whispers) == 1:
        return "<speak>You have one whisper! How exciting! Here it is! <amazon:effect name=\"whispered\">" + whispers[0] + ".</amazon:effect>.</speak>"
    else:
        count = 1
        output = "<speak>You have " + str(len(whispers)) + " whispers. Let me whisper them to you..." 
        for whisper in whispers:
            output += "<break time=\"1s\"/>Whisper number " + str(count) + "! <amazon:effect name=\"whispered\">" + whisper + ".</amazon:effect>"
            count = count + 1
        
        output += "<break time=\"1s\"/>Well, I hope you've enjoyed your whispers! Check again soon!</speak>"
        print(output)
        return output
    

# --------------- Functions that control the skill's behavior ------------------
def get_readwhispers_response(session, intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "My Whispers"
    
    userId = session['user']['userId']
    password = intent['slots']['password']['value']
    
    whispers = read_whisper(userId, password)
    
    speech_output = build_output(whispers)
    
    reprompt_text = "I'm still searhing for your whispers! Hang tight!"
    should_end_session = False
    return build_response(session_attributes, build_whispered_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_sendwhisper_response(session, intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    
    card_title = "Send Whisper To"
    speech_output = "All right, I'll send your whisper to " + intent['slots']['name']['value'] 
    reprompt_text = "Sending whisper"
    
    userID = session['user']['userId']
    
    whisper = Whisper(userID, intent['slots']['message']['value'], intent['slots']['password']['value'], intent['slots']['name']['value'])
    write_whisper(whisper)
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Whisper! I can read your whispers or send a whisper to someone. What do you want to do?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using whispers! Bye! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "test":
        return get_test_response()
    elif intent_name == "ReadWhispers":
        return get_readwhispers_response(session, intent)
    elif intent_name == "SendWhisperToName":
        return get_sendwhisper_response(session, intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.28bf33ec-531c-4378-83cd-5a2499b8a642"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
