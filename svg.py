# using svgfig
import sys, os, random

from svgfig import *
# When having something to import first load it, transform in into a path and then work on it

def initialize():
    # svgfig.canvas().attr["font-family"]
    # With this I can change the default canvas settings
    # svgfig.canvas_defaults["font-family"]
    canvas().attr["viewBox"] = "0 0 800 600"


def run(tasksets):
    pass

def make_cell(dim, color, text, pos):
    """ Creates a cell containing text and of color color """
    text = SVG("text", SVG("tspan", text),  x = pos[0], y = pos[1], stroke = "none", fill = color - 0x100)
    rect = SVG("rect", x = pos[0], y = pos[1], width = dim, height = dim, fill = color)
    return Fig(text, rect).SVG()

def make_line(dim):
    dim = 20
    dist = 1
    pos = [0, 20]
    s = SVG("g")
    color = 0
    next_color = lambda x: (x + 0x1000) % 0xFFFFFF

    for i in range(dim):
        s.append(make_cell(dim, color, "text " + str(i), pos))
        pos[0] += dim + 1
        color = next_color(color)
    
    test_svg(s)

def test_svg(image):
    f = os.tempnam() + ".svg"
    canvas(image, viewBox = "0 0 800 600").save(f)
    print "saving to", f
    os.system("open %s" % f)

if __name__ == '__main__':
    initialize()
    make_line(10)
