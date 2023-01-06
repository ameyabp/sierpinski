import argparse
import svgwrite
import math
import itertools
import random

R = 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--canvas_size', help='Width of the canvas to draw on', type=int, default=1000)
    parser.add_argument('-i', '--num_iterations', help='Number of iterations to run', type=int, default=1000)
    parser.add_argument('-v', '--num_vertices', help='Number of vertices to start with', type=int, default=2)
    parser.add_argument('-p', '--points', help='x & y coordinates of vertices, in range (0,1)', nargs='+', type=float, default=None)

    args = parser.parse_args()
    canvas_size = (args.canvas_size, args.canvas_size)
    itr = args.num_iterations
    num_vertices = args.num_vertices

    vertices = []
    if args.points:
        for i in range(num_vertices):
            vertices.append((args.points[2*i] * canvas_size[0], args.points[2*i+1] * canvas_size[0]))

    dwg = svgwrite.Drawing('sapinski.svg', canvas_size, profile='full')
    sapinski = dwg.g(stroke="blue", fill="rgb(90%,90%,100%)", stroke_width=0.25)

    # add the <g /> element to the <defs /> element of the drawing
    dwg.defs.add(sapinski)

    # add all the points
    # set base polygon vertices if not provided by user
    temp_vertices = []
    reselect = False
    while len(vertices) == 0:
        for i in range(num_vertices):
            x = random.random() * canvas_size[0]
            y = random.random() * canvas_size[0]

            temp_vertices.append((x,y))
        
        # check if they are collinear
        for combo in itertools.combinations(temp_vertices, 3):
            x1 = combo[0][0]
            y1 = combo[0][1]
            x2 = combo[1][0]
            y2 = combo[1][1]
            x3 = combo[2][0]
            y3 = combo[2][1]
            if (x1 == x2 == x3) or math.isclose((y2-y1)/(x2-x1), (y3-y2)/(x3-x2)):
                # choose a different set of vertices
                reselect = True
                break
        
        if reselect:
            reselect = False
            temp_vertices.clear()
            continue

        vertices = temp_vertices

    for p in vertices:
        sapinski.add(dwg.circle((p[0], p[1]), 2*R))

    # seed the iterations
    x = sum([p[0] for p in vertices])/num_vertices
    y = sum([p[1] for p in vertices])/num_vertices
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
