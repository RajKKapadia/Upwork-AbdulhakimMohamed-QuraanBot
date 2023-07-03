from flask import Blueprint, request, jsonify

from quran_chatgpt.helper.conversation import create_conversation
from quran_chatgpt.helper.utils import get_context

backend = Blueprint(
    'backend',
    __name__
)


@backend.route('/api/qa', methods=['POST'])
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
