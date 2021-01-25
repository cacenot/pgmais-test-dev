import unittest

from parser import parse_raw_text, remove_invalidate_phone_numbers, remove_messages_by_state, remove_wrongly_scheduled,\
    remove_duplicated_destination, remove_messages_by_size, remove_blacklisted_phone_numbers
from ddd import States


class TestParser(unittest.TestCase):
    def test_parse_raw_text(self):
        """
        Test that it can parse messages
        """
        data = b'bff58d7b-8b4a-456a-b852-5a3e000c0e63;10;976978899;NEXTEL;21:24:03;sapien sapien non mi integer ac ' \
               b'neque\nbff58d7b-8b4a-456a-b852-5a3e000c0e63;12;996958849;NEXTEL;21:24:03;sapien sapien non mi ' \
               b'integer ac neque'
        result = parse_raw_text(data)
        expected_result = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '10', '976978899', 'NEXTEL', '21:24:03',
             'sapien sapien non mi integer ac neque'),
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '12', '996958849', 'NEXTEL', '21:24:03',
             'sapien sapien non mi integer ac neque'),
        ]
        self.assertEqual(result, expected_result)

    def test_remove_invalidate_phone_numbers(self):
        """
        Test to remove invalidated phone numbers
        """
        data = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '10', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('e7b87f43-9aa8-414b-9cec-f28e653ac25e', '12', '996958849', 'OI', '21:24:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        result = remove_invalidate_phone_numbers(data)
        expected_result = [
            ('e7b87f43-9aa8-414b-9cec-f28e653ac25e', '12', '996958849', 'OI', '21:24:03',
             'sapien sapien non mi integer ac neque'),
        ]
        self.assertEqual(result, expected_result)

    def test_remove_messages_by_state(self):
        """
        Test to remove messages based on destinies by state
        """
        data = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('e7b87f43-9aa8-414b-9cec-f28e653ac25e', '12', '996958849', 'OI', '21:24:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        result = remove_messages_by_state(data, States.SaoPaulo)
        expected_result = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        self.assertEqual(result, expected_result)

    def test_remove_wrongly_scheduled(self):
        """
        Test to remove messages that was scheduled late by argument time_limit
        """
        data = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('e7b87f43-9aa8-414b-9cec-f28e653ac25e', '12', '996958849', 'OI', '21:24:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        result = remove_wrongly_scheduled(data)
        expected_result = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        self.assertEqual(result, expected_result)

    def test_remove_messages_by_size(self):
        """
        Test to remove messages that the message text length is more than 140 characters
        """
        data = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('e7b87f43-9aa8-414b-9cec-f28e653ac25e', '12', '996958849', 'OI', '21:24:03',
             'sapien sapien non mi integer ac neque sapien non mi integer ac neque sapien non mi integer ac neque '
             'sapien non mi integer ac neque sapien non mi integer ac neque sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        result = remove_messages_by_size(data)
        expected_result = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        self.assertEqual(result, expected_result)

    def test_remove_duplicated_destination(self):
        """
        Test that have more than one message for the same destination, only the message with the lowest time should
        be considered
        """
        data = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('e7b87f43-9aa8-414b-9cec-f28e653ac25e', '12', '996958849', 'OI', '15:24:03',
             'sapien sapien non mi integer ac neque'),
            ('b7e2af69-ce52-4812-adf1-395c8875ad30', '12', '996958849', 'OI', '12:24:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        result = remove_duplicated_destination(data)
        expected_result = [
            ('b7e2af69-ce52-4812-adf1-395c8875ad30', '12', '996958849', 'OI', '12:24:03',
             'sapien sapien non mi integer ac neque'),
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        self.assertEqual(result, expected_result)

    def test_remove_blacklisted_phone_numbers(self):
        """
        Test to remove messages that is in blacklist
        """
        data = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('e7b87f43-9aa8-414b-9cec-f28e653ac25e', '46', '950816645', 'OI', '21:24:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        result = remove_blacklisted_phone_numbers(data)
        expected_result = [
            ('bff58d7b-8b4a-456a-b852-5a3e000c0e63', '22', '976978899', 'NEXTEL', '11:05:03',
             'sapien sapien non mi integer ac neque'),
            ('d81b2696-8b62-4b8b-af82-586ce0875ebc', '47', '956958849', 'VIVO', '15:00:00',
             'sapien sapien non mi integer ac neque'),
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
