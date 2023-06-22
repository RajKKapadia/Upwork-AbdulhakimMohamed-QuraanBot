from datetime import datetime

from flask import Flask, request, jsonify

from quran_chatgpt.helper.conversation import create_conversation
from quran_chatgpt.helper.twilio_api import send_message
from quran_chatgpt.helper.database_api import get_user, update_messages, create_user
from quran_chatgpt.helper.utils import get_context
from quran_chatgpt.logger import logging

logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200


@app.route('/twilio', methods=['POST'])
def twilio():
    try:
        logger.info('A new twilio request...')
        data = request.form.to_dict()
        user_name = data['ProfileName']
        query = data['Body']
        sender_id = data['From']
        
        # TODO
        # get the user
        user = get_user(sender_id)

        # create chat_history from the previous conversations
        if user:
            context = get_context(user['messages'][-2:])
        else:
            context = ''
            
        response = create_conversation(query, context)

        logger.info(f'Sender -> {sender_id}')
        logger.info(f'Query -> {query}')
        logger.info(f'Response -> {response}')

        if user:
            update_messages(sender_id, query,
                            response, user['messageCount'])
        else:
            # if not create
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
                'channel': 'WhatsApp',
                'is_paid': False,
                'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }

            create_user(user)

        send_message(sender_id, response)
        logger.info('Request success.')
    except:
        logger.info('Request failed.')
        pass

    return 'OK', 200


@app.route('/api/qa', methods=['POST'])
def api_qa():
    try:
        body = request.get_json()
        query = body['query']
        messages = body['messages']
        context = get_context(messages)
        response = create_conversation(query, context)
        return jsonify(
            {
                'status': 1,
                'response': response['result']
            }
        )
    except:
        return jsonify(
            {
                'status': 0,
                'response': 'We are facing technical issue at this point.'
            }
        )
