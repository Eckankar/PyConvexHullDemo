from HullAlgorithm import HullAlgorithm
from bisect import bisect_left

class PointPruning(HullAlgorithm):
    """
    Solves the convex hull problem by pruning points inside of triangles.

    O(n^2)

    This method is flawed!
    """
    def execute(self):
        def pt(p): return self.plane.points[p]

        def isLeftTurn(p1, p2, p3):
            (a, b), (c, d), (e, f) = pt(p1), pt(p2), pt(p3)
            return a*d - b*c + b*e - d*e + c*f - a*f < 0

        def index(a, x):
            i = bisect_left(a, x)
            if i != len(a) and a[i] == x:
                return i
            return False

        def remove(a, x):
            i = index(a, x)
            if i != False:
                del a[i]

        # Step 1: Find top-most and bottom-most points 
        activeMarker = self.markers.addPointMarker(0, (100, 100, 255))
        maxMarker = self.markers.addPointMarker(0, (0, 255, 0))
        minMarker = self.markers.addPointMarker(0, (0, 255, 0))
        maximum = 0
        minimum = 0
        yield
        for i in range(0, len(self.plane.points)):
            self.markers.movePointMarker(activeMarker, i)
            if pt(i)[1] > pt(maximum)[1]:
                self.markers.movePointMarker(maxMarker, i)
                maximum = i
            if pt(i)[1] < pt(minimum)[1]:
                self.markers.movePointMarker(minMarker, i)
                minimum = i
            yield
        self.markers.removePointMarker(activeMarker)

        # Step 2: Go through all triangles containing those two points as corners.
        # Prune any points contained in any triangle.
        hull = range(0, len(self.plane.points))

        line1 = self.markers.addLineMarker(minimum, maximum, (0, 255, 0))
        line2 = self.markers.addLineMarker(minimum, maximum, (0, 255, 0))
        line3 = self.markers.addLineMarker(minimum, maximum, (0, 255, 0))
        for i in range(0, len(self.plane.points)):
            if i == maximum or i == minimum or index(hull, i) is False: continue

            self.markers.moveLineMarker(line2, minimum, i)
            self.markers.moveLineMarker(line3, maximum, i)
            yield

            activeMarker = self.markers.addPointMarker(0, (100, 100, 255))
            for p in [j for j in hull]:
                if p == maximum or p == minimum or p == i: continue
                self.markers.movePointMarker(activeMarker, p)
                lt1 = isLeftTurn(minimum, maximum, p)
                lt2 = isLeftTurn(maximum, i, p)
                lt3 = isLeftTurn(i, minimum, p)
                ltc = isLeftTurn(minimum, maximum, i)

                if ltc == lt1 and ltc == lt2 and ltc == lt3:
                    remove(hull, p)
                    self.markers.addPointMarker(p, (200, 200, 200))
                yield
            self.markers.removePointMarker(activeMarker)

        for l in [line1, line2, line3]: self.markers.removeLineMarker(l)
        self.markers.removePointMarker(maxMarker)
        self.markers.removePointMarker(minMarker)
        yield

