class HullAlgorithm:
    """
    Base class to be used for convex hull algorithms.

    An algorithm must be initialized with initialize before use.

    The field 'plane' contains a Plane containing the points we're working on.
    
    The field 'markers' contains a Markers that can be used for illustrative
    purposes.
    """

    def initialize(self, plane, markers):
        """ Basic initialization of algorithm before use. """
        self.plane = plane
        self.markers = markers

    def execute(self):
        """
        Does the actual hull-finding.

        Should be implemented as a generator function, that is, it should yield
        execution after each significant step in its execution, to allow for
        redrawing of the display, as well as slowing down the execution for
        better visual effect.

        In addition, the algorithm should yield before doing anything, to allow
        for initial drawing of the unsolved problem.
        """
        pass
