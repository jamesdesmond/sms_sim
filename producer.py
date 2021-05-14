import random
import string

from faker import Faker

fake = Faker('en-US')


def generate_message(max_chars=100):
    # returns a string of random chars, default length of 100
    return ''.join([random.choice(string.ascii_letters) for i in range(max_chars - random.randint(0, max_chars - 1))])


class Message:
    def __init__(self):
        # The split on 'x' accounts for extensions that can be added by the faker lib
        self.phone_number = fake.phone_number().split('x')[0]
        self.message = generate_message()

    def __str__(self):
        return f'{self.phone_number} : {self.message}'


def get_messages(num_messages=1000):
    # returns a list of Message objects containing a phone number, and a message. default length of 1000
    return [(Message()) for i in range(num_messages)]


class Producer:
    def __init__(self, num_messages=1000):
        self.messages = get_messages(num_messages=num_messages)
