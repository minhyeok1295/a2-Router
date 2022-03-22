import pickle

import threading


class ThreadSock(threading.thread):
    
    def __init__(self,node):
        threading.Thread.__init__(self)
        self.node = node
        # https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.node.open_thread_sock()
        while not self.stopped():
            self.router.receive()
        self.node.thread_sock.close()


def make_packet(src_ip, dest_ip, message, ttl):
    data = {
        'src_ip' : src_ip,
        'dest_ip' : dest_ip,
        'message' : message,
        'ttl' : ttl
    }
    return pickle.dumps(data)