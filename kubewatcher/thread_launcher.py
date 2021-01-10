import threading


class ThreadLauncher(object):
    _threads = []

    def launch(self, target, args):
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True
        self._threads.append(thread)
        thread.start()

    def join(self):
        for t in self._threads:
            t.join()
