from optparse import OptionParser
import json
import time
from concurrent.futures import ThreadPoolExecutor

from kitchen import Kitchen
from order import Order

parser = OptionParser()

def main(options, args):
    kitchen = Kitchen()
    executor = ThreadPoolExecutor(max_workers=4)
    while True:
        try:
            orderString = input()
            order = Order(**json.loads(orderString))
            # print("receive order at %s: %s" % (time.time(), order))
        except Exception as e:
            continue
        kitchen.dispatchCourier(order, executor)
        kitchen.cook(order)


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    main(options, args)