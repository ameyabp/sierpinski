import argparse
import svgwrite
import math
import random

R = 0.1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--canvas_size', help='Width of the canvas to draw on', type=int, default=1000)
    parser.add_argument('-i', '--num_iterations', help='Number of iterations to run', type=int, default=1000)
    parser.add_argument('-p1', '--point1', help='First point of the triangle - tuple with coordinates in range (0,1)', type=float, default=None)
    parser.add_argument('-p2', '--point2', help='Secind point of the triangle - tuple with coordinates in range (0,1)', type=float, default=None)
    parser.add_argument('-p3', '--point3', help='Third point of the triangle - tuple with coordinates in range (0,1)', type=float, default=None)

    args = parser.parse_args()
    canvas_size = (args.canvas_size, args.canvas_size)
    itr = args.num_iterations
    p1 = args.point1
    p2 = args.point2
    p3 = args.point3

    dwg = svgwrite.Drawing('sapinski.svg', canvas_size, profile='tiny')
    sapinski = dwg.g(stroke="blue", fill="rgb(90%,90%,100%)", stroke_width=0.25)

    # add the <g /> element to the <defs /> element of the drawing
    dwg.defs.add(sapinski)

    # add all the points
    # set base triangle vertices
    while not p1 or not p2 or not p3:
        x1 = random.random() * canvas_size[0]
        y1 = random.random() * canvas_size[0]
        
        x2 = random.random() * canvas_size[0]
        y2 = random.random() * canvas_size[0]
        
        x3 = random.random() * canvas_size[0]
        y3 = random.random() * canvas_size[0]

        # check if they are collinear
        if (x1 == x2 == x3) or math.isclose((y2-y1)/(x2-x1), (y3-y2)/(x3-x2)):
            # choose a different set of 3 points
            continue

        p1 = (x1, y1)
        p2 = (x2, y2)
        p3 = (x3, y3)

    vertices = [p1, p2, p3]
    for p in vertices:
        sapinski.add(dwg.circle((p[0], p[1]), R))

    # seed the iterations
    x = (p1[0] + p2[0] + p3[0])/3
    y = (p1[1] + p2[1] + p3[1])/3
    sapinski.add(dwg.circle((x, y), R))

    # start the iterations
    ctr = 0
    while ctr < itr:
        p = random.choice(vertices)
        x = (p[0] + x)/2
        y = (p[1] + y)/2
        sapinski.add(dwg.circle((x, y), R))

        ctr += 1

    use_sapinski = dwg.use(sapinski)
    dwg.add(use_sapinski)
    dwg.save()
