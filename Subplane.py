class Subplane:
    """
    Contains a subset of points for a plane.
    """
    def __init__(self, plane, subset):
        self.plane = plane
        self.subset = subset
        self.points = [plane.points[i] for i in subset]

    def tr(self, i):
        """ Translates from local to global index """
        return self.subset[i]
