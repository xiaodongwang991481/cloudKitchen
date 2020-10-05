class Order(object):
    def __init__(self, id, name, temp, shelfLife, decayRate):
        self.id = id
        self.name = name
        self.temp = temp
        self.shelfLife = shelfLife
        self.decayRate = decayRate

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "temp": self.temp,
            "shelfLife": self.shelfLife,
            "decayRate": self.decayRate
        }

    def __str__(self):
        return str(self.toDict())

    def __repr__(self):
        return repr(self.toDict())