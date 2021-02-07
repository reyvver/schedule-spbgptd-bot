from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


# import time, traceback
#
#
# def every(delay, task):
#     next_time = time.time() + delay
#     while True:
#         time.sleep(max(0, next_time - time.time()))
#         try:
#             task()
#         except Exception:
#             traceback.print_exc()
#             # in production code you might want to have this instead of course:
#             # logger.exception("Problem while executing repetitive task.")
#         # skip tasks if we are behind schedule:
#         next_time += (time.time() - next_time) // delay * delay + delay
#
#
# def foo():
#     print("foo", time.time())
#


