import statistics

import pytest

import producer
import sender

mean = 3
fail_rate = 0.1
max_wait = 5
num_messages = 100000


@pytest.fixture()
def times(request):
    prod = producer.Producer(num_messages=num_messages)
    send = sender.Sender(mean, fail_rate, max_wait)
    return [send.send_message(i, test=True) for i in prod.messages]


def test_mean(times):
    # A sender, who picks up messages from the producer and simulates sending messages by
    # waiting a random period time distributed around a configurable mean.
    times.remove(0)  # get rid of failures
    calculated_mean = statistics.mean(times)
    fudge_factor = mean / 10
    # this test ensure the actual mean is +- 1/10 of the actual expected mean.
    print(f'calculated mean: {calculated_mean}')
    assert calculated_mean <= mean + fudge_factor or calculated_mean >= mean - fudge_factor


def test_fail_rate(times):
    # The sender also has a configurable failure rate.
    failures = times.count(0)
    fudge_factor = 0.1
    print(f'fail rate: {(failures / num_messages)}')
    assert (failures / num_messages) <= fail_rate + fudge_factor or (
                failures / num_messages) >= fail_rate - fudge_factor
