import time
import random
import threading
import sys

class Shelf(object):
    def __init__(self, capacity, kitchen, name):
        self.capacity = capacity
        self.kitchen = kitchen
        self.name = name
        self.shelfDecayModifier = 1
        self.orders = {}
        self.lock = threading.RLock()

    def printShelf(self):
        self.lock.acquire()
        for orderId, orderAndTime in self.orders.items():
            order, orderTime = orderAndTime
            print('order %s was added in shelf %s at %s' % (order, self.name, orderTime))
        self.lock.release()

    def cleanOrders(self):
        for orderId, orderAndTime in self.orders.items():
            order, orderTime = orderAndTime
            value = self.calcValue(order, orderTime)
            if value <= 0.0:
                print('%s discard order %s from shelf %s with value %s' % (time.time(), order, self.name, value))
                del self.orders[orderId]
                self.kitchen.printShelves()

    def orderMatch(self, order):
        return order.temp.lower() == self.name

    def replaceOrder(self, order):
        return None

    def addOrder(self, order):
        self.lock.acquire()
        if self.orderMatch(order):
            self.cleanOrders()
            if len(self.orders) < self.capacity:
                orderTime = time.time()
                self.orders[order.id] = (order, orderTime)
                print(
                    '%s add order %s to shelf %s with value %s' % (
                        time.time(), order, self.name, self.calcValue(order, orderTime)
                    ),
                    file=sys.stdout
                )
                self.lock.release()
                self.kitchen.printShelves()
                return True
            else:
                order = self.replaceOrder(order)
                if order is not None:
                    self.lock.release()
                    self.kitchen.printShelves()
                    return True
        self.lock.release()
        return False

    def pickOrder(self, order):
        self.lock.acquire()
        order, orderTime = self.orders.pop(order.id)
        self.lock.release()
        if order is not None:
            value = self.calcValue(order, orderTime)
            if value <= 0:
                print(
                    "%s discard order %s from shelf %s when pickup with value %s" % (
                        time.time(), order, self.name, value
                    )
                )
                self.kitchen.printShelves()
                return None
            else:
                print(
                    '%s pickup order %s from shelf %s with value %s' % (
                        time.time(), order, self.name, value
                    ),
                    file=sys.stdout
                )
                self.kitchen.printShelves()
                return order
        return order

    def calcValue(self, order, orderInShelfTime):
        orderAge = time.time() - orderInShelfTime
        return (order.shelfLife - orderAge - order.decayRate * orderAge * self.shelfDecayModifier) / float(order.shelfLife)

class HotShelf(Shelf):
    def __init__(self, capacity, kitchen):
        super().__init__(capacity, kitchen, 'hot')

class ColdShelf(Shelf):
    def __init__(self, capacity, kitchen):
        super().__init__(capacity, kitchen, 'cold')

class FrozenShelf(Shelf):
    def __init__(self, capacity, kitchen):
        super().__init__(capacity, kitchen, 'frozen')

class OverFlowShelf(Shelf):
    def __init__(self, capacity, kitchen):
        super().__init__(capacity, kitchen, 'overflow')
        self.shelfDecayModifier = 2

    def orderMatch(self, order):
        return True

    def replaceOrder(self, order):
        orderIds = list(self.orders.keys())
        orderId = random.choice(orderIds)
        replacedOrder, replacedOrderTime = self.orders.pop(orderId)
        print(
            '%s overflow shelf discards replaced order %s with value %s' % (
                time.time(), replacedOrder, self.calcValue(replacedOrder, replacedOrderTime)
            ),
            file=sys.stdout
        )
        self.orders[order.id] = (order, time.time())
