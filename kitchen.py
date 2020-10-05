from shelf import *
import time
import sys

from courier import Courier

class Kitchen(object):
    def __init__(self):
        self.hotShelf = HotShelf(10, self)
        self.coldShelf = ColdShelf(10, self)
        self.frozenShelf = FrozenShelf(10, self)
        self.overflowShelf = OverFlowShelf(15, self)
        self.shelves = {
            self.hotShelf.name: self.hotShelf,
            self.coldShelf.name: self.coldShelf,
            self.frozenShelf.name: self.frozenShelf,
            self.overflowShelf.name: self.overflowShelf
        }

    def printShelves(self):
        self.hotShelf.printShelf()
        self.coldShelf.printShelf()
        self.frozenShelf.printShelf()
        self.overflowShelf.printShelf()

    def addOrderToshelf(self, order):
        shelf = self.shelves.get(order.temp.lower())
        if shelf is None:
            raise Exception("no shelf found with order's temp %s" % order.temp)
        if not shelf.addOrder(order):
            self.overflowShelf.addOrder(order)

    def pickupOrder(self, order):
        shelf = self.shelves.get(order.temp.lower())
        if shelf is None:
            raise Exception("no shelf found with order's temp %s" % order.temp)
        pickupOrder = shelf.pickOrder(order)
        if pickupOrder is None:
            pickupOrder = self.overflowShelf.pickOrder(order)
        if pickupOrder is None:
            print('cannot pickup order at %s: %s. It may be discarded already' % (time.time(), order))
        return pickupOrder

    def dispatchCourier(self, order, executor):
        courier = Courier(self, executor)
        courier.dispatchOrder(order)

    def cook(self, order):
        print('%s order %s is cooked' % (time.time(), order), file=sys.stdout)
        self.addOrderToshelf(order)

