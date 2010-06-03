from HullAlgorithm import HullAlgorithm

class JarvisMarch(HullAlgorithm):
    """
    Implements Jarvis' March
    O(hn), h = size of convex hull
    """
    def execute(self):
        def pt(p): return self.plane.points[p]

        def isLeftTurn(p1, p2, p3):
            (a, b), (c, d), (e, f) = pt(p1), pt(p2), pt(p3)
            return a*d - b*c + b*e - d*e + c*f - a*f < 0

        # Step 1: Find the initial point for the hull
        activeMarker = self.markers.addPointMarker(0, (100, 100, 255))
        minMarker = self.markers.addPointMarker(0, (0, 255, 0))
        minimum = 0
        yield
        for i in range(0, len(self.plane.points)):
            self.markers.movePointMarker(activeMarker, i)
            if pt(i)[0] < pt(minimum)[0]:
                self.markers.movePointMarker(minMarker, i)
                minimum = i
            yield
        self.markers.removePointMarker(activeMarker)
        self.markers.removePointMarker(minMarker)

        currentPoint = minimum

        # Step 2: March around
        first = True
        while first or currentPoint != minimum:
            first = False
            activeMarker = self.markers.addPointMarker(currentPoint, (100, 100, 255))
            currentMarker = self.markers.addPointMarker(currentPoint, (0, 0, 255))
            yield
            nextPoint = None
            for i in range(0, len(self.plane.points)):
                self.markers.movePointMarker(activeMarker, i)
                if i == currentPoint:
                    continue
                elif nextPoint == None:
                    nextPoint = i
                    nextLineMarker = self.markers.addLineMarker(currentPoint, nextPoint, (100, 100, 255))
                elif not isLeftTurn(currentPoint, nextPoint, i):
                    nextPoint = i
                    self.markers.moveLineMarker(nextLineMarker, currentPoint, nextPoint)
                yield
            self.markers.removePointMarker(activeMarker)
            self.markers.removePointMarker(currentMarker)
            self.markers.removeLineMarker(nextLineMarker)

            self.markers.addLineMarker(currentPoint, nextPoint, (0, 255, 0))
            self.markers.addPointMarker(currentPoint, (0, 255, 0))

            currentPoint = nextPoint
            yield
