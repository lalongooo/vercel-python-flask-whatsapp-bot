import os

GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL = os.getenv("GRAPH_FACEBOOK_WHATSAPP_MESSAGES_URL")
FIREBASE_SERVER_KEY = os.environ.get('FIREBASE_SERVER_KEY')
WHATSAPP_API_TEMP_ACCESS_TOKEN = os.environ.get('WHATSAPP_API_TEMP_ACCESS_TOKEN')
HEADERS = {
    'Authorization': f'Bearer {WHATSAPP_API_TEMP_ACCESS_TOKEN}',
    "Content-Type": "application/json",
}
TEXT_MESSAGE_TEMPLATE = {
    "messaging_product": "whatsapp",
    "to": "",
    "text": {
        "body": ""
    }
}

INTERACTIVE_BOILERPLATE_INITIAL = {
        "messaging_product": "whatsapp",
        "to": "",
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
    }