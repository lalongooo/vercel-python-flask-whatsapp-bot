from flask import Flask
from flask import request
from flask import Response
from flask import make_response
import requests
import json
from utils.util import Util
from utils.constants import (
    GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL,
    HEADERS,
    INTERACTIVE_BOILERPLATE_INITIAL,
    TEXT_MESSAGE_TEMPLATE,
)

app = Flask(__name__)

@app.route('/')
def home():
    return 'WhatsApp Bot Service is operating normally ✅'

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    if request.args.get("hub.challenge"):
        return request.args.get("hub.challenge")
    else:
        data_decoded = request.data.decode('utf-8')
        print("Request payload: 👇🏼")
        print(data_decoded)
        print("Request payload: 👆🏼")

        if Util.is_message(request):
            if Util.is_interactive_list_reply(request):
                return handle_interactive_list_reply(request)
            else:
                return reply_with_interactive_message(request)
        else:
            print("it is not a valid message")
            response = make_response('')
            response.status_code = 200
            return response

def handle_interactive_list_reply(request):
    reply_data = Util.get_reply_content(request)
    print(reply_data)
    if reply_data == "1":
        return reply(request, "Comenzaremos tu proceso de contratación...")
    elif reply_data == "2":
        return reply(request, "Nuestro servicio nunca falla. No mientas.")
    elif reply_data == "3":
        return reply(request, "Cobramos un chingo de dinero 🤑")
    else:
        return reply_with_interactive_message(request)

def reply_with_interactive_message(request):
    interactive_reply_content = INTERACTIVE_BOILERPLATE_INITIAL.copy()
    interactive_reply_content["to"] = Util.get_author(request)
    response = requests.post(
        url = GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL,
        headers = HEADERS,
        data = json.dumps(interactive_reply_content)
    )

    response_json = response.json()
    print(response_json)
    response = make_response(response_json)
    response.status_code = 200
    return response

def reply(request, reply_message):
    text_message = TEXT_MESSAGE_TEMPLATE.copy()
    text_message["to"] = Util.get_author(request)
    text_message["text"]["body"] = reply_message
    text_message_payload = json.dumps(text_message)
    
    print("WhatsApp Request payload: 🟢")
    print(text_message_payload)
    print("WhatsApp Request payload: 🔴")
    
    response = requests.post(
        url = GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL,
        headers = HEADERS,
        data = text_message_payload
    )
    response_json = response.json()

    print("WhatsApp Response payload: 🟢")
    print(response_json)
    print("WhatsApp Response payload: 🔴")

    return make_bot_response_200(response_json)

def make_bot_response_200(content):
    response = make_response(content)
    response.status_code = 200
    return response