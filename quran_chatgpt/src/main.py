from datetime import datetime

from flask import Flask, request, jsonify

from quran_chatgpt.helper.conversation import create_conversation
from quran_chatgpt.helper.twilio_api import send_message
from quran_chatgpt.helper.database_api import get_user, update_messages, create_user
from quran_chatgpt.helper.utils import get_context

qa = create_conversation()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200


@app.route('/twilio', methods=['POST'])
def twilio():
    try:
        data = request.form.to_dict()
        user_name = data['ProfileName']
        query = data['Body']
        sender_id = data['From']
        # TODO
        # get the user
        user = get_user(sender_id)

        # create chat_history from the previous conversations
        context = get_context([])
        response = qa(
            {
                'context': context,
                'query': query
            }
        )

        if user:
            update_messages(sender_id, query, response['result'], user['messageCount'])
        else:
            # if not create
            message = {
                'query': query,
                'response': response['result'],
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

        send_message(sender_id, response['result'])
    except:
        pass

    return 'OK', 200


@app.route('/api/qa', methods=['POST'])
def api_qa():
    try:
        body = request.get_json()
        query = body['query']
        messages = body['messages']
        context = get_context(messages)
        response = qa(
            {
                'context': context,
                'query': query
            }
        )
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
