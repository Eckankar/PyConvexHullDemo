from random import random

class Plane:
    """
    Container for the points.
    Points are stored in the field 'points'.
    """
    def __init__(self, n):
        self.points = [(random(), random()) for i in range(n)]
