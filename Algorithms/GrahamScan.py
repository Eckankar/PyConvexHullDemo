from HullAlgorithm import HullAlgorithm
from math import atan2

class GrahamScan(HullAlgorithm):
    """
    Implements the Graham scan.
    O(n lg n)
    """
    def execute(self):
        def pt(p): return self.plane.points[p]

        def isLeftTurn(p1, p2, p3):
            (a, b), (c, d), (e, f) = pt(p1), pt(p2), pt(p3)
            return a*d - b*c + b*e - d*e + c*f - a*f < 0

        # Step 1: Find p_0
        activeMarker = self.markers.addPointMarker(0, (100, 100, 255))
        maxMarker = self.markers.addPointMarker(0, (0, 255, 0))
        maximum = 0
        yield
        for i in range(0, len(self.plane.points)):
            self.markers.movePointMarker(activeMarker, i)
            if pt(i)[1] > pt(maximum)[1]:
                self.markers.movePointMarker(maxMarker, i)
                maximum = i
            yield
        self.markers.removePointMarker(activeMarker)
        self.markers.removePointMarker(maxMarker)

        p0 = maximum

        # Step 2: Sort the rest
        sortedPoints = range(len(self.plane.points))
        del sortedPoints[p0]
        sortedPoints = sorted(
            sortedPoints,
            key = lambda k: -atan2(pt(k)[1] - pt(p0)[1], pt(k)[0] - pt(p0)[0])
        )
        yield

        stack = [p0]
        stack.extend(sortedPoints[0:2])

        lineStack = [
            self.markers.addLineMarker(p0, sortedPoints[0], (100, 100, 255)),
            self.markers.addLineMarker(sortedPoints[0], sortedPoints[1], (100, 100, 255))
        ]

        pointStack = [
            self.markers.addPointMarker(p0, (0, 255, 0)),
            self.markers.addPointMarker(sortedPoints[0], (0, 255, 0)),
            self.markers.addPointMarker(sortedPoints[1], (0, 255, 0))
        ]

        for p in sortedPoints[2:]:
            pMarker = self.markers.addPointMarker(p, (100, 100, 255))

            while not isLeftTurn(stack[-2], stack[-1], p):
                stack.pop()
                line = lineStack.pop()
                self.markers.removeLineMarker(line)
                point = pointStack.pop()
                self.markers.changePointMarkerColor(point, (255, 0, 0))
                yield

            self.markers.changePointMarkerColor(pMarker, (0, 255, 0))
            lineStack.append(
                    self.markers.addLineMarker(stack[-1], p, (100, 100, 255))
            )
            pointStack.append(pMarker)
            stack.append(p)
            yield

        self.markers.addLineMarker(stack[-1], p0, (100, 100, 255))

        self.hull = stack
