import threading
import time
import concurrent.futures


def thread_fun(name):
    print(f"starting thread {name} \n")
    time.sleep(1)
    print(f"finished thread {name} \n")


def thread_fun2(name):
    print(f"starting thread {name} \n")
    for i in range(10):
        print(i)
    print(f"finished thread {name} \n")


class DummyDB:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def write(self, name):
        print(f"running thread {name}\n")
        # only 1 thread can access now
        with self.lock:
            copy_value = self.value
            copy_value += 1
            time.sleep(1)
            self.value = copy_value
        print(f"finished thread {name}\n")


class ProducerConsumer:
    def __init__(self, max_size=10):
        self.queue = []
        self.max_size = max_size
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()

    def write_message(self, message):
        if len(self.queue) >= self.max_size:
            self.producer_lock.acquire()
        if self.producer_lock.locked():
            self.producer_lock.release()

        self.producer_lock.acquire()
        print(f"write message: {message} | queue size: {len(self.queue)}")
        time.sleep(0.1)
        self.queue.append(message)
        self.producer_lock.release()

    def read_message(self):
        self.consumer_lock.acquire()
        message = self.queue[-1]
        self.queue = self.queue[:-1]
        print(f"read message: {message}")
        self.consumer_lock.release()


if __name__ == '__main__':
    # start = time.time()
    # db = DummyDB()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as exec:
    #     # async start
    #     for i in range(3):
    #         exec.submit(db.write, i)
    # print("Final value", db.value, "time caused", time.time() - start)

    def produce(client: ProducerConsumer):
        for i in range(20):
            client.write_message(i)

    def consume(client: ProducerConsumer):
        while len(client.queue) > 0:
            print("consume size:", len(client.queue))
            client.read_message()

    cs = ProducerConsumer(10)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(produce, cs)
        ex.submit(consume, cs)




