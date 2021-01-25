from flask import Flask, request

from parser import parse_raw_text, remove_invalidate_phone_numbers, remove_messages_by_state, remove_wrongly_scheduled,\
    remove_duplicated_destination, remove_messages_by_size, remove_blacklisted_phone_numbers, broker_id
from ddd import States

app = Flask(__name__)


@app.route('/', methods=['POST'])
def parse_messages():
    messages = parse_raw_text(request.data)
    messages = remove_invalidate_phone_numbers(messages)
    messages = remove_messages_by_state(messages, States.SaoPaulo)
    messages = remove_wrongly_scheduled(messages)
    messages = remove_messages_by_size(messages)
    messages = remove_duplicated_destination(messages)
    messages = remove_blacklisted_phone_numbers(messages)
    broker_id_message_list = ['{};{}'.format(message[0], broker_id[message[3]]) for message in messages]
    response = '\n'.join(m for m in broker_id_message_list)
    return response, 200
