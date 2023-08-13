from flask import Flask
from flask import request
from flask import Response
from flask import make_response
import requests
import uuid
import os
import json
from utils.util import Util
from utils.constants import (
    GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL,
    HEADERS,
    WHATSAPP_API_TEMP_ACCESS_TOKEN,
)

app = Flask(__name__)

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    if request.args.get("hub.challenge"):
        return request.args.get("hub.challenge")
    else:
        json_data = json.loads(request.data)
        print("Message Data Received:")

        data_decoded = request.data.decode('utf-8')
        print("request.data.decode('utf-8')")
        print(type(data_decoded))
        print(data_decoded)

        if Util.is_message(request):
            if Util.is_interactive_list_reply(request):
                print("it is interactive reply")
                return handle_interactive_list_reply(request)
            else:
                print("it is NOT interactive reply")
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
    url = GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL
    to_author = Util.get_author(request)
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": to_author,
        "type": "interactive",
        "recipient_type": "individual",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "¡Hola! Muchas gracias por ponerte en contacto con nosotros."
            },
            "body": {
                "text": "Estamos encantados de ayudarte."
            },
            "action": {
                "button": "Elige una opción",
                "sections":
                [
                    {
                        "rows":
                        [
                            {
                                "id": "1",
                                "title": "Contratar servicio",
                                "description": "Conoce los detalles para contratar internet en tu domicilio"
                            },
                            {
                                "id": "2",
                                "title": "Reportar una falla",
                                "description": "Lamentamos que esto haya sucedido. Selecciona para levantar un reporte"
                            },
                            {
                                "id": "3",
                                "title": "Precios de paquetes",
                                "description": "Información relacionada a precios de paquetes de internet en tu casa"
                            }
                        ]
                    }
                ]
            }
        }
    })

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    response_json = response.json()
    print(response_json)

    response = make_response(response_json)
    response.status_code = 200
    return response

def reply(request, reply_message):
    url = GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL
    to_author = Util.get_author(request)
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": to_author,
        "text": {
            "body": reply_message
        }
    })

    response = requests.request("POST", url, headers=HEADERS, data=payload)
    response_json = response.json()
    print(response_json)
    response = make_response(response_json)
    response.status_code = 200
    return response