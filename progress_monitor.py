import os # used to clear the terminal
import threading # needed to print without getting blocked by sleep()

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

    # TODO: allow senders to be added while ProgressMonitor is printing
    def add_sender(self, send: sender.Sender):
        self.send.append(sender)

    def __str__(self):
        # {self.msg_sent + self.msg_fail}/{len(self.producer.messages)}\n' \
        return f'Messages sent: {self.msg_sent}\nMessages failed: {self.msg_fail}\n' \
            f'Average time per message: {self.avg_time} sec.'

    def exec(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self)
        # This timer begins the printing loop
        print_thread = threading.Timer(self.refresh_rate, self.exec)
        print_thread.start()
        # these loops will run simultaniously as the printing thread
        for msg in self.producer.messages:
            for send in self.senders:
                res = send.send_message(msg)
                if res != 0:
                    self.msg_sent = self.msg_sent + 1
                    self.times.append(res)
                    self.avg_time = (sum(self.times) / len(self.times))
                else:
                    self.msg_fail = self.msg_fail + 1
        print_thread.cancel()
