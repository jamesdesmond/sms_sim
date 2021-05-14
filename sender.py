import logging
import random
import sys
import time

import scipy.stats as stats

import producer

logging.basicConfig(stream=sys.stdout)


class Sender:

    def get_wait_times(self, wait_time_mean, max_wait, rand_iter):
        # returns a list, with specifed mean, std. dev. of length: rand_iter
        lower, upper = 0, max_wait
        mu, sigma = wait_time_mean, 1
        # truncnorm is used here as when I used normalvariate I would get negative random waits. I could abs() them,
        # but it throws off the configurable mean
        return (stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)).rvs(
            rand_iter).tolist()

    def __init__(self, wait_time_mean, fail_rate, max_wait=2, rand_iter=10000):
        # wait_time_mean: time (in sec.) to set the random generation's mean to
        # fail_rate: float (0-1) representing the probability of failure, 1=absolute success, 0=failure
        # max_wait: time (in sec.)
        # rand_iter: int, how many elemeents to populate random list time with
        self.wait_time_mean = wait_time_mean
        self.fail_rate = fail_rate
        self.max_wait = max_wait
        self.rand_iter = rand_iter
        self.wait_times = self.get_wait_times(wait_time_mean, max_wait, rand_iter)

    def send_message(self, msg: producer.Message, test=False):
        # simulates sending messages by waiting a random period of time and has a configurable failure rate.
        # msg: Message, this is the contents to send
        # returns: time taken per message, as a float representing seconds
        # or, 0 if message fail
        if random.random() > self.fail_rate:
            try:
                wait_time = (self.wait_times.pop())
            except IndexError as ie:
                # If the list is empty, then we must generate more random values
                self.wait_times = self.get_wait_times(wait_time_mean=self.wait_time_mean, max_wait=self.max_wait,
                                                      rand_iter=self.rand_iter)
                wait_time = (self.wait_times.pop())
            if not test:
                time.sleep(wait_time)
            logging.info(f'TO: {msg.phone_number}')
            logging.info(f'BODY: {msg.message}')
            logging.info(f'WAIT TIME: {wait_time} sec.')
            return wait_time
        else:
            return 0

    def __str__(self):
        return f'mean: {self.wait_time_mean}\nfail_rate: {self.fail_rate}\nmax_wait: {self.max_wait}\n' \
            f'random iterations: {self.rand_iter}\ncount of wait times: {len(self.wait_times)}'
