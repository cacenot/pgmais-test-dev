from typing import List, Tuple
from datetime import datetime
import requests
import threading
import concurrent.futures

from ddd import DDDs, States, DDDs_by_state

thread_local = threading.local()

broker_id = {
    'VIVO': 1,
    'TIM': 1,
    'CLARO': 2,
    'OI': 2,
    'NEXTEL': 3,
}


def parse_raw_text(raw_text: bytes) -> List[Tuple]:
    lines = raw_text.decode('utf-8').splitlines()
    messages = [tuple(message.split(';')) for message in lines if len(message.split(';')) == 6]
    return messages


def remove_invalidate_phone_numbers(messages: List[Tuple]):
    def _validate_phone(message: Tuple[str]) -> bool:
        try:
            ddd = message[1]
            phone_number = message[2]
            if len(ddd) != 2:
                return False
            elif len(phone_number) != 9:
                return False
            elif int(phone_number[0]) != 9:
                return False
            elif int(phone_number[1]) < 6:
                return False
            elif ddd not in DDDs:
                return False
            else:
                return True
        except:
            return False
    return [message for message in messages if _validate_phone(message)]


def remove_messages_by_state(messages: List[Tuple], state: States) -> List[Tuple]:
    state_ddds = DDDs_by_state[state]
    return [message for message in messages if message[1] not in state_ddds]


def remove_wrongly_scheduled(messages: List[Tuple], time_limit: str = '19:59:59') -> List[Tuple]:
    _time_limit = datetime.strptime(time_limit, '%H:%M:%S').time()
    _messages = []
    for message in messages:
        try:
            message_time = datetime.strptime(message[4], '%H:%M:%S').time()
            if message_time <= _time_limit:
                _messages.append(message)
        except:
            pass
    return _messages


def remove_messages_by_size(messages: List[Tuple], text_max_size: int = 140) -> List[Tuple]:
    return [message for message in messages if len(message[5]) <= text_max_size]


def remove_duplicated_destination(messages: List[Tuple]) -> List[Tuple]:
    # Isolate all duplicate destination based on phone numbers
    destinations = [[message[2]] for message in messages]
    duplicate_destinations = [item for sublist in [x for n, x in enumerate(destinations) if x in destinations[:n]]
                              for item in sublist]

    # Get the earlier message from duplicated destinies
    def _get_earlier_message(_messages: List[Tuple]) -> Tuple:
        earlier_time = None
        earlier_message = None
        for message in _messages:
            message_time = datetime.strptime(message[4], '%H:%M:%S').time()
            if earlier_time is None or message_time < earlier_time:
                earlier_time = message_time
                earlier_message = message
        return earlier_message

    earlier_messages = []
    for destination in duplicate_destinations:
        _messages = [message for message in messages if message[2] == destination]
        earlier_messages.append(_get_earlier_message(_messages))

    # Isolate non duplicate messages by destination
    messages_without_duplicated = [message for message in messages if message[2] not in duplicate_destinations]

    # Return merged earlier messages with non duplicate messages
    return earlier_messages + messages_without_duplicated


def _get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def remove_blacklisted_phone_numbers(messages: List[Tuple]):
    def _check_blacklist(phone_number: str) -> requests.Response:
        session = _get_session()
        response = session.get('{}{}'.format('https://front-test-pg.herokuapp.com/blacklist/', phone_number))
        return response

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = []
        for message in messages:
            _phone_number = '{}{}'.format(message[1], message[2])
            future = executor.submit(_check_blacklist, phone_number=_phone_number)
            results.append([message, future])
    return [result[0] for result in results if result[1].result().status_code != 200]
