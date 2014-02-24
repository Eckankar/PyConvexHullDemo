from HullAlgorithm import HullAlgorithm
from Subplane import Subplane
from Submarkers import Submarkers
from GrahamScan import GrahamScan
from math import ceil

class ChansAlgorithm(HullAlgorithm):
    """
    Implements Chan's algorithm for finding the convex hull.
    http://www.cs.ucsb.edu/~suri/cs235/ChanCH.pdf
    O(n lg h)
    """
    def execute(self):
        self.omarkers = self.markers
        subplane = Subplane(self.plane, range(len(self.plane.points)))
        self.markers = Submarkers(self.markers, subplane)

        t = 1
        self.done = False
        while not self.done:
            self.markers.clearMarkers()
            H = 2**(2**t)
            m = min(H, len(self.plane.points))
            for x in self.hull2D(m, H): yield
            t += 1

    def hull2D(self, m, H):
        def pt(p): return self.plane.points[p]
        def isLeftTurn(p1, p2, p3):
            (a, b), (c, d), (e, f) = pt(p1), pt(p2), pt(p3)
            return a*d - b*c + b*e - d*e + c*f - a*f < 0

        def chunks(l, n):
            """
            Yield successive n-sized chunks from l.
            http://stackoverflow.com/a/312464/79061
            """
            for i in xrange(0, len(l), n):
                yield l[i:i+n]

        def rtangent(hull, p):
            """
            Return the index of the point in hull that the right tangent line from
            p to hull touches.

            http://tomswitzer.net/2010/12/2d-convex-hulls-chans-algorithm/
            """
            done = False
            l, r = 0, len(hull)
            l_prev = isLeftTurn(p, hull[0], hull[-1])
            l_next = isLeftTurn(p, hull[0], hull[(l + 1) % r])

            lmarker = self.markers.addPointMarker(hull[0], (255, 255, 0))
            rmarker = self.markers.addPointMarker(hull[0], (255, 255, 0))
            cmarker = self.markers.addPointMarker(hull[0], (255, 0, 0))
            while l < r and not done:
                yield
                c = (l + r) / 2
                self.markers.movePointMarker(cmarker, c)
                c_prev = isLeftTurn(p, hull[c], hull[(c - 1) % len(hull)])
                c_next = isLeftTurn(p, hull[c], hull[(c + 1) % len(hull)])
                c_side = isLeftTurn(p, hull[l], hull[c])
                if c_prev and c_next:
                    done = True
                    yield c
                elif c_side and (not l_next or l_prev == l_next) or \
                        not c_side and not c_prev:
                    r = c               # Tangent touches left chain
                    self.markers.movePointMarker(rmarker, hull[r])
                else:
                    l = c + 1           # Tangent touches right chain
                    self.markers.movePointMarker(lmarker, l)
                    l_prev = -c_next    # Switch sides
                    l_next = isLeftTurn(p, hull[l], hull[(l + 1) % len(hull)])

            if not done:
                yield l

            for m in [lmarker,cmarker,rmarker]: self.markers.removePointMarker(m)

        n = len(self.plane.points)

        # Partition into n/m partitions of size at most m
        grahams = []
        for chunk in chunks(range(n), m):
            markers = [self.markers.addPointMarker(i, (0, 50, 200)) for i in chunk]
            yield

            subplane = Subplane(self.plane, chunk)
            submarkers = Submarkers(self.markers, subplane)

            graham = GrahamScan()
            graham.initialize(subplane, submarkers)
            for x in graham.execute(): yield
            graham.hull = [subplane.tr(i) for i in graham.hull]
            grahams.append(graham)

            submarkers.clearPointMarkers()
            for i in markers: self.markers.removePointMarker(i)
            yield

        # Find p_1 
        activeMarker = self.markers.addPointMarker(0, (100, 100, 255))
        maxMarker = self.markers.addPointMarker(0, (0, 255, 0))
        maximum = 0
        yield
        for i in range(0, len(self.plane.points)):
            self.markers.movePointMarker(activeMarker, i)
            if pt(i)[0] > pt(maximum)[0]:
                self.markers.movePointMarker(maxMarker, i)
                maximum = i
            yield
        self.markers.removePointMarker(activeMarker)
        self.markers.removePointMarker(maxMarker)

        finalhull = [maximum]
        self.markers.addPointMarker(maximum, (255, 0, 0))
        yield

        # Determine which hull p_1 is on:
        for graham in grahams:
            if maximum in graham.hull:
                lastGraham = graham
                lastHullPos = graham.hull.index(maximum)

                break

        for k in range(H):
            p = finalhull[-1]

            thisGraham = None
            qbestMarker = None
            qbest = None
            qlMarker = None
            for graham in grahams:
                if graham == lastGraham:
                    # If we're trying the same hull again; simply pick the
                    # next point on it.
                    newhp = (lastHullPos + 1) % len(graham.hull)
                else:
                    for x in rtangent(graham.hull, p):
                        yield
                        newhp = x

                qnew = graham.hull[newhp % len(graham.hull)]

                if qbest is None or isLeftTurn(p, qnew, qbest):
                    if qbest is None:
                        qbestMarker = self.markers.addPointMarker(qnew, (255, 0, 0))
                        qlMarker = self.markers.addLineMarker(p, qnew, (255, 0, 0))
                    else:
                        self.markers.movePointMarker(qbestMarker, qnew)
                        self.markers.moveLineMarker(qlMarker, p, qnew)

                    qbest = qnew
                    lastHullPos = newhp
                    lastGraham = graham
            yield

            finalhull.append(qbest)
            qbestMarker = None
            yield

            # We are done!
            if qbest == maximum:
                self.markers.addLineMarker(qbest, maximum, (255, 0, 0))
                self.done = True
                break

        yield

        for graham in grahams:
            graham.markers.clearMarkers()

