import threading
import random
import time

class Courier(object):
    def __init__(self, kitchen, executor):
        self.kitchen = kitchen
        self.executor = executor

    def dispatchOrder(self, order):
        # print('%s dispatch order %s' % (time.time(), order))
        self.executor.submit(self.pickupOrder, order)

    def pickupOrder(self, order):
        time.sleep(random.uniform(2, 6))
        # print('%s pickup order %s' % (time.time(), order))
        self.kitchen.pickupOrder(order)

