from datetime import datetime
import threading
import time

from flask import Blueprint, request

from quran_chatgpt.helper.twilio_api import send_message
from quran_chatgpt.helper.database_api import get_user, update_messages, create_user, update_user
from quran_chatgpt.helper.conversation import chat_completion, get_name, get_email, get_consent, get_general_response
from quran_chatgpt.helper.utils import generate_messages, create_string_chunks

from config import config

twilio = Blueprint(
    'twilio',
    __name__
)

def combined_function(user: dict, query: str, user_name: str, sender_id: str) -> None:
    try:
        messages = generate_messages(user['messages'][-2:], query, user_name)
        response = chat_completion(messages)
        chunks = create_string_chunks(response, 1500)
        update_messages(sender_id, query,
                        response, user['messageCount'])
        for chunk in chunks:
            send_message(sender_id, chunk)
            time.sleep(1)
    except:
        send_message(sender_id, config.ERROR_MESSAGE)

@twilio.route('/receiveMessage', methods=['POST'])
def receive_message():
    try:
        print('A new twilio request...')
        data = request.form.to_dict()
        user_name = data['ProfileName']
        query = data['Body']
        sender_id = data['From']

        # TODO
        # get the user
        user = get_user(sender_id)

        print(f'Sender -> {sender_id}')
        print(f'Query -> {query}')

        if user:
            if user['status'] == 'active':
                threading.Thread(target=combined_function, args=[user, query, user_name, sender_id]).start()
            else:
                properties = user['properties']
                property = ''
                for p in properties:
                    if not p['isFilled']:
                        property += p['name']
                        break

                if property == 'consent':
                    response = get_consent(query)
                    if response['status'] == -1:
                        send_message(sender_id, config.ERROR_MESSAGE)
                    elif response['status'] == 0:
                        send_message(sender_id, response['output'])
                    else:
                        properties[0]['isFilled'] = True
                        properties[0]['value'] = response['output']
                        update_user(
                            sender_id,
                            {
                                'consent': response['output'],
                                'properties': properties
                            }
                        )
                        response = get_general_response(
                            'Politely ask just the name of the user.')
                        update_messages(sender_id, query,
                                        response, user['messageCount'])
                        send_message(sender_id, response)

                elif property == 'name':
                    response = get_name(query)
                    if response['status'] == -1:
                        send_message(sender_id, config.ERROR_MESSAGE)
                    elif response['status'] == 0:
                        send_message(sender_id, response['output'])
                    else:
                        properties[1]['isFilled'] = True
                        properties[1]['value'] = response['output']
                        update_user(
                            sender_id,
                            {
                                'userName': response['output'],
                                'properties': properties
                            }
                        )
                        response = get_general_response(
                            'Politely ask just the email address of the user.')
                        update_messages(sender_id, query,
                                        response, user['messageCount'])
                        send_message(sender_id, response)

                elif property == 'email':
                    response = get_email(query)
                    if response['status'] == -1:
                        send_message(sender_id, config.ERROR_MESSAGE)
                    elif response['status'] == 0:
                        send_message(sender_id, response['output'])
                    else:
                        properties[2]['isFilled'] = True
                        properties[2]['value'] = response['output']
                        update_user(
                            sender_id,
                            {
                                'email': response['output'],
                                'properties': properties
                            }
                        )
                        response = config.FINAL_MESSAGE
                        update_messages(sender_id, query,
                                        response, user['messageCount'])
                        send_message(sender_id, response)

                else:
                    update_user(
                        sender_id,
                        {
                            'status': 'active'
                        }
                    )
                    threading.Thread(target=combined_function, args=[user, query, user_name, sender_id]).start()
        else:
            response = config.CONSENT_MESSAGE
            message = {
                'query': query,
                'response': response,
                'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }
            user = {
                'userName': user_name,
                'senderId': sender_id,
                'messages': [message],
                'messageCount': 1,
                'mobile': sender_id.split(':')[-1],
                'email': '',
                'consent': '',
                'channel': 'WhatsApp',
                'is_paid': False,
                'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M'),
                'status': 'inactive',
                'properties': [
                    {
                        'name': 'consent',
                        'isFilled': False,
                        'value': ''
                    },
                    {
                        'name': 'name',
                        'isFilled': False,
                        'value': ''
                    },
                    {
                        'name': 'email',
                        'isFilled': False,
                        'value': ''
                    }
                ]
            }
            create_user(user)
            send_message(sender_id, response)
        print('Request success.')
    except:
        print('Request failed.')
        pass

    return 'OK', 200
