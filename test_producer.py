import pytest

import producer

max_chars = 1000


@pytest.fixture()
def prod(request):
    return producer.Producer()


def test_producer_len(prod):
    # A producer that generates a configurable number of messages (default 1000)
    assert len(prod.messages) == max_chars


def test_phone_number_uniq(prod):
    # random phone number.
    phone_numbers = set([i.phone_number for i in prod.messages])  # a list of all unique phone numbers
    assert len(
        phone_numbers) == max_chars  # asserts that there is as many unique phone numbers as there are phone numbers


def test_phone_number_length(prod):
    # Each message contains up to 100 random characters.
    for msg in prod.messages:
        assert len(msg.message) <= 100
