import os
import threading  # needed to print without getting blocked by sleep()

from joblib import Parallel, delayed, parallel_backend

import producer
import sender


class ProgressMonitor:
    def __init__(self, producer: producer.Producer, senders: list(), refresh_rate=5):
        # producer is a Producer object
        # senders is a list of Sender objects
        # refresh_rate: time (in sec.) to wait before refreshing console
        self.producer = producer
        self.senders = senders
        self.refresh_rate = refresh_rate
        self.msg_sent = 0
        self.msg_fail = 0
        self.times = []
        self.avg_time = 0  # (in seconds)
        self.total_time = 0
        self.print_thread = None

    # TODO: allow senders to be added while ProgressMonitor is printing
    def add_sender(self, send: sender.Sender):
        self.senders.append(send)

    def __str__(self):
        # {self.msg_sent + self.msg_fail}/{len(self.producer.messages)}\n' \
        return f'Messages sent: {self.msg_sent}\nMessages failed: {self.msg_fail}\n' \
            f'Average time per message: {self.avg_time} sec.'
        # \n Total Time Slept:{self.total_time}

    def update_vars(self, send, msg):
        res = send.send_message(msg)
        # print(f'res received: {res}')
        if res != 0:
            self.msg_sent = self.msg_sent + 1
            self.times.append(res)
            self.avg_time = (sum(self.times) / len(self.times))
            self.total_time = self.total_time + res
        else:
            self.msg_fail = self.msg_fail + 1

    def _print(self, delay):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str(self))
        t = threading.Timer(delay, self._print, args=[delay])
        self.print_thread = t
        t.start()

    def exec(self):
        print(str(self))
        print_thread = threading.Timer(self.refresh_rate, self._print, args=[self.refresh_rate])
        self.print_thread = print_thread
        print_thread.start()
        # print(self)
        # This timer begins the printing loop
        # these loops will run simultaniously as the printing thread
        for send in self.senders:
            with parallel_backend('threading', n_jobs=-1):  # n_jobs=-1 will auto allocate cores
                Parallel()(delayed(self.update_vars)(send=send, msg=msg) for msg in self.producer.messages)
        print_thread.cancel()
        self.print_thread.cancel()
        print(str(self))
    # Current issue is that the print thread doesnt work, I tried putting it in main so I could get funky w/ it but wasn't looking good
    # I think I should move it back here and read up on if joblib is blocking
