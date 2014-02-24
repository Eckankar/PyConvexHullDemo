class Submarkers:
    """
    Acts like Markers, but works on a Subplane, performing index translation to a
    backing marker instance.
    """
    def __init__(self, markers, subplane):
        self.markers = markers
        self.subplane = subplane

        self.linemarkers = {}
        self.pointmarkers = {}
        self.verticalmarkers = {}

    def tr(self, i):
        return self.subplane.tr(i)

    def clearPointMarkers(self):
        """ Remove all added point markers """
        ms = [x for x in self.pointmarkers]
        for i in ms: self.removePointMarker(i)

    def clearLineMarkers(self):
        """ Remove all added line markers """
        ms = [x for x in self.linemarkers]
        for i in ms: self.removeLineMarker(i)

    def clearVerticalMarkers(self):
        """ Remove all added vertical markers """
        ms = [x for x in self.verticalmarkers]
        for i in ms: self.removeVerticalMarker(i)

    def clearMarkers(self):
        """ Remove all added markers """
        self.clearPointMarkers()
        self.clearLineMarkers()
        self.clearVerticalMarkers()

    def addPointMarker(self, index, color):
        m = self.markers.addPointMarker(self.tr(index), color)
        self.pointmarkers[m] = m
        return m

    def addLineMarker(self, start, end, color):
        m = self.markers.addLineMarker(self.tr(start), self.tr(end), color)
        self.linemarkers[m] = m
        return m

    def addVerticalMarker(self, x, color):
        m = self.markers.addVerticalMarker(x, color)
        self.verticalmarkers[m] = m
        return m

    def movePointMarker(self, id, index):
        self.markers.movePointMarker(id, self.tr(index))

    def moveLineMarker(self, id, start, end):
        self.markers.moveLineMarker(id, self.tr(start), self.tr(end))

    def moveVerticalMarker(self, id, x):
        self.markers.moveVerticalMarker(id, x)

    def changePointMarkerColor(self, id, color):
        self.markers.changePointMarkerColor(id, color)

    def changeLineMarkerColor(self, id, color):
        self.markers.changeLineMarkerColor(id, color)

    def changeVerticalMarkerColor(self, id, color):
        self.markers.changeVerticalMarkerColor(id, color)

    def removePointMarker(self, id):
        self.markers.removePointMarker(id)
        del self.pointmarkers[id]

    def removeLineMarker(self, id):
        self.markers.removeLineMarker(id)
        del self.linemarkers[id]

    def removeVerticalMarker(self, id):
        self.markers.removeVerticalMarker(id)
        del self.verticalmarkers[id]

