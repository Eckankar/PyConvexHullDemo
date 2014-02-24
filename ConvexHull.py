#!/usr/bin/python
from Plane import Plane
from Markers import Markers
import pygame
from threading import Event, Thread
from Algorithms import *
from optparse import OptionParser
from time import sleep

class ConvexHull:
    """Visualization of sorting algorithms."""
    def __init__(self, algorithm, stop_event, options):
        self.stopEvent = stop_event

        self.numPoints = options.numPoints
        self.size = options.size
        self.pointSize = options.pointSize
        self.margin = options.margin
        self.closeDelay = options.closeDelay

        self.plane = Plane(self.numPoints)
        self.markers = Markers()

        algorithm.initialize(self.plane, self.markers)

        self.gen = algorithm.execute()

        pygame.init()
        self.window = pygame.display.set_mode((self.size + 2 * self.margin, self.size + 2 * self.margin))

        self.i = 0
        self.update()

    def update(self):
        """ Update the graphical display. """
        self.window.fill((255, 255, 255))

        def scale(p):
            (x, y) = p
            return (self.margin + int(x * self.size), self.margin + int(y * self.size))
        def pt(i):
            return scale(self.plane.points[i])

        for p in self.plane.points:
            pygame.draw.circle(self.window, (0, 0, 0), scale(p), self.pointSize)

        for l in self.markers.linemarkers.itervalues():
            pygame.draw.line(self.window, l['color'], pt(l['start']), pt(l['end']))

        for l in self.markers.verticalmarkers.itervalues():
            pygame.draw.line(self.window, l['color'], pt((l['x'], 0)), pt((l['x'], 1)))

        for p in self.markers.pointmarkers.itervalues():
            pygame.draw.circle(self.window, p['color'], pt(p['index']), self.pointSize)

        pygame.display.flip()

    def step(self):
        try:
            self.gen.next()
        except StopIteration:
            self.update()
            self.stopEvent.wait(self.closeDelay)
            self.stopEvent.set()


def main():
    """ Main method, called on execution of the .py from the commandline """
    algorithms = {
        'jarvismarch': JarvisMarch(),
        'grahamscan': GrahamScan(),
        'marriagebq': MarriageBeforeConquest(),
        'chan': ChansAlgorithm(),
    }
    parser = OptionParser()
    parser.add_option('-a', '--algorithm', type='choice',
                      default='jarvismarch', dest='algorithm',
                      choices=algorithms.keys(),
                      help='algorithm to use')
    parser.add_option('-d', '--delay', type='float',
                      default=0.01, dest='delay',
                      help='delay between each step in seconds')
    parser.add_option('-w', '--window-size', type='int',
                      default=400, dest='size',
                      help='size of window')
    parser.add_option('-p', '--point-size', type='int',
                      default=5, dest='pointSize',
                      help='size of the points')
    parser.add_option('-m', '--margin-width', type='int',
                      default=20, dest='margin',
                      help='size of window margin')
    parser.add_option('-n', type='int',
                      default=20, dest='numPoints',
                      help='number of points to find hull of')
    parser.add_option('-c', '--close-delay', type='int',
                      default=5, dest='closeDelay',
                      help='delay before the window closes on completion')
    (options, args) = parser.parse_args()
    algorithm = algorithms[options.algorithm];

    stopEvent = Event()

    disp = ConvexHull(algorithm, stopEvent, options)

    def update():
        """ Update loop; updates the screen every few seconds. """
        while True:
            stopEvent.wait(options.delay)
            disp.update()
            if stopEvent.isSet():
                break
            disp.step()

    t = Thread(target=update)
    t.start()

    while not stopEvent.isSet():
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stopEvent.set()
        except KeyboardInterrupt:
            stopEvent.set()

if __name__ == "__main__":
    main()

