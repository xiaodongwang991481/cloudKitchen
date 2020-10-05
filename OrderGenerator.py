from optparse import OptionParser
import json
import random
import time
import uuid
import sys

from order import Order

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  default="orders.json",
                  help="json sample file", metavar="FILE")
parser.add_option("-r", "--rate",
                  dest="rate", default=2, type="int",
                  help="order generating rate")



if __name__ == "__main__":
    (options, args) = parser.parse_args()
    with open(options.filename) as file:
        content = file.read()
        orders = [Order(**order) for order in json.loads(content)]
    rate = options.rate
    interval = 1.0 / rate
    while True:
        order = random.choice(orders)
        order.id = str(uuid.uuid1())
        print(json.dumps(order.toDict()), file=sys.stdout)
        sys.stdout.flush()
        time.sleep(interval)
