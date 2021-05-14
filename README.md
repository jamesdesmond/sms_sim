The objective is to simulate sending a large number of SMS alerts, like for an emergency alert
service. The simulation consists of three parts:
1. A producer that generates a configurable number of messages (default 1000) to random
phone number.
2. A sender, who picks up messages from the producer and simulates sending messages by
waiting a random period time distributed around a configurable mean. The sender also
has a configurable failure rate.
3. A progress monitor that displays the following and updates it every N seconds
(configurable):
a. Number of messages sent so far
b. Number of messages failed so far
c. Average time per message so far

One instance each for the producer and the progress monitor will be started while a variable
number of senders can be started with different mean processing time and error rate settings.
You are free in the programming language you choose, but your code should come with
reasonable unit testing.

# How to run
- `git pull git@github.com:jamesdesmond/sms_sim.git`
- `cd sms_sim/`
- `pip install -r requirements.txt`
- `python main.py`
- `python main.py --log=INFO` This will print the sms message as soon as it is "sent"
- `python -m pytest` This will run unit tests

# Comments on solution
- The progress_monitor is supposed to update every N seconds. I have implemented this, but the progress monitor will also print at the beginning and end of execution.
- The progress_monitor will attempt to clear the term it is running on when it refreshes, this doesn't work on Pycharm's output.
- The progress_monitor's `__str__()` method has a few things commented out because they were not specifically asked for in the assignment, but they were helpful for verifying correctness.
- The requirements don't mention if a sender should be able to be added to a Progress Monitor that is already running. My current solution does not support adding senders.
- The requirements don't mention if any retry logic should be implemented. If needed I would just need to add a config value: max_retries, and if fail, recall send_message unless it has already been called == max_retries
- My first attempt at a solution was single threaded, and simulating 28 seconds of time.sleep() took me 29 seconds. time.sleep() is not GIL blocking, so threading should be a great solution. After implementing joblib's Parallel() I was able to simulate 33 seconds of time.sleep() in just 7 seconds of realtime. (Running on CPU: Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz)
    - Build settings:
        - messages: 10
        - senders:
            - sender1
                - wait_time_mean : 3
                - fail_rate : 0.1
                - max_wait : 5
            - sender2
                - wait_time_mean : 0.5
                - fail_rate : 0.25
                - max_wait : 2
- I did not include unit tests for progress_monitor. I felt the simple tests to implement (e.g. making sure I can add senders before exec(), or testing the simple logic of update_vars) would not be that helpful to me, and would result in writing tests so constrained to the test cases, they may not even be useful if any changes occurs to progress_monitor. The threading as well would result in tests that are more complicated than the code itself.
