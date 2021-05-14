import time

import producer
import progress_monitor
import sender

if __name__ == '__main__':
    start = time.time()
    prod = producer.Producer(num_messages=100)
    # mean_wait_time (in sec.), fail_rate (probablity 0-1), max_wait (in sec.)
    send1 = sender.Sender(3, 0.1, max_wait=5)
    send2 = sender.Sender(0.5, 0.25, max_wait=2)
    pro_mon = progress_monitor.ProgressMonitor(prod, [send1, send2], refresh_rate=1)
    pro_mon.exec()
    print(f'realtime elapsed: {time.time() - start}')
